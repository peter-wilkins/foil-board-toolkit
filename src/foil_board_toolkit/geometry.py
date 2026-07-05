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
    foil_box_length_mm: float
    foil_box_width_mm: float
    stance_center_from_tail_mm: float
    volume_estimate_l: float
    outline_points: list[Point]
    rocker_points: list[Point]
    station_widths: list[Point]


@dataclass(frozen=True)
class OutlineControls:
    """Named plan-shape controls expressed as fractions of length and max width."""

    tail_width: float
    tail_shoulder_at: float
    tail_shoulder_width: float
    parallel_start_at: float
    parallel_end_at: float
    nose_shoulder_at: float
    nose_shoulder_width: float
    nose_width: float
    tail_curve: float = 1.0
    tail_to_mid_curve: float = 1.0
    nose_to_mid_curve: float = 1.0
    nose_curve: float = 1.0


@dataclass(frozen=True)
class DesignPreset:
    base_length_mm: float
    length_per_litre: float
    base_width_mm: float
    width_per_litre: float
    foil_box_position_ratio: float
    nose_rocker_mm: float
    tail_rocker_mm: float
    outline: OutlineControls


PRESETS = {
    "wing": DesignPreset(
        1250,
        5.8,
        440,
        1.35,
        0.38,
        145,
        22,
        OutlineControls(0.34, 0.11, 0.58, 0.34, 0.60, 0.84, 0.54, 0.20, 1.25, 0.85, 1.15, 0.85),
    ),
    "midlength_wing": DesignPreset(
        1320,
        4.5,
        460,
        1.25,
        0.39,
        155,
        24,
        OutlineControls(0.30, 0.11, 0.54, 0.38, 0.64, 0.86, 0.50, 0.17, 1.35, 0.90, 1.10, 0.80),
    ),
    "compact_wing": DesignPreset(
        980,
        7.8,
        390,
        3.0,
        0.36,
        115,
        18,
        OutlineControls(0.54, 0.09, 0.76, 0.22, 0.52, 0.80, 0.58, 0.34, 0.65, 0.80, 1.25, 1.35),
    ),
    "parawing": DesignPreset(
        1320,
        5.5,
        420,
        1.25,
        0.39,
        145,
        22,
        OutlineControls(0.30, 0.11, 0.56, 0.34, 0.60, 0.86, 0.50, 0.18, 1.30, 0.90, 1.10, 0.82),
    ),
    "downwind_sup": DesignPreset(
        1540,
        5.55,
        360,
        1.50,
        0.43,
        220,
        32,
        OutlineControls(0.14, 0.13, 0.40, 0.46, 0.70, 0.88, 0.56, 0.18, 1.85, 1.05, 1.10, 0.72),
    ),
    "beginner_sup_foil": DesignPreset(
        1550,
        4.4,
        520,
        1.78,
        0.41,
        170,
        28,
        OutlineControls(0.50, 0.10, 0.74, 0.32, 0.58, 0.83, 0.60, 0.36, 0.75, 0.85, 1.20, 1.30),
    ),
    "prone": DesignPreset(
        950,
        5.2,
        410,
        1.25,
        0.36,
        120,
        18,
        OutlineControls(0.44, 0.09, 0.66, 0.28, 0.50, 0.80, 0.54, 0.26, 0.80, 0.85, 1.15, 1.05),
    ),
    "pump": DesignPreset(
        700,
        24.3,
        300,
        8.15,
        0.36,
        75,
        12,
        OutlineControls(0.66, 0.08, 0.84, 0.24, 0.52, 0.78, 0.64, 0.42, 0.55, 0.75, 1.25, 1.45),
    ),
    "race": DesignPreset(
        1950,
        6.6,
        360,
        0.95,
        0.45,
        240,
        34,
        OutlineControls(0.10, 0.13, 0.34, 0.50, 0.72, 0.90, 0.42, 0.12, 2.00, 1.10, 1.10, 0.70),
    ),
    "wind_foil": DesignPreset(
        1720,
        2.2,
        650,
        1.33,
        0.42,
        170,
        28,
        OutlineControls(0.54, 0.10, 0.78, 0.32, 0.58, 0.82, 0.60, 0.34, 0.65, 0.80, 1.25, 1.25),
    ),
}

OUTLINE_STATION_COUNT = 49
FOIL_BOX_LENGTH_MM = 320
FOIL_BOX_WIDTH_MM = 90

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
        foil_box_length_mm=FOIL_BOX_LENGTH_MM,
        foil_box_width_mm=FOIL_BOX_WIDTH_MM,
        stance_center_from_tail_mm=stance_center_from_tail_mm,
        volume_estimate_l=volume_estimate_l,
        outline_points=_outline_points(station_widths),
        rocker_points=_rocker_points(length_mm, preset),
        station_widths=station_widths,
    )


def _station_widths(length_mm: float, max_width_mm: float, preset: DesignPreset) -> list[Point]:
    stations = []
    segments = _outline_control_segments(preset.outline)
    for index in range(OUTLINE_STATION_COUNT):
        t = index / (OUTLINE_STATION_COUNT - 1)
        width_ratio = _smooth_interpolate(segments, t)
        stations.append(Point(length_mm * t, max_width_mm * width_ratio))
    return stations


def _outline_control_segments(outline: OutlineControls) -> list[tuple[tuple[float, float], tuple[float, float], float]]:
    points = [
        (0.00, outline.tail_width),
        (outline.tail_shoulder_at, outline.tail_shoulder_width),
        (outline.parallel_start_at, 1.00),
        (outline.parallel_end_at, 1.00),
        (outline.nose_shoulder_at, outline.nose_shoulder_width),
        (1.00, outline.nose_width),
    ]
    curves = [
        outline.tail_curve,
        outline.tail_to_mid_curve,
        1.0,
        outline.nose_to_mid_curve,
        outline.nose_curve,
    ]
    return [
        (left, right, curve)
        for left, right, curve in zip(points, points[1:], curves)
    ]


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
    max_width_mm = max(point.y_mm for point in station_widths)
    for left, right in zip(station_widths, station_widths[1:]):
        dx = right.x_mm - left.x_mm
        left_area = _station_area_mm2(left, max_thickness_mm, max_width_mm)
        right_area = _station_area_mm2(right, max_thickness_mm, max_width_mm)
        total_mm3 += dx * (left_area + right_area) / 2
    return total_mm3 / 1_000_000


def _station_area_mm2(station: Point, max_thickness_mm: float, max_width_mm: float) -> float:
    station_width = max(abs(station.y_mm), 1)
    width_fraction = min(1.0, station_width / max_width_mm)
    thickness = max_thickness_mm * (0.45 + 0.55 * math.sqrt(width_fraction))
    cross_section_fullness = 0.88
    return station.y_mm * thickness * cross_section_fullness


def _smooth_interpolate(
    segments: list[tuple[tuple[float, float], tuple[float, float], float]], t: float
) -> float:
    for (left_t, left_v), (right_t, right_v), curve in segments:
        if left_t <= t <= right_t:
            local_t = (t - left_t) / (right_t - left_t)
            eased = _curved_smoothstep(local_t, curve)
            return left_v + (right_v - left_v) * eased
    return segments[-1][1][1]


def _curved_smoothstep(value: float, curve: float) -> float:
    eased = value * value * (3 - 2 * value)
    if curve == 1.0:
        return eased
    if curve > 1.0:
        return eased**curve
    return 1 - (1 - eased) ** (1 / curve)


def _smoothstep(edge0: float, edge1: float, value: float) -> float:
    if value <= edge0:
        return 0.0
    if value >= edge1:
        return 1.0
    x = (value - edge0) / (edge1 - edge0)
    return x * x * (3 - 2 * x)
