"use strict";

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const desktop = window.matchMedia("(min-width: 1024px)");
const menu = document.getElementById("menu");
const btnMobile = document.getElementById("btn-mobile");

function setMenuOpen(open) {
  menu.classList.toggle("active", open);
  btnMobile.setAttribute("aria-expanded", String(open));
  btnMobile.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
}

btnMobile.addEventListener("click", () => {
  setMenuOpen(!menu.classList.contains("active"));
});
menu.addEventListener("click", (event) => {
  const link = event.target.closest("a");
  if (!link) return;
  setMenuOpen(false);
  const href = link.getAttribute("href");
  if (href.startsWith("#")) {
    const target = document.getElementById(href.slice(1));
    if (target) {
      target.setAttribute("tabindex", "-1");
      target.focus({ preventScroll: true });
    }
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menu.classList.contains("active")) {
    setMenuOpen(false);
    btnMobile.focus();
  }
});
document.addEventListener("click", (event) => {
  if (!menu.contains(event.target)) setMenuOpen(false);
});
document.addEventListener("focusin", (event) => {
  if (!menu.contains(event.target)) setMenuOpen(false);
});
desktop.addEventListener("change", () => {
  const focusWasInMenu = menu.contains(document.activeElement);
  setMenuOpen(false);
  if (focusWasInMenu) {
    (desktop.matches ? menu.querySelector("a") : btnMobile).focus();
  }
});
menu.classList.add("enhanced");

// Uma única implementação, independente de CDN, para todas as larguras.
const carousel = document.querySelector(".carousel");
const slides = Array.from(carousel.querySelectorAll(".project"));
const navigation = document.querySelector(".carousel-navigation");
const carouselStatus = document.getElementById("carousel-status");
let activeSlide = 0;

const dots = slides.map((slide, index) => {
  const dot = document.createElement("button");
  dot.type = "button";
  dot.className = "dot";
  dot.setAttribute("aria-label", `Ver projeto ${index + 1}: ${slide.querySelector(".working").textContent}`);
  dot.setAttribute("aria-controls", "projects-carousel");
  dot.addEventListener("click", () => goToSlide(index));
  navigation.append(dot);
  return dot;
});

function updateSlide(index) {
  activeSlide = index;
  dots.forEach((dot, dotIndex) => {
    dot.classList.toggle("active", dotIndex === index);
    if (dotIndex === index) dot.setAttribute("aria-current", "true");
    else dot.removeAttribute("aria-current");
  });
  const status = `Projeto ${index + 1} de ${slides.length}: ${slides[index].querySelector(".working").textContent}`;
  if (carouselStatus.textContent !== status) carouselStatus.textContent = status;
}

function goToSlide(index) {
  const nextIndex = (index + slides.length) % slides.length;
  const left = carousel.scrollLeft + slides[nextIndex].getBoundingClientRect().left - carousel.getBoundingClientRect().left;
  carousel.scrollTo({ left, behavior: reducedMotion.matches ? "auto" : "smooth" });
}

let scrollFrame = 0;
carousel.addEventListener("scroll", () => {
  cancelAnimationFrame(scrollFrame);
  scrollFrame = requestAnimationFrame(() => {
    const left = carousel.getBoundingClientRect().left;
    let nearest = 0;
    slides.forEach((slide, index) => {
      if (Math.abs(slide.getBoundingClientRect().left - left) < Math.abs(slides[nearest].getBoundingClientRect().left - left)) nearest = index;
    });
    updateSlide(nearest);
  });
}, { passive: true });
document.querySelector(".carousel-prev").addEventListener("click", () => goToSlide(activeSlide - 1));
document.querySelector(".carousel-next").addEventListener("click", () => goToSlide(activeSlide + 1));
carousel.addEventListener("keydown", (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey) return;
  const destinations = { ArrowLeft: activeSlide - 1, ArrowRight: activeSlide + 1, Home: 0, End: slides.length - 1 };
  if (Object.hasOwn(destinations, event.key)) {
    event.preventDefault();
    // Mantém o foco no carrossel, sem deixar um link focado fora da tela.
    carousel.focus({ preventScroll: true });
    goToSlide(destinations[event.key]);
  }
});
carousel.addEventListener("focusin", (event) => {
  const slide = event.target.closest(".project");
  if (slide) goToSlide(slides.indexOf(slide));
});
updateSlide(0);
document.querySelector(".carousel-controls").hidden = false;

document.getElementById("copyright-year").textContent = new Date().getFullYear();

const contactForm = document.getElementById("contact-form");
const contactFields = ["nome", "email", "mensagem"].map((id) => document.getElementById(id));
const draftLink = document.getElementById("contact-draft");

function continueInWhatsApp(url) {
  // Abre primeiro uma janela vazia para detectar bloqueios antes de limpar os campos.
  const whatsappWindow = window.open("about:blank", "_blank");
  if (!whatsappWindow) return;
  whatsappWindow.opener = null;
  const whatsappLink = whatsappWindow.document.createElement("a");
  whatsappLink.href = url;
  whatsappLink.rel = "noopener noreferrer";
  whatsappWindow.document.body.append(whatsappLink);
  whatsappLink.click();
  contactForm.reset();
  window.location.reload();
}

draftLink.addEventListener("click", (event) => {
  event.preventDefault();
  continueInWhatsApp(draftLink.href);
});

contactFields.forEach((field) => {
  field.addEventListener("input", () => field.setCustomValidity(""));
});
contactForm.addEventListener("submit", (event) => {
  event.preventDefault();
  contactFields.forEach((field) => {
    field.setCustomValidity(field.value.trim() ? "" : "Preencha este campo.");
  });
  if (!contactForm.reportValidity()) return;
  const [name, email, message] = contactFields.map((field) => field.value.trim());
  const url = new URL(document.getElementById("contact-whatsapp").href);
  url.searchParams.set("text", `Olá! Me chamo ${name}.\nEmail: ${email}\n\n${message}`);
  draftLink.href = url.href;
  draftLink.hidden = false;
  document.getElementById("contact-status").textContent = "Mensagem preparada. Continue no WhatsApp para revisar e enviar. Se a janela não abrir, use o link abaixo.";
  continueInWhatsApp(url.href);
});
contactForm.querySelector('[type="submit"]').disabled = false;

// As animações são decorativas: uma falha não interrompe os controles do site.
const animationFiles = {
  "animation-prog": "programer",
  "animation-seta": "seta",
  "animation-seo": "seo",
  "animation-responsible": "responsible",
  "animation-uxui": "uiux",
  setatwo: "seta",
  setasix: "seta",
  setaseven: "seta",
};
function initializeAnimations() {
  if (!window.lottie || typeof window.lottie.loadAnimation !== "function") return;
  Object.entries(animationFiles).forEach(([id, file]) => {
    const container = document.getElementById(id);
    try {
      const animation = window.lottie.loadAnimation({
        container,
        renderer: "svg",
        loop: true,
        autoplay: !reducedMotion.matches,
        path: `assets/image/${file}.json`,
      });
      const syncMotion = () => {
        // Algumas animações começam vazias; usa um quadro intermediário como ilustração.
        if (reducedMotion.matches) animation.goToAndStop(Math.floor(animation.totalFrames / 2), true);
        else animation.play();
      };
      animation.addEventListener("DOMLoaded", () => {
        container.classList.add("is-loaded");
        syncMotion();
      });
      reducedMotion.addEventListener("change", syncMotion);
    } catch (error) {
      console.warn(`Não foi possível carregar a animação ${file}.`, error);
    }
  });
}
if (window.lottie) initializeAnimations();
else document.getElementById("lottie-script").addEventListener("load", initializeAnimations, { once: true });
