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
station sampling, stance guides, a generic foil-track envelope, and a first
station-based volume model.

| Example | Current rating | What looks better | Still wrong / next tuning |
| --- | --- | --- | --- |
| `downwind-sup-86l` | Better | Reads as a distinct downwind family: high length/width ratio, pulled-in tail, softer forward shoulder, and less symmetric nose/tail language. The 165 mm thickness is now produced by explicit volume stations. | Side profile implies a 320 mm blank height once nose rocker is included. That needs workshop proof before any CNC promise. |
| `compact-wing-50l` | Better | Short, square, and visibly separate from downwind. Tail block and nose are less generic, and the side view now shows a deck/bottom band. | Still needs real compact-wing tail language and rail hard-edge/cut-rail controls before workshop use. |
| `midlength-wing-85l` | Better | Cleaner midlength proportions with a more deliberate tail, finer outline sampling, and a measured 154 mm max-thickness station. | Deck, rail, and bottom controls are still family constants, not user-tunable design inputs. |
| `midlength-wing-114l` | Better | Larger midlength separates from compact wing and preserves a useful parallel standing section. | Rails are still too idealised. Add rail-break / shoulder controls later. |
| `beginner-sup-foil-122l` | Better | Wide stable platform now has a squarer tail, rounder nose language, and a visible deck/bottom side profile. | Current SVG cannot express deck recess, carry handle, inserts, or sandwich/laminate structure. |
| `pump-13l` | Better | Tiny, square board now has stronger pump-board proportions and visible stance/track/volume guides. | Needs pump-specific stance and foil-track rules; current 320 mm envelope may be too generic. |
| `wind-foil-193l` | Maybe | Huge, wide, and separate from everything else; denser sampling makes it less faceted. | Low priority. Do not tune until wind foil becomes a real target. |

## Next Design Control To Add

The generator now has separate curve sharpness controls and a simple 3D-ish
station model for volume distribution. The next useful control is to make those
volume features user-visible and workshop-checkable:

- expose deck crown / recess as explicit controls
- expose rail fullness and hard-edge/cut-rail controls
- turn bottom contour placeholders into named family options
- add foil-track and stance rules by design family
- export a machine-readable geometry report beside each SVG

Do not move to CNC claims until a generated 3D blank can be measured for
bounding box, volume, track placement, minimum thickness, stock envelope, and
router capacity.
