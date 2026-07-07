# MVP Plan

## Slice 1: Board Spec Schema

Create a small machine-readable board specification:

- rider weight
- discipline
- target volume
- skill level
- foil size
- stance

Output: validated JSON examples.

## Slice 2: 2D Generator

Generate:

- top outline
- side rocker/profile
- station widths
- rough volume estimate

Output: SVG templates, report JSON, and a fast HTML review gallery.

Current first pass:

- `examples/midlength-wing-85l.json` defines a board spec.
- `python3 -m foil_board_toolkit generate ...` exports an SVG template and can
  also write a geometry report JSON with `--report-out`.
- The generated shape includes a top outline, side rocker, foil box guide,
  stance guide, rough volume estimate, stock envelope, and station-based
  volume measurements.
- `tools/regenerate_examples.py` regenerates SVGs, report JSON files, and the
  fast HTML gallery for visual review.
- `tools/regenerate_examples.py --png` refreshes slow static PNG thumbnails
  only when README assets need updating.

## Slice 3: Feedback Loop

Add tests for:

- no negative dimensions
- volume estimate close to target
- foil box remains inside useful stance range
- generated outline is smooth enough for cutting templates

## Slice 4: First Workshop Artifact

Export a real printable/checkable board template for Peter to inspect.

## Later Slices

- 3D mesh preview
- STEP export
- sliced blank generation for CNC depth limits
- foil-box/inserts generation
- internal pocketing and structure
- CFD and optimisation experiments
