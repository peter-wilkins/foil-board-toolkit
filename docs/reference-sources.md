# Reference Sources

## Rule

Use reference material to learn design ranges and workflow patterns. Do not
copy commercial board geometry into this repo.

Downloaded pages, cloned reference repos, and third-party design files belong in
the ignored local folder:

```text
references/
```

Only commit:

- source URL
- licence status
- public dimensions
- qualitative design notes
- derived ranges or ratios
- attribution

Do not commit downloaded `.s3dx`, `.brd`, `.stl`, `.obj`, `.dxf`, CAD exports,
or screenshots unless the licence is explicitly compatible with this project.

## Current Local Reference Pack

Collected on 2026-07-04 into ignored local folders:

```text
references/shape3d/
references/repos/boardcad-le/
references/repos/super-shaper-9000/
references/repos/openelectricsurfboard/
references/repos/Surf-Shaper/
```

These files are for local study only. They are not part of the public project.

## Source Ledger

| Source | URL | Licence / rights status | Use in this repo |
| --- | --- | --- | --- |
| Shape3D Warehouse | https://www.shape3d.com/warehouse/Default.aspx?Account=7129 | Public pages with dimensions and downloadable board files. Download availability is not a permissive open-source licence. Some examples mention Shape3D Design Pro requirements. Treat geometry as proprietary/unknown unless a board page says otherwise. | Use public dimensions and qualitative observations only. Do not commit downloaded geometry. |
| BoardCAD LE | https://github.com/HavardNJ/boardcad-le | GitHub licence metadata was absent when checked. Original BoardCAD lineage should be verified before reuse. | Study file concepts, Bezier board modelling, templates, and CNC workflow. Do not copy code or bundled geometry. |
| Super Shaper 9000 | https://github.com/garthtrickett/super-shaper-9000 | AGPL licence in `LICENSE`, with a network-use source-sharing provision. | Study browser-based UX, imports/exports, and shaping workflow. Do not copy code into this Apache repo. |
| Open Electric Surfboard | https://github.com/largeostrich/openelectricsurfboard | CC BY-SA 4.0 according to GitHub metadata and repo `COPYING`. | Potentially reusable with attribution/share-alike handling. Useful for open hardware structure and OpenSCAD workflow, not foil board shape quality. |
| Surf-Shaper | https://github.com/Jurajzovinec/Surf-Shaper | No licence file found in the local clone. | Reference-only. Useful for Onshape/Three.js workflow ideas; do not copy code or assets. |

## Shape3D Candidate Boards

These public pages give useful dimensions and visual references. They are not
licenced as open-source designs.

| Board ID | Name | Public dimensions | Volume | Public category / note | Why useful |
| --- | --- | --- | --- | --- | --- |
| 9281 | Downwind Sup Foil Free | 6' 6" x 17 9/16" x 5 15/16" | 85.9 L | Stand Up Paddle / Foil. Page comments mention beak nose and fish tail created with Free 3D layers and Design Pro/version requirements. | Narrow, lower-volume downwind-style reference. Good antidote to our current over-blobby outline. |
| 10903 | Downwind Sup Foil Tail cut | 6' 6" x 19 3/16" x 5 27/32" | 91.3 L | Stand Up Paddle / Foil. | Similar length/volume to 9281 but wider. Useful for comparing width sensitivity. |
| 9666 | Downwind Sup Foil 77 | 7' 7" x 22 1/2" x 6 5/8" | 148.5 L | Stand Up Paddle / Foil. Page note says no 3D layers except recessed deck. | Larger downwind/SUP reference; useful for high-volume range. |
| 14067 | Downwind Sup Foil 80 Foil Tracks Box | 8' 0" x 22" x 6" | 137.8 L | Stand Up Paddle / Foil. Page comments mention foil track box and Design Pro/version requirements. | Long, relatively narrow downwind reference with track-box thinking. |
| 8732 | Wing foil board 4_6 50L | 4' 6" x 21 1/4" x 4 5/32" | 50.0 L | Foil Board / Free Ride. Page comments mention flat-to-double-concave bottom via 3D layer. | Compact wing board reference; useful for short-board outline proportions. |
| 8645 | Wing foil board | 5' 2" x 27 25/32" x 4 1/8" | 82.1 L | Foil Board / Free Ride. Page comments mention flat-to-double-concave bottom via 3D layer. | Higher-volume wing freeride reference. Highlights how much width grows with stability. |
| 12687 | Wing Flat Rail | 6' 0" x 23 25/32" x 6 1/16" | 113.9 L | Foil Board / Free Ride. Page comments say inspired by Neyrafoil and mention Design Pro requirements. | Midlength wing reference with flat rail/cut rail idea. |
| 8648 | SUP FOIL VStep | 6' 10 1/8" x 29" x 4 7/16" | 122.3 L | Stand Up Paddle / Foil. Page comments mention Tail V Step. | Wide SUP foil reference; useful for beginner/stability end of the range. |
| 14598 | Pump foil | 40" x 16" x 1 19/32" | 13.0 L | Foil / Pump. | Tiny pump-board outlier; useful as a separate family, not part of normal wing/downwind scaling. |
| 14616 | Wind Foil Double cut outs Free | 7' 21/32" x 35 23/32" x 5 3/4" | 193.4 L | Wind / Foil. Page comments mention double cut-outs made with Free layers. | Very wide/high-volume wind foil outlier; useful only to keep discipline families separate. |

## Early Design Lessons

- The current generated example is too blobby because it does not model real
  design families. A downwind board, compact wing board, SUP foil board, and pump
  board should not share one generic outline equation.
- Width is the fastest visual credibility signal. A 6'6" downwind board can be
  around 17.5-19.2" wide, while freeride/SUP boards can be much wider.
- The generator needs named outline controls: tail block width, max-width
  station, shoulder width, nose width, parallel midsection, and nose/tail
  roundness.
- Rocker should be split into design controls: tail rocker, flat carry section,
  nose rocker start, nose kick, and curve type.
- Bottom features and deck features should be represented as optional design
  features, not baked into the base outline.
- Each design family needs its own sane parameter range and visual tests.

## Next Reference Work

1. Convert the Shape3D candidate table into derived ratios.
2. Create one JSON preset per design family:
   - downwind SUP
   - midlength wing
   - compact wing
   - beginner SUP foil
   - pump board
3. Generate a gallery of variants per family.
4. Visually reject silly shapes before adding more CAD complexity.
