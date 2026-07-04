"""First-pass board geometry heuristics.

These formulas are intentionally simple. They give us a deterministic shape
that can be inspected, tested, and improved as real board data arrives.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .spec import BoardSpec


@dataclass(frozen=True)
class Point:
    x_mm: float
    y_mm: float


@dataclass(frozen=True)
class BoardGeometry:
    length_mm: float
    max_width_mm: float
    max_thickness_mm: float
    foil_box_center_from_tail_mm: float
    stance_center_from_tail_mm: float
    volume_estimate_l: float
    outline_points: list[Point]
    rocker_points: list[Point]
    station_widths: list[Point]


@dataclass(frozen=True)
class DesignPreset:
    base_length_mm: float
    length_per_litre: float
    base_width_mm: float
    width_per_litre: float
    foil_box_position_ratio: float
    nose_rocker_mm: float
    tail_rocker_mm: float
    outline_controls: tuple[tuple[float, float], ...]


PRESETS = {
    "wing": DesignPreset(
        1250,
        5.8,
        440,
        1.35,
        0.38,
        145,
        22,
        ((0.00, 0.42), (0.10, 0.62), (0.28, 0.93), (0.48, 1.00), (0.68, 0.93), (0.88, 0.50), (1.00, 0.22)),
    ),
    "midlength_wing": DesignPreset(
        1320,
        4.5,
        460,
        1.25,
        0.39,
        155,
        24,
        ((0.00, 0.36), (0.10, 0.58), (0.30, 0.90), (0.52, 1.00), (0.72, 0.92), (0.90, 0.45), (1.00, 0.20)),
    ),
    "compact_wing": DesignPreset(
        980,
        7.8,
        390,
        3.0,
        0.36,
        115,
        18,
        ((0.00, 0.52), (0.08, 0.70), (0.25, 1.00), (0.52, 0.98), (0.76, 0.72), (0.92, 0.45), (1.00, 0.30)),
    ),
    "parawing": DesignPreset(
        1320,
        5.5,
        420,
        1.25,
        0.39,
        145,
        22,
        ((0.00, 0.35), (0.10, 0.58), (0.30, 0.92), (0.52, 1.00), (0.72, 0.90), (0.90, 0.43), (1.00, 0.18)),
    ),
    "downwind_sup": DesignPreset(
        1540,
        5.55,
        360,
        1.50,
        0.43,
        220,
        32,
        ((0.00, 0.24), (0.08, 0.46), (0.24, 0.78), (0.42, 0.98), (0.66, 1.00), (0.86, 0.62), (1.00, 0.24)),
    ),
    "beginner_sup_foil": DesignPreset(
        1550,
        4.4,
        520,
        1.78,
        0.41,
        170,
        28,
        ((0.00, 0.46), (0.10, 0.68), (0.30, 0.94), (0.50, 1.00), (0.72, 0.88), (0.90, 0.52), (1.00, 0.30)),
    ),
    "prone": DesignPreset(
        950,
        5.2,
        410,
        1.25,
        0.36,
        120,
        18,
        ((0.00, 0.42), (0.10, 0.64), (0.30, 0.94), (0.52, 1.00), (0.74, 0.82), (0.90, 0.48), (1.00, 0.25)),
    ),
    "pump": DesignPreset(
        700,
        24.3,
        300,
        8.15,
        0.36,
        75,
        12,
        ((0.00, 0.62), (0.10, 0.78), (0.28, 0.98), (0.52, 1.00), (0.74, 0.82), (0.90, 0.52), (1.00, 0.35)),
    ),
    "race": DesignPreset(
        1950,
        6.6,
        360,
        0.95,
        0.45,
        240,
        34,
        ((0.00, 0.18), (0.08, 0.38), (0.25, 0.76), (0.46, 1.00), (0.70, 0.92), (0.88, 0.48), (1.00, 0.16)),
    ),
    "wind_foil": DesignPreset(
        1720,
        2.2,
        650,
        1.33,
        0.42,
        170,
        28,
        ((0.00, 0.50), (0.10, 0.72), (0.30, 0.98), (0.52, 1.00), (0.76, 0.84), (0.92, 0.50), (1.00, 0.28)),
    ),
}

SKILL_LENGTH_ADJUST_MM = {
    "beginner": 120,
    "intermediate": 0,
    "advanced": -80,
    "race": 60,
}

SKILL_WIDTH_ADJUST_MM = {
    "beginner": 45,
    "intermediate": 0,
    "advanced": -25,
    "race": -45,
}


def generate_geometry(spec: BoardSpec) -> BoardGeometry:
    preset = PRESETS[spec.discipline]
    length_mm = (
        preset.base_length_mm
        + spec.target_volume_l * preset.length_per_litre
        + (spec.rider_weight_kg - 80) * 1.5
        + SKILL_LENGTH_ADJUST_MM[spec.skill_level]
    )
    max_width_mm = (
        preset.base_width_mm
        + spec.target_volume_l * preset.width_per_litre
        + (spec.rider_weight_kg - 80) * 0.55
        + SKILL_WIDTH_ADJUST_MM[spec.skill_level]
    )

    station_widths = _station_widths(length_mm, max_width_mm, preset)
    max_thickness_mm = _solve_thickness_for_volume(spec.target_volume_l, station_widths)
    volume_estimate_l = _estimate_volume_l(station_widths, max_thickness_mm)

    foil_box_center_from_tail_mm = length_mm * preset.foil_box_position_ratio
    foil_size_shift_mm = (1200 - spec.foil_area_cm2) * 0.035
    foil_box_center_from_tail_mm += foil_size_shift_mm
    stance_center_from_tail_mm = foil_box_center_from_tail_mm + spec.stance_width_mm * 0.08

    return BoardGeometry(
        length_mm=length_mm,
        max_width_mm=max_width_mm,
        max_thickness_mm=max_thickness_mm,
        foil_box_center_from_tail_mm=foil_box_center_from_tail_mm,
        stance_center_from_tail_mm=stance_center_from_tail_mm,
        volume_estimate_l=volume_estimate_l,
        outline_points=_outline_points(station_widths),
        rocker_points=_rocker_points(length_mm, preset),
        station_widths=station_widths,
    )


def _station_widths(length_mm: float, max_width_mm: float, preset: DesignPreset) -> list[Point]:
    stations = []
    for index in range(25):
        t = index / 24
        width_ratio = _smooth_interpolate(list(preset.outline_controls), t)
        stations.append(Point(length_mm * t, max_width_mm * width_ratio))
    return stations


def _outline_points(station_widths: list[Point]) -> list[Point]:
    right_side = [Point(point.x_mm, point.y_mm / 2) for point in station_widths]
    left_side = [Point(point.x_mm, -point.y_mm / 2) for point in reversed(station_widths)]
    return right_side + left_side + [right_side[0]]


def _rocker_points(length_mm: float, preset: DesignPreset) -> list[Point]:
    points = []
    for index in range(49):
        t = index / 48
        tail = preset.tail_rocker_mm * (1 - _smoothstep(0.04, 0.18, t))
        nose = preset.nose_rocker_mm * _smoothstep(0.58, 1.0, t) ** 1.2
        points.append(Point(length_mm * t, tail + nose))
    return points


def _solve_thickness_for_volume(target_volume_l: float, station_widths: list[Point]) -> float:
    litres_per_mm_thickness = _estimate_volume_l(station_widths, max_thickness_mm=1)
    return target_volume_l / litres_per_mm_thickness


def _estimate_volume_l(station_widths: list[Point], max_thickness_mm: float) -> float:
    total_mm3 = 0.0
    for left, right in zip(station_widths, station_widths[1:]):
        dx = right.x_mm - left.x_mm
        left_area = _station_area_mm2(left, max_thickness_mm)
        right_area = _station_area_mm2(right, max_thickness_mm)
        total_mm3 += dx * (left_area + right_area) / 2
    return total_mm3 / 1_000_000


def _station_area_mm2(station: Point, max_thickness_mm: float) -> float:
    max_station_width = max(abs(station.y_mm), 1)
    width_fraction = min(1.0, max_station_width / 650)
    thickness = max_thickness_mm * (0.45 + 0.55 * math.sqrt(width_fraction))
    cross_section_fullness = 0.88
    return station.y_mm * thickness * cross_section_fullness


def _smooth_interpolate(controls: list[tuple[float, float]], t: float) -> float:
    for (left_t, left_v), (right_t, right_v) in zip(controls, controls[1:]):
        if left_t <= t <= right_t:
            local_t = (t - left_t) / (right_t - left_t)
            eased = local_t * local_t * (3 - 2 * local_t)
            return left_v + (right_v - left_v) * eased
    return controls[-1][1]


def _smoothstep(edge0: float, edge1: float, value: float) -> float:
    if value <= edge0:
        return 0.0
    if value >= edge1:
        return 1.0
    x = (value - edge0) / (edge1 - edge0)
    return x * x * (3 - 2 * x)
