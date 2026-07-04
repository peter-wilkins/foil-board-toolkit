"""SVG export for quick visual feedback."""

from __future__ import annotations

from html import escape

from .geometry import BoardGeometry, Point
from .spec import BoardSpec


def geometry_to_svg(spec: BoardSpec, geometry: BoardGeometry) -> str:
    margin = 90
    plan_height = geometry.max_width_mm + margin * 2
    profile_top = plan_height + 170
    profile_height = 360
    profile_vertical_scale = 2.4
    width = geometry.length_mm + margin * 2
    height = profile_top + profile_height + margin

    plan_points = _points_to_svg(
        [Point(point.x_mm + margin, point.y_mm + margin + geometry.max_width_mm / 2) for point in geometry.outline_points]
    )
    rocker_points = _points_to_svg(
        [
            Point(point.x_mm + margin, profile_top + profile_height - point.y_mm * profile_vertical_scale)
            for point in geometry.rocker_points
        ]
    )
    rocker_band_points = _points_to_svg(
        [
            Point(point.x_mm + margin, profile_top + profile_height - point.y_mm * profile_vertical_scale)
            for point in geometry.rocker_points
        ]
        + [
            Point(geometry.rocker_points[-1].x_mm + margin, profile_top + profile_height),
            Point(margin, profile_top + profile_height),
        ]
    )
    baseline_y = profile_top + profile_height
    foil_x = margin + geometry.foil_box_center_from_tail_mm
    stance_x = margin + geometry.stance_center_from_tail_mm

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}mm" height="{height:.0f}mm" viewBox="0 0 {width:.0f} {height:.0f}">
  <title>{escape(spec.name)} foil board template</title>
  <style>
    text {{ font-family: system-ui, sans-serif; fill: #263238; }}
    .small {{ font-size: 24px; }}
    .label {{ font-size: 30px; font-weight: 650; }}
    .outline {{ fill: #e7f3f1; stroke: #123c46; stroke-width: 4; }}
    .rocker-band {{ fill: #d5eee9; stroke: none; }}
    .rocker {{ fill: none; stroke: #004f63; stroke-width: 8; }}
    .guide {{ stroke: #d05d2d; stroke-width: 3; stroke-dasharray: 12 10; }}
    .baseline {{ stroke: #546e7a; stroke-width: 2; }}
  </style>
  <rect width="100%" height="100%" fill="#fbfaf6"/>
  <text x="{margin}" y="48" class="label">Foil Board Toolkit: {escape(spec.name)}</text>
  <text x="{margin}" y="84" class="small">Plan outline: {geometry.length_mm:.0f} mm x {geometry.max_width_mm:.0f} mm. Estimated volume: {geometry.volume_estimate_l:.1f} L.</text>

  <polygon class="outline" points="{plan_points}"/>
  <line class="guide" x1="{foil_x:.1f}" y1="{margin}" x2="{foil_x:.1f}" y2="{margin + geometry.max_width_mm:.1f}"/>
  <line class="guide" x1="{stance_x:.1f}" y1="{margin}" x2="{stance_x:.1f}" y2="{margin + geometry.max_width_mm:.1f}" opacity="0.55"/>
  <text x="{foil_x + 12:.1f}" y="{margin + 38}" class="small">foil box centre</text>
  <text x="{stance_x + 12:.1f}" y="{margin + 74}" class="small">stance centre</text>

  <text x="{margin}" y="{profile_top - 45}" class="label">Side rocker profile</text>
  <text x="{margin + 330}" y="{profile_top - 45}" class="small">vertical scale x{profile_vertical_scale:.1f}</text>
  <line class="baseline" x1="{margin}" y1="{baseline_y}" x2="{margin + geometry.length_mm:.1f}" y2="{baseline_y}"/>
  <polygon class="rocker-band" points="{rocker_band_points}"/>
  <polyline class="rocker" points="{rocker_points}"/>
  <text x="{margin}" y="{height - 38}" class="small">Generated heuristic. Experimental design aid, not a proven board shape.</text>
</svg>
"""


def _points_to_svg(points: list[Point]) -> str:
    return " ".join(f"{point.x_mm:.1f},{point.y_mm:.1f}" for point in points)
