# Agent Instructions

## Role

Build an open-source foil board design toolkit without copying protected board designs.

## Working Rules

- Keep the repo clean; check `git status -sb` before implementation.
- Prefer small, tested slices over big CAD fantasies.
- Do not scrape, download, or republish proprietary board geometry.
- Public board dimensions and photographs may be used for trend analysis, but keep attribution and source notes.
- The generator must produce original parameterised designs.
- Complexity requires proof: add CFD, CAM, optimisation, lattice cores, or full CAD only after a smaller feedback loop demonstrates value.
- Treat generated boards as experimental and safety-sensitive.

## Current Focus

First prove a tiny loop:

1. Accept a board specification.
2. Generate simple outline/profile geometry.
3. Export a human-checkable template.
4. Test the geometry and rough volume estimates.

