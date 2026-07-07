"""Regenerate example SVGs, reports, and the fast visual-review gallery."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import shutil
import subprocess

from foil_board_toolkit.geometry import generate_geometry
from foil_board_toolkit.report import geometry_report_to_json
from foil_board_toolkit.spec import load_board_spec
from foil_board_toolkit.svg import geometry_to_svg


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
GENERATED = EXAMPLES / "generated"
PREVIEWS = GENERATED / "previews"
GALLERY = GENERATED / "index.html"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--png", action="store_true", help="Also regenerate slow PNG previews for README use")
    args = parser.parse_args(argv)

    GENERATED.mkdir(parents=True, exist_ok=True)
    if args.png:
        PREVIEWS.mkdir(parents=True, exist_ok=True)

    gallery_items = []
    for spec_path in sorted(EXAMPLES.glob("*.json")):
        spec = load_board_spec(spec_path)
        geometry = generate_geometry(spec)
        svg_path = GENERATED / f"{spec_path.stem}.svg"
        svg_path.write_text(geometry_to_svg(spec, geometry), encoding="utf-8")
        print(f"wrote {svg_path.relative_to(ROOT)}")

        report_path = GENERATED / f"{spec_path.stem}.report.json"
        report_path.write_text(geometry_report_to_json(spec, geometry), encoding="utf-8")
        print(f"wrote {report_path.relative_to(ROOT)}")
        gallery_items.append((spec.name, svg_path, report_path, geometry))

        if args.png and shutil.which("convert"):
            png_path = PREVIEWS / f"{spec_path.stem}.png"
            subprocess.run(
                [
                    "convert",
                    "-background",
                    "white",
                    "-density",
                    "110",
                    str(svg_path),
                    "-resize",
                    "1100x",
                    str(png_path),
                ],
                check=True,
            )
            print(f"wrote {png_path.relative_to(ROOT)}")
        elif args.png:
            print("skipped PNG preview generation: ImageMagick convert not found")

    GALLERY.write_text(_gallery_html(gallery_items), encoding="utf-8")
    print(f"wrote {GALLERY.relative_to(ROOT)}")

    return 0


def _gallery_html(gallery_items) -> str:
    cards = "\n".join(
        f"""      <article class="card">
        <header>
          <h2>{escape(name)}</h2>
          <p>{geometry.length_mm:.0f} x {geometry.max_width_mm:.0f} x {geometry.max_thickness_mm:.0f} mm · {geometry.volume_estimate_l:.1f} L · stock {geometry.stock_length_mm:.0f} x {geometry.stock_width_mm:.0f} x {geometry.stock_thickness_mm:.0f} mm</p>
        </header>
        <img src="{svg_path.name}" alt="{escape(name)} generated SVG template">
        <p><a href="{svg_path.name}">SVG</a> · <a href="{report_path.name}">geometry report</a></p>
      </article>"""
        for name, svg_path, report_path, geometry in gallery_items
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Foil Board Toolkit generated examples</title>
    <style>
      body {{ margin: 0; font-family: system-ui, sans-serif; color: #172326; background: #fbfaf6; }}
      main {{ max-width: 1440px; margin: 0 auto; padding: clamp(16px, 4vw, 32px); }}
      h1 {{ margin: 0 0 8px; font-size: 32px; }}
      .intro {{ margin: 0 0 24px; color: #4d5b60; }}
      .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 420px), 1fr)); gap: 24px; }}
      .card {{ border: 1px solid #ccd8d6; border-radius: 6px; padding: 16px; background: white; }}
      h2 {{ margin: 0; font-size: 20px; }}
      p {{ margin: 6px 0 0; }}
      img {{ display: block; width: 100%; height: auto; margin-top: 14px; border: 1px solid #edf0ef; }}
      a {{ color: #005b70; }}
    </style>
  </head>
  <body>
    <main>
      <h1>Foil Board Toolkit generated examples</h1>
      <p class="intro">Fast visual review gallery. These are reference-informed original heuristics, not build-ready board designs.</p>
      <section class="grid">
{cards}
      </section>
    </main>
  </body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
