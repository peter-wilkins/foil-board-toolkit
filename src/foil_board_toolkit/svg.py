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
    profile_vertical_scale = 1.45
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
    foil_box_x = foil_x - geometry.foil_box_length_mm / 2
    foil_box_y = margin + geometry.max_width_mm / 2 - geometry.foil_box_width_mm / 2
    stance_x = margin + geometry.stance_center_from_tail_mm
    rear_foot_x = stance_x - spec.stance_width_mm / 2
    front_foot_x = stance_x + spec.stance_width_mm / 2

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
    .hardware {{ fill: none; stroke: #7d3c98; stroke-width: 4; }}
    .stance {{ stroke: #546e7a; stroke-width: 2; stroke-dasharray: 8 9; }}
    .baseline {{ stroke: #546e7a; stroke-width: 2; }}
  </style>
  <rect width="100%" height="100%" fill="#fbfaf6"/>
  <text x="{margin}" y="48" class="label">Foil Board Toolkit: {escape(spec.name)}</text>
  <text x="{margin}" y="84" class="small">Plan outline: {geometry.length_mm:.0f} mm x {geometry.max_width_mm:.0f} mm. Estimated volume: {geometry.volume_estimate_l:.1f} L.</text>

  <polygon class="outline" points="{plan_points}"/>
  <rect class="hardware" x="{foil_box_x:.1f}" y="{foil_box_y:.1f}" width="{geometry.foil_box_length_mm:.1f}" height="{geometry.foil_box_width_mm:.1f}" rx="0"/>
  <line class="guide" x1="{foil_x:.1f}" y1="{margin}" x2="{foil_x:.1f}" y2="{margin + geometry.max_width_mm:.1f}"/>
  <line class="guide" x1="{stance_x:.1f}" y1="{margin}" x2="{stance_x:.1f}" y2="{margin + geometry.max_width_mm:.1f}" opacity="0.55"/>
  <line class="stance" x1="{rear_foot_x:.1f}" y1="{margin}" x2="{rear_foot_x:.1f}" y2="{margin + geometry.max_width_mm:.1f}"/>
  <line class="stance" x1="{front_foot_x:.1f}" y1="{margin}" x2="{front_foot_x:.1f}" y2="{margin + geometry.max_width_mm:.1f}"/>
  <text x="{foil_x + 12:.1f}" y="{margin + 38}" class="small">foil box centre</text>
  <text x="{stance_x + 12:.1f}" y="{margin + 74}" class="small">stance centre</text>
  <text x="{foil_box_x:.1f}" y="{foil_box_y - 16:.1f}" class="small">track envelope {geometry.foil_box_length_mm:.0f} x {geometry.foil_box_width_mm:.0f} mm</text>

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
