# Domain Language

## Board Specification

The user-facing input record. Describes the job the board should do.

Examples:

- rider weight
- skill level
- discipline
- target volume
- foil size
- stance
- intended launch mode

## Board Geometry

The generated shape model.

Examples:

- length
- width
- thickness distribution
- rocker curve
- plan outline
- rail profile
- deck crown
- bottom contour
- foil box position

## Outline Controls

Named controls for the plan-view shape. These are deliberately simpler than CAD
curves and exist so visual tuning has plain language.

Examples:

- tail width
- tail shoulder position
- tail shoulder width
- parallel rail start
- parallel rail end
- nose shoulder position
- nose shoulder width
- nose width

The first generator used anonymous width stations. The current generator uses
these named controls so each design family can be tuned without guessing what a
tuple of numbers means.

## Design Family

A broad style of board, such as:

- beginner wing board
- midlength wing board
- downwind SUP board
- parawing board
- race board

Design families define ranges and relationships, not exact shapes.

## Reference Board

A commercial or custom board used only as a source of public design signals: published dimensions, photographs, reviews, and observed use cases.

Reference boards are not copied into the generated geometry.

## Workshop Output

Files or instructions a builder can use:

- SVG
- DXF
- STL
- STEP
- toolpath setup notes
- blank slicing plan
- insert/foil-box placement template
