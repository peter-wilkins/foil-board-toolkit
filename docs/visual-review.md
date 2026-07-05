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

Updated 2026-07-05 after adding per-segment outline curve controls, denser
station sampling, stance guides, and a generic foil-track envelope.

| Example | Current rating | What looks better | Still wrong / next tuning |
| --- | --- | --- | --- |
| `downwind-sup-86l` | Better | Reads as a distinct downwind family: high length/width ratio, pulled-in tail, softer forward shoulder, and less symmetric nose/tail language. Thickness now stays closer to the public-reference range after width-normalised volume solving. | Still needs a better 3D volume model before treating the 171 mm thickness estimate as real. |
| `compact-wing-50l` | Better | Short, square, and visibly separate from downwind. Tail block and nose are less generic. | Still needs real compact-wing tail language and rail hard-edge/cut-rail controls before workshop use. |
| `midlength-wing-85l` | Better | Cleaner midlength proportions with a more deliberate tail and finer outline sampling. | Still looks like a smooth template, not a shaped board. Needs deck/rail/bottom controls. |
| `midlength-wing-114l` | Better | Larger midlength separates from compact wing and preserves a useful parallel standing section. | Rails are still too idealised. Add rail-break / shoulder controls later. |
| `beginner-sup-foil-122l` | Better | Wide stable platform now has a squarer tail and rounder nose language. | Current SVG cannot express deck recess, rail volume, or carry handle/inserts. |
| `pump-13l` | Better | Tiny, square board now has stronger pump-board proportions and visible stance/track guides. | Needs pump-specific stance and foil-track rules; current 320 mm envelope may be too generic. |
| `wind-foil-193l` | Maybe | Huge, wide, and separate from everything else; denser sampling makes it less faceted. | Low priority. Do not tune until wind foil becomes a real target. |

## Next Design Control To Add

The generator now has separate curve sharpness controls for tail, tail-to-mid,
nose-to-mid, and nose transitions. The next useful control is not more 2D
smoothing; it is simple 3D volume distribution:

- thickness stations tied to the plan outline
- deck crown / recess as explicit controls
- rail fullness and hard-edge/cut-rail controls
- bottom contour placeholders, even if only flat / vee / concave labels at first
- foil-track and stance rules by design family

Do not move to CNC claims until the 3D blank model can be measured for bounding
box, volume, track placement, minimum thickness, and stock envelope.
