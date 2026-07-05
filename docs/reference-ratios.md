# Reference Ratios

These ratios come from public dimensions recorded in
[`reference-sources.md`](reference-sources.md). They are used to shape broad
design-family ranges, not to clone any board.

## Public Reference Dimensions

| Source | Family | Length mm | Width mm | Thickness mm | Volume L | Length / width | Length mm / L | Width mm / L |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Shape3D 9281 | downwind SUP | 1981 | 446 | 151 | 85.9 | 4.44 | 23.1 | 5.2 |
| Shape3D 10903 | downwind SUP | 1981 | 487 | 148 | 91.3 | 4.07 | 21.7 | 5.3 |
| Shape3D 9666 | downwind SUP | 2311 | 572 | 168 | 148.5 | 4.04 | 15.6 | 3.8 |
| Shape3D 14067 | downwind SUP | 2438 | 559 | 152 | 137.8 | 4.36 | 17.7 | 4.1 |
| Shape3D 8732 | compact wing | 1372 | 540 | 106 | 50.0 | 2.54 | 27.4 | 10.8 |
| Shape3D 8645 | wing freeride | 1575 | 706 | 105 | 82.1 | 2.23 | 19.2 | 8.6 |
| Shape3D 12687 | midlength wing | 1829 | 604 | 154 | 113.9 | 3.03 | 16.1 | 5.3 |
| Shape3D 8648 | beginner SUP foil | 2086 | 737 | 113 | 122.3 | 2.83 | 17.1 | 6.0 |
| Shape3D 14598 | pump | 1016 | 406 | 40 | 13.0 | 2.50 | 78.2 | 31.3 |
| Shape3D 14616 | wind foil | 2150 | 907 | 146 | 193.4 | 2.37 | 11.1 | 4.7 |

## Generated Example Dimensions

| Example | Family | Generated dimensions | Volume | Length / width |
| --- | --- | ---: | ---: | ---: |
| `downwind-sup-86l` | downwind SUP | 1930 x 461 x 165 mm | 86.0 L | 4.18 |
| `compact-wing-50l` | compact wing | 1362 x 537 x 108 mm | 50.0 L | 2.54 |
| `midlength-wing-85l` | wing | 1743 x 555 x 154 mm | 85.0 L | 3.14 |
| `midlength-wing-114l` | midlength wing | 1840 x 605 x 166 mm | 114.0 L | 3.04 |
| `beginner-sup-foil-122l` | beginner SUP foil | 2087 x 737 x 120 mm | 122.0 L | 2.83 |
| `pump-13l` | pump | 1008 x 403 x 47 mm | 13.0 L | 2.50 |
| `wind-foil-193l` | wind foil | 2152 x 909 x 148 mm | 193.0 L | 2.37 |

## Design Notes

- Downwind boards need a visibly high length/width ratio. A 6'6" board around
  17.5-19.2" wide looks like a different species from a freeride wing board.
- Compact wing and pump boards can be short without looking wrong, but they need
  a squarer outline language.
- Beginner SUP foil and wind foil are wide-platform families. They should not
  share the narrow downwind outline model.
- The first SVG generator was funny because one generic control curve tried to
  cover every family. The current generator uses per-family outline controls and
  per-segment curve sharpness as a minimum next step.
- Thickness now comes from a station-based volume model with explicit deck
  crown, rail thickness, and bottom-contour placeholders. The numbers are useful
  for comparison, but still not a validated 3D CAD shape.
- These examples are visual calibration artifacts. They are still not proven
  rideable board designs.
