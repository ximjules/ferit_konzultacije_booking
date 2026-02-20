"""
Usage:
  pip install pillow
  python tools/make_favicon.py path/to/logo.png
Produces: static/images/favicon.ico
"""
import sys
from pathlib import Path
from PIL import Image

def make_favicon(src_path):
    src = Path(src_path)
    out_dir = Path(__file__).resolve().parents[2] / "static" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "favicon.ico"
    img = Image.open(src).convert("RGBA")
    sizes = [(64,64),(48,48),(32,32),(16,16)]
    icons = [img.resize(s, Image.LANCZOS) for s in sizes]
    icons[0].save(out, format='ICO', sizes=sizes)
    print(f"Saved favicon to: {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide source PNG file path.")
    else:
        make_favicon(sys.argv[1])
