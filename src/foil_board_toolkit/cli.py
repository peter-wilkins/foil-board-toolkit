"""Command line entry points."""

from __future__ import annotations

import argparse
from pathlib import Path

from .geometry import generate_geometry
from .report import geometry_report_to_json
from .spec import load_board_spec
from .svg import geometry_to_svg


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="foil-board-toolkit")
    subcommands = parser.add_subparsers(dest="command", required=True)

    generate = subcommands.add_parser("generate", help="Generate a board template SVG")
    generate.add_argument("spec_json", help="Path to a board spec JSON file")
    generate.add_argument("--out", required=True, help="Output SVG path")
    generate.add_argument("--report-out", help="Optional output path for a geometry report JSON")

    args = parser.parse_args(argv)
    if args.command == "generate":
        spec = load_board_spec(args.spec_json)
        geometry = generate_geometry(spec)
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(geometry_to_svg(spec, geometry), encoding="utf-8")
        print(f"wrote {output_path}")
        if args.report_out:
            report_path = Path(args.report_out)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(geometry_report_to_json(spec, geometry), encoding="utf-8")
            print(f"wrote {report_path}")
        return 0
    raise AssertionError(f"unhandled command {args.command}")
