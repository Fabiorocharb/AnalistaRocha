"""Verificações de consistência dos metadados, sitemap e recursos locais."""

from html.parser import HTMLParser
import json
from pathlib import Path
import struct
import unittest
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://fabiorocharb.github.io/AnalistaRocha/"


class PageMetadata(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.json_ld = []
        self.in_json_ld = False
        self.title = ""
        self.in_title = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json_ld = True
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_json_ld = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_json_ld:
            self.json_ld.append(data)
        if self.in_title:
            self.title += data


class SEOTests(unittest.TestCase):
    def setUp(self):
        self.page = PageMetadata((ROOT / "index.html").read_text(encoding="utf-8"))
        self.meta = {attrs.get("name", attrs.get("property")): attrs.get("content")
                     for tag, attrs in self.page.tags if tag == "meta"}

    def test_canonical_and_sitemap_agree(self):
        canonicals = [attrs["href"] for tag, attrs in self.page.tags
                      if tag == "link" and attrs.get("rel") == "canonical"]
        self.assertEqual(canonicals, [BASE_URL])
        sitemap = ET.parse(ROOT / "sitemap.xml")
        locations = [node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(locations, canonicals)
        self.assertEqual(self.meta["og:url"], BASE_URL)
        self.assertNotIn("noindex", self.meta["robots"])
        self.assertNotIn("nofollow", self.meta["robots"])
        self.assertTrue((ROOT / ".nojekyll").is_file())

    def test_metadata_and_structured_data_agree(self):
        self.assertEqual(self.page.title, self.meta["og:title"])
        self.assertEqual(self.page.title, self.meta["twitter:title"])
        self.assertEqual(self.meta["description"], self.meta["og:description"])
        self.assertEqual(self.meta["description"], self.meta["twitter:description"])
        self.assertNotIn("keywords", self.meta)
        self.assertEqual(sum(tag == "h1" for tag, _ in self.page.tags), 1)
        data = json.loads("".join(self.page.json_ld))
        self.assertEqual(data["@context"], "https://schema.org")
        entities = {entity["@id"]: entity for entity in data["@graph"]}
        self.assertEqual(len(entities), len(data["@graph"]))
        webpage = next(entity for entity in entities.values() if entity["@type"] == "WebPage")
        self.assertEqual(webpage["name"], self.page.title)
        self.assertEqual(webpage["description"], self.meta["description"])
        for entity in entities.values():
            self.assertEqual(entity["url"], BASE_URL)
            for value in entity.values():
                if isinstance(value, dict) and "@id" in value:
                    self.assertIn(value["@id"], entities)
        person = next(entity for entity in entities.values() if entity["@type"] == "Person")
        links = {attrs.get("href") for tag, attrs in self.page.tags if tag == "a"}
        self.assertTrue(set(person["sameAs"]).issubset(links))

    def test_social_preview_exists_with_declared_size(self):
        image_url = self.meta["og:image"]
        self.assertEqual(image_url, self.meta["twitter:image"])
        self.assertTrue(image_url.startswith(BASE_URL))
        image = (ROOT / image_url.removeprefix(BASE_URL)).read_bytes()
        self.assertEqual(image[:8], b"\x89PNG\r\n\x1a\n")
        dimensions = struct.unpack(">II", image[16:24])
        self.assertEqual(dimensions, (int(self.meta["og:image:width"]), int(self.meta["og:image:height"])))

    def test_local_resources_and_svg_references_exist(self):
        for tag, attrs in self.page.tags:
            resource = attrs.get("src") if tag in ["img", "script"] else attrs.get("href") if tag == "link" else None
            if resource and not urlparse(resource).scheme:
                self.assertTrue((ROOT / unquote(resource)).is_file(), resource)
        for path in (ROOT / "assets" / "image").glob("*.svg"):
            root = ET.parse(path).getroot()
            identifiers = {node.attrib["id"] for node in root.iter() if "id" in node.attrib}
            for node in root.iter():
                for value in node.attrib.values():
                    if value.startswith("url(#"):
                        self.assertIn(value[5:-1], identifiers, str(path))


if __name__ == "__main__":
    unittest.main()
