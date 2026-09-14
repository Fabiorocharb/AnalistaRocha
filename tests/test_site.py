"""Regressões do site: python -m unittest discover -s tests -v.

Requer Playwright e Google Chrome (python -m pip install playwright).
Nenhuma mensagem é enviada: a abertura do WhatsApp é interceptada.
"""

import functools
import os
from pathlib import Path
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(QuietHandler, directory=str(ROOT))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="chrome", headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.context = self.browser.new_context(reduced_motion="reduce")
        # Os testes principais devem funcionar mesmo sem as CDNs.
        self.context.route("https://**/*", lambda route: route.abort())
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.goto(self.url)

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], "Erros de JavaScript")

    def assert_layout(self):
        self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"),
                        self.page.evaluate("Array.from(document.querySelectorAll('body *')).filter(el => el.getBoundingClientRect().right > innerWidth && !el.closest('.carousel')).map(el => el.tagName + '#' + el.id + '.' + el.className).slice(0, 12)"))
        self.assertTrue(self.page.locator(".cards").evaluate_all("""cards => cards.every(card => {
            const text = card.querySelector('p').getBoundingClientRect();
            const box = card.getBoundingClientRect();
            return text.bottom <= box.bottom && text.left >= box.left && text.right <= box.right;
        })"""))
        self.assertTrue(self.page.locator("#header").evaluate("""header => {
            const logo = header.querySelector('figure').getBoundingClientRect();
            const nav = header.querySelector('nav').getBoundingClientRect();
            return logo.right <= nav.left || logo.bottom <= nav.top;
        }"""))

    def test_responsive_layout(self):
        for width, height in [(320, 568), (360, 800), (390, 844), (480, 800),
                              (600, 800), (768, 1024), (820, 1180), (1023, 800),
                              (1024, 768), (1280, 800), (1366, 768), (1920, 1080),
                              (2560, 1440), (844, 390)]:
            with self.subTest(width=width, height=height):
                self.page.set_viewport_size({"width": width, "height": height})
                self.assert_layout()
                self.page.locator(".dot").nth(4).click()
                self.page.wait_for_function("document.querySelectorAll('.dot')[4].getAttribute('aria-current') === 'true'")
                self.assert_layout()

    def test_rows_has_no_exposed_sides_or_vertical_clipping(self):
        self.page.emulate_media(reduced_motion="no-preference")
        self.page.wait_for_function("document.querySelector('#rows img').complete")
        for width, height in [(320, 568), (390, 844), (768, 1024), (844, 390),
                              (1024, 768), (1366, 768), (1920, 1080),
                              (2560, 1440), (3440, 1440), (3840, 2160)]:
            with self.subTest(width=width, height=height):
                self.page.set_viewport_size({"width": width, "height": height})
                image = self.page.locator("#rows img")
                self.assertTrue(image.is_visible())
                left_positions = []
                for time in [0, 1250, 2500, 3750, 5000, 7500, 10000]:
                    metrics = image.evaluate("""(image, time) => {
                        const animation = image.getAnimations()[0];
                        animation.pause();
                        animation.currentTime = time;
                        const box = image.getBoundingClientRect();
                        const container = image.parentElement.getBoundingClientRect();
                        return {
                            coversSides: box.left + box.width * .03 <= container.left &&
                                         box.right - box.width * .03 >= container.right,
                            fitsVertically: box.top >= container.top && box.bottom <= container.bottom,
                            width: box.width, height: box.height, left: box.left
                        };
                    }""", time)
                    self.assertTrue(metrics["coversSides"], metrics)
                    self.assertTrue(metrics["fitsVertically"], metrics)
                    if width < 1024:
                        self.assertAlmostEqual(metrics["height"], max(height * .3, width * 1.2 / 3.5), delta=1)
                        self.assertAlmostEqual(metrics["width"] / metrics["height"], 3.5, places=2)
                    else:
                        self.assertLessEqual(metrics["height"], 360.01)
                    left_positions.append(metrics["left"])
                self.assertGreater(max(left_positions) - min(left_positions), 10)
                self.assert_layout()
                output = os.environ.get("SITE_SCREENSHOT_DIR")
                if output and width in [390, 1920, 3440]:
                    Path(output).mkdir(parents=True, exist_ok=True)
                    for time in [0, 5000]:
                        image.evaluate("(el, time) => { el.getAnimations()[0].currentTime = time; }", time)
                        self.page.locator("#rows").screenshot(path=str(Path(output) / f"rows-{width}-{time}.png"))
        self.page.emulate_media(reduced_motion="reduce")
        self.assertEqual(self.page.locator("#rows img").evaluate("el => getComputedStyle(el).animationName"), "none")

    def test_mobile_menu_and_resize(self):
        self.page.set_viewport_size({"width": 390, "height": 844})
        button = self.page.locator("#btn-mobile")
        button.click()
        self.assertEqual(button.get_attribute("aria-expanded"), "true")
        self.assert_layout()
        self.page.keyboard.press("Escape")
        self.assertEqual(button.get_attribute("aria-expanded"), "false")
        self.assertTrue(button.evaluate("el => el === document.activeElement"))
        button.click()
        self.page.locator("h1").click()
        self.assertEqual(button.get_attribute("aria-expanded"), "false")
        button.click()
        self.page.set_viewport_size({"width": 1280, "height": 800})
        self.page.wait_for_function("document.getElementById('btn-mobile').getAttribute('aria-expanded') === 'false'")
        self.assertEqual(button.get_attribute("aria-expanded"), "false")
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.assertFalse(self.page.locator("#menu1").is_visible())
        button.click()
        self.page.locator('#menu1 a[href="#talkProject"]').click()
        self.assertEqual(button.get_attribute("aria-expanded"), "false")
        self.assertTrue(self.page.locator("#talkProject").evaluate("el => el === document.activeElement"))
        self.assertGreaterEqual(self.page.locator("#talkProject").bounding_box()["y"], 80)

    def test_carousel_buttons_keyboard_and_scroll(self):
        self.page.locator(".carousel-next").click()
        self.page.wait_for_function("document.querySelectorAll('.dot')[1].hasAttribute('aria-current')")
        self.page.locator(".carousel-prev").click()
        self.page.wait_for_function("document.querySelectorAll('.dot')[0].hasAttribute('aria-current')")
        self.page.locator(".carousel-prev").click()
        self.page.wait_for_function("document.querySelectorAll('.dot')[4].hasAttribute('aria-current')")
        carousel = self.page.locator(".carousel")
        carousel.focus()
        self.page.keyboard.press("Home")
        self.page.wait_for_function("document.querySelectorAll('.dot')[0].hasAttribute('aria-current')")
        self.page.keyboard.press("ArrowRight")
        self.page.wait_for_function("document.querySelectorAll('.dot')[1].hasAttribute('aria-current')")
        carousel.evaluate("el => el.scrollLeft = el.clientWidth * 3")
        self.page.wait_for_function("document.querySelectorAll('.dot')[3].hasAttribute('aria-current')")
        self.assertEqual(self.page.locator('.dot[aria-current="true"]').count(), 1)
        self.page.locator(".project a").nth(2).focus()
        self.page.wait_for_function("document.querySelectorAll('.dot')[2].hasAttribute('aria-current')")

    def test_contact_validation_and_draft(self):
        expected_phone = parse_qs(urlparse(self.page.locator("#contact-whatsapp").get_attribute("href")).query)["phone"]
        self.context.route("https://api.whatsapp.com/**", lambda route: route.fulfill(status=200, content_type="text/html", body="<p>WhatsApp interceptado para teste.</p>"))
        self.page.evaluate("window.contactPageMarker = true")
        submit = self.page.locator('button[type="submit"]')
        submit.click()
        self.assertEqual(len(self.context.pages), 1)
        self.page.locator("#nome").fill("   ")
        self.page.locator("#email").fill("teste@example.com")
        self.page.locator("#mensagem").fill("   ")
        submit.click()
        self.assertEqual(len(self.context.pages), 1)
        self.assertTrue(self.page.evaluate("window.contactPageMarker"))
        self.page.locator("#nome").fill("Teste de revisão")
        self.page.locator("#mensagem").fill("Olá! Orçamento & dúvidas?\nQuero um site.")
        with self.context.expect_page() as popup_info, self.page.expect_navigation(wait_until="load"):
            submit.click()
        popup = popup_info.value
        popup.wait_for_url("https://api.whatsapp.com/**")
        query = parse_qs(urlparse(popup.url).query)
        self.assertEqual(query["phone"], expected_phone)
        self.assertEqual(query["text"], ["Olá! Me chamo Teste de revisão.\nEmail: teste@example.com\n\nOlá! Orçamento & dúvidas?\nQuero um site."])
        self.assertTrue(popup.evaluate("window.opener === null"))
        self.assertEqual(popup.evaluate("document.referrer"), "")
        self.assertIsNone(self.page.evaluate("window.contactPageMarker"))
        for field in ["nome", "email", "mensagem"]:
            self.assertEqual(self.page.locator(f"#{field}").input_value(), "")
        self.assertFalse(self.page.locator("#contact-draft").is_visible())
        self.assertEqual(self.page.locator("#contact-status").inner_text(), "")

    def test_contact_preserves_fields_if_popup_blocked(self):
        self.page.evaluate("() => { window.contactPageMarker = true; window.originalWindowOpen = window.open; window.open = () => null; }")
        self.page.locator("#nome").fill("Teste")
        self.page.locator("#email").fill("teste@example.com")
        self.page.locator("#mensagem").fill("Mensagem para testar bloqueio.")
        self.page.locator('button[type="submit"]').click()
        self.assertTrue(self.page.evaluate("window.contactPageMarker"))
        self.assertEqual(self.page.locator("#mensagem").input_value(), "Mensagem para testar bloqueio.")
        link = self.page.locator("#contact-draft")
        self.assertTrue(link.is_visible())
        self.assertIn("Mensagem para testar bloqueio.", parse_qs(urlparse(link.get_attribute("href")).query)["text"][0])
        self.page.evaluate("() => { window.open = window.originalWindowOpen; }")
        self.context.route("https://api.whatsapp.com/**", lambda route: route.fulfill(status=200, content_type="text/html", body="<p>WhatsApp interceptado para teste.</p>"))
        with self.context.expect_page() as popup_info, self.page.expect_navigation(wait_until="load"):
            link.click()
        popup_info.value.wait_for_url("https://api.whatsapp.com/**")
        self.assertEqual(self.page.locator("#mensagem").input_value(), "")

    def test_large_text(self):
        self.page.add_style_tag(content="html { font-size: 200%; }")
        for width in [320, 768, 1024, 1920]:
            self.page.set_viewport_size({"width": width, "height": 900})
            self.assert_layout()

    def test_no_javascript(self):
        context = self.browser.new_context(java_script_enabled=False, viewport={"width": 320, "height": 568})
        context.route("https://**/*", lambda route: route.abort())
        page = context.new_page()
        page.goto(self.url)
        self.assertTrue(page.locator("#menu1").is_visible())
        self.assertTrue(page.locator("#contact-whatsapp").is_visible())
        self.assertTrue(page.locator('button[type="submit"]').is_disabled())
        self.assertFalse(page.locator(".carousel-controls").is_visible())
        self.assertTrue(page.locator("#animation-prog .animation-fallback").is_visible())
        context.close()

    def test_real_animations_and_screenshots(self):
        context = self.browser.new_context(reduced_motion="reduce")
        page = context.new_page()
        page.on("pageerror", lambda error: self.errors.append(str(error)))
        page.goto(self.url)
        page.wait_for_function("document.querySelectorAll('.animation.is-loaded').length === 8", timeout=30000)
        self.assertTrue(page.evaluate("lottie.getRegisteredAnimations().every(animation => animation.isPaused && animation.currentFrame > 0)"))
        page.emulate_media(reduced_motion="no-preference")
        page.wait_for_function("lottie.getRegisteredAnimations().every(animation => !animation.isPaused)")
        page.emulate_media(reduced_motion="reduce")
        page.wait_for_function("lottie.getRegisteredAnimations().every(animation => animation.isPaused)")
        output = os.environ.get("SITE_SCREENSHOT_DIR")
        if output:
            Path(output).mkdir(parents=True, exist_ok=True)
            for width in [390, 768, 1366]:
                page.set_viewport_size({"width": width, "height": 900})
                page.locator(".perfil").scroll_into_view_if_needed()
                page.wait_for_function("document.querySelector('.perfil').complete && document.querySelector('.perfil').naturalWidth > 0")
                page.evaluate("window.scrollTo(0, 0)")
                page.screenshot(path=str(Path(output) / f"site-{width}.png"), full_page=True)
        context.close()


if __name__ == "__main__":
    unittest.main()
