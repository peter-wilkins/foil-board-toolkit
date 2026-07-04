# Visual Review Loop

The gallery is a design-review tool, not proof that a board will ride well.
The aim is to kill obviously silly shapes early and keep tuning the family
presets before adding 3D CAD complexity.

Regenerate the examples after changing geometry code:

```bash
PYTHONPATH=src python3 tools/regenerate_examples.py
```

Then review the PNG gallery in the README and update this table.

## Review Criteria

- **Outline credibility:** does the plan shape look like the intended family?
- **Family separation:** does it clearly differ from the other families?
- **Nose/tail intent:** do nose and tail widths look deliberate?
- **Parallel rail section:** is the useful standing/paddling section visible?
- **Rocker credibility:** does the profile look less like a cartoon ramp?

## Current Review

| Example | Current rating | What looks better | Still wrong / next tuning |
| --- | --- | --- | --- |
| `downwind-sup-86l` | Maybe | Narrower and longer than the first generic SVG. It now reads more like a downwind family. | Tail and nose are still too symmetrical. Needs a more deliberate pulled-in tail and softer nose transition. |
| `compact-wing-50l` | Maybe | Short, square, and clearly different from downwind. | Needs more realistic compact-wing tail language and less rectangular bulk through the middle. |
| `midlength-wing-85l` | Maybe | Less like the first generic blob; rails have more intent. | Still too generic. Needs clearer midlength nose and tail proportions. |
| `midlength-wing-114l` | Maybe | Larger midlength now separates from compact wing. | Rails still too smooth. Add rail-break / shoulder controls later. |
| `beginner-sup-foil-122l` | Maybe | Correctly reads as a wide, stable platform. | Nose/tail need more board-like shaping; currently very schematic. |
| `pump-13l` | Maybe | Correctly tiny and square. | Needs specific pump-board stance/foil-box geometry; current outline is just a family placeholder. |
| `wind-foil-193l` | Maybe | Huge, wide, and separate from everything else. | Low priority for now; do not tune until wind foil becomes a real target. |

## Next Design Control To Add

Add separate nose and tail curve sharpness controls. The current model controls
width stations, but every transition uses the same smoothstep easing. Real
families need different curve character:

- hard square tail vs rounded pintail
- beak nose vs round nose
- parallel rail length
- shoulder softness
- nose/tail asymmetry
