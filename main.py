#!/usr/bin/env python3
"""An abstract Image class per file type, plus an HTML gallery builder."""
import argparse
import base64
import io
import os
import tempfile
from abc import ABC, abstractmethod

try:
    from PIL import Image as PILImage
    from PIL import ImageDraw
except ImportError:  # pragma: no cover
    PILImage = None

class Image(ABC):
    """Common interface for gallery images."""
    extensions = ()

    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise ValueError(f"not a file: {path}")
        self.path = path
        self._pil = None

    @property
    @abstractmethod
    def kind(self) -> str: ...

    def _open(self):
        if PILImage is None:
            raise RuntimeError("Pillow is required for image metadata (pip install pillow)")
        if self._pil is None:
            self._pil = PILImage.open(self.path)
        return self._pil

    @property
    def size(self):
        return self._open().size

    @property
    def mode(self):
        return self._open().mode

    def thumbnail_data_uri(self, box=(160, 120)) -> str:
        image = self._open().convert("RGB")
        image.thumbnail(box)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=80)
        return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()

    def __str__(self):
        width, height = self.size
        return f"{self.kind:<6} {os.path.basename(self.path):<24} {width:>4}x{height:<4} {self.mode}"

class PngImage(Image):
    kind = "PNG"

class JpgImage(Image):
    kind = "JPEG"

class GifImage(Image):
    kind = "GIF"

TYPES = {".png": PngImage, ".jpg": JpgImage, ".jpeg": JpgImage, ".gif": GifImage}

class Gallery:
    def __init__(self, title="Image Gallery"):
        self.title = title
        self.images = []

    def add(self, path: str) -> Image:
        extension = os.path.splitext(path)[1].lower()
        if extension not in TYPES:
            raise ValueError(f"unsupported image type '{extension}'")
        image = TYPES[extension](path)
        self.images.append(image)
        return image

    def add_directory(self, directory: str) -> int:
        added = 0
        for name in sorted(os.listdir(directory)):
            if os.path.splitext(name)[1].lower() in TYPES:
                self.add(os.path.join(directory, name))
                added += 1
        return added

    def to_html(self, output: str) -> str:
        cards = "\n".join(
            f'<figure><img src="{image.thumbnail_data_uri()}" alt="{os.path.basename(image.path)}">'
            f'<figcaption>{os.path.basename(image.path)}<br><small>{image.kind} '
            f'{image.size[0]}x{image.size[1]}</small></figcaption></figure>'
            for image in self.images)
        html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{self.title}</title>
<style>
body {{ font-family: system-ui, sans-serif; background: #111; color: #eee; margin: 2rem; }}
.gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1rem; }}
figure {{ margin: 0; background: #1d1d1d; border-radius: 8px; overflow: hidden; }}
img {{ width: 100%; display: block; }}
figcaption {{ padding: .5rem; font-size: .85rem; }}
</style></head><body><h1>{self.title}</h1><div class="gallery">
{cards}
</div></body></html>"""
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(html)
        return output

def demo() -> None:
    if PILImage is None:
        print("Pillow is not installed; install it with: pip install pillow")
        return
    with tempfile.TemporaryDirectory() as tmp:
        colours = [("sunset.png", (240, 120, 60)), ("ocean.jpg", (30, 90, 170)),
                   ("forest.gif", (40, 130, 70))]
        for name, colour in colours:
            image = PILImage.new("RGB", (320, 240), colour)
            draw = ImageDraw.Draw(image)
            draw.text((20, 20), name, fill="white")
            image.save(os.path.join(tmp, name))
        gallery = Gallery("Demo Gallery")
        count = gallery.add_directory(tmp)
        print(f"indexed {count} images")
        for image in gallery.images:
            print(image)
        output = os.path.join(tmp, "gallery.html")
        gallery.to_html(output)
        html = open(output).read()
        print(f"html written: {os.path.getsize(output)} bytes, "
              f"embedded thumbnails: {html.count('data:image/jpeg;base64,')}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", help="directory of images")
    parser.add_argument("--output", default="gallery.html")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.dir:
        demo()
        return
    gallery = Gallery(os.path.basename(os.path.abspath(args.dir)))
    gallery.add_directory(args.dir)
    for image in gallery.images:
        print(image)
    print("gallery:", gallery.to_html(args.output))

if __name__ == "__main__":
    main()
