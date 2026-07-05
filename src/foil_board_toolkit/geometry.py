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
class VolumeStation:
    x_mm: float
    width_mm: float
    thickness_mm: float
    rail_thickness_mm: float
    deck_crown_mm: float
    bottom_contour_depth_mm: float
    cross_section_area_mm2: float


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
    deck_profile_points: list[Point]
    station_widths: list[Point]
    volume_stations: list[VolumeStation]
    stock_length_mm: float
    stock_width_mm: float
    stock_thickness_mm: float


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
class VolumeControls:
    tail_thickness: float
    mid_thickness: float
    nose_thickness: float
    max_thickness_start_at: float
    max_thickness_end_at: float
    rail_thickness: float
    deck_crown_mm: float
    bottom_contour_depth_mm: float
    section_fullness: float


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
    volume: VolumeControls


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
        VolumeControls(0.62, 1.0, 0.58, 0.32, 0.58, 0.48, 8, 2, 0.84),
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
        VolumeControls(0.62, 1.0, 0.58, 0.36, 0.64, 0.45, 9, 2, 0.92),
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
        VolumeControls(0.70, 1.0, 0.62, 0.26, 0.54, 0.52, 6, 3, 0.86),
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
        VolumeControls(0.62, 1.0, 0.58, 0.34, 0.62, 0.45, 7, 2, 0.90),
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
        VolumeControls(0.52, 1.0, 0.60, 0.40, 0.70, 0.36, 12, 1, 0.92),
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
        VolumeControls(0.72, 1.0, 0.66, 0.30, 0.58, 0.55, 10, 2, 0.88),
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
        VolumeControls(0.66, 1.0, 0.58, 0.28, 0.52, 0.50, 6, 2, 0.84),
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
        VolumeControls(0.76, 1.0, 0.70, 0.24, 0.52, 0.58, 3, 1, 0.88),
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
        VolumeControls(0.38, 1.0, 0.44, 0.46, 0.70, 0.34, 10, 1, 0.76),
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
        VolumeControls(0.74, 1.0, 0.68, 0.30, 0.58, 0.56, 8, 4, 0.88),
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
    max_thickness_mm = _solve_thickness_for_volume(spec.target_volume_l, station_widths, preset)
    volume_stations = _volume_stations(station_widths, max_thickness_mm, preset)
    volume_estimate_l = _estimate_volume_l(volume_stations)
    rocker_points = _rocker_points(length_mm, preset)
    deck_profile_points = _deck_profile_points(rocker_points, volume_stations)

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
        rocker_points=rocker_points,
        deck_profile_points=deck_profile_points,
        station_widths=station_widths,
        volume_stations=volume_stations,
        stock_length_mm=math.ceil((length_mm + 40) / 10) * 10,
        stock_width_mm=math.ceil((max_width_mm + 30) / 10) * 10,
        stock_thickness_mm=math.ceil((max(point.y_mm for point in deck_profile_points) + 10) / 10) * 10,
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


def _deck_profile_points(rocker_points: list[Point], volume_stations: list[VolumeStation]) -> list[Point]:
    return [
        Point(rocker.x_mm, rocker.y_mm + station.thickness_mm + station.deck_crown_mm)
        for rocker, station in zip(rocker_points, volume_stations)
    ]


def _solve_thickness_for_volume(target_volume_l: float, station_widths: list[Point], preset: DesignPreset) -> float:
    low = 1.0
    high = 260.0
    for _ in range(40):
        candidate = (low + high) / 2
        volume_l = _estimate_volume_l(_volume_stations(station_widths, candidate, preset))
        if volume_l < target_volume_l:
            low = candidate
        else:
            high = candidate
    return high


def _estimate_volume_l(volume_stations: list[VolumeStation]) -> float:
    total_mm3 = 0.0
    for left, right in zip(volume_stations, volume_stations[1:]):
        dx = right.x_mm - left.x_mm
        total_mm3 += dx * (left.cross_section_area_mm2 + right.cross_section_area_mm2) / 2
    return total_mm3 / 1_000_000


def _volume_stations(station_widths: list[Point], max_thickness_mm: float, preset: DesignPreset) -> list[VolumeStation]:
    max_width_mm = max(point.y_mm for point in station_widths)
    return [
        _volume_station(point, index / (len(station_widths) - 1), max_thickness_mm, max_width_mm, preset)
        for index, point in enumerate(station_widths)
    ]


def _volume_station(
    station: Point,
    t: float,
    max_thickness_mm: float,
    max_width_mm: float,
    preset: DesignPreset,
) -> VolumeStation:
    station_width = max(abs(station.y_mm), 1)
    width_fraction = min(1.0, station_width / max_width_mm)
    length_thickness = _thickness_ratio_at(t, preset.volume)
    width_thickness = 0.82 + 0.18 * math.sqrt(width_fraction)
    thickness = max_thickness_mm * length_thickness * width_thickness
    rail_thickness = thickness * preset.volume.rail_thickness
    deck_crown = preset.volume.deck_crown_mm * math.sin(math.pi * t) * math.sqrt(width_fraction)
    bottom_contour_depth = preset.volume.bottom_contour_depth_mm * math.sin(math.pi * t) * width_fraction
    area = station_width * thickness * preset.volume.section_fullness
    area += station_width * (deck_crown + bottom_contour_depth) * 0.35
    return VolumeStation(
        x_mm=station.x_mm,
        width_mm=station.y_mm,
        thickness_mm=thickness,
        rail_thickness_mm=rail_thickness,
        deck_crown_mm=deck_crown,
        bottom_contour_depth_mm=bottom_contour_depth,
        cross_section_area_mm2=area,
    )


def _thickness_ratio_at(t: float, controls: VolumeControls) -> float:
    if t <= controls.max_thickness_start_at:
        local_t = t / controls.max_thickness_start_at
        return controls.tail_thickness + (controls.mid_thickness - controls.tail_thickness) * _curved_smoothstep(local_t, 0.85)
    if t <= controls.max_thickness_end_at:
        return controls.mid_thickness
    local_t = (t - controls.max_thickness_end_at) / (1 - controls.max_thickness_end_at)
    return controls.mid_thickness + (controls.nose_thickness - controls.mid_thickness) * _curved_smoothstep(local_t, 1.15)


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
