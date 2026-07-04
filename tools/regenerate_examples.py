"""Regenerate example SVGs and PNG previews."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

from foil_board_toolkit.geometry import generate_geometry
from foil_board_toolkit.spec import load_board_spec
from foil_board_toolkit.svg import geometry_to_svg


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
GENERATED = EXAMPLES / "generated"
PREVIEWS = GENERATED / "previews"


def main() -> int:
    GENERATED.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)

    for spec_path in sorted(EXAMPLES.glob("*.json")):
        spec = load_board_spec(spec_path)
        geometry = generate_geometry(spec)
        svg_path = GENERATED / f"{spec_path.stem}.svg"
        svg_path.write_text(geometry_to_svg(spec, geometry), encoding="utf-8")
        print(f"wrote {svg_path.relative_to(ROOT)}")

        if shutil.which("convert"):
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
