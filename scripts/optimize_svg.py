"""Remove somente imagens embutidas em <defs> que não são referenciadas.

Não comprime pixels nem modifica formas, máscaras, proporções ou cores.
Execute: python scripts/optimize_svg.py
"""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def optimize_svg(source):
    # Limita a otimização às definições sem uso, preservando o XML restante.
    def prune_definitions(match):
        def prune_image(image_match):
            image = image_match.group(0)
            identifier = re.search(r'\bid="([^"]+)"', image)
            if not identifier or "data:image/" not in image:
                return image
            referenced = re.search(r"#" + re.escape(identifier.group(1)) + r"(?=[\s\"')])", source)
            return image if referenced else ""

        return re.sub(r"<image\b[^>]*?/>", prune_image, match.group(0))

    result = re.sub(r"<defs\b[^>]*>.*?</defs>", prune_definitions, source, flags=re.DOTALL)
    ET.fromstring(result)
    return result


if __name__ == "__main__":
    total_before = total_after = 0
    for path in sorted((ROOT / "assets" / "image").glob("*.svg")):
        original = path.read_bytes()
        optimized = optimize_svg(original.decode("utf-8")).encode("utf-8")
        if optimized != original:
            path.write_bytes(optimized)
        total_before += len(original)
        total_after += len(optimized)
        print(f"{path.name}: {len(original):,} -> {len(optimized):,} bytes")
    print(f"Total: {total_before:,} -> {total_after:,} bytes ({(1 - total_after / total_before) * 100:.1f}% menor)")
