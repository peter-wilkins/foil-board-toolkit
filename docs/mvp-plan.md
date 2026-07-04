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

Output: SVG or DXF templates.

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

