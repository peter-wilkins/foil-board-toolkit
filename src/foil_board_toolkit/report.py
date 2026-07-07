"""Machine-readable geometry reports."""

from __future__ import annotations

import json
from typing import Any

from .geometry import BoardGeometry
from .spec import BoardSpec


SCHEMA_VERSION = "foil-board-geometry-report/v1"


def geometry_report_dict(spec: BoardSpec, geometry: BoardGeometry) -> dict[str, Any]:
    """Return deterministic report data for validation and workshop review."""

    foil_box_rear = geometry.foil_box_center_from_tail_mm - geometry.foil_box_length_mm / 2
    foil_box_front = geometry.foil_box_center_from_tail_mm + geometry.foil_box_length_mm / 2
    rear_foot = geometry.stance_center_from_tail_mm - spec.stance_width_mm / 2
    front_foot = geometry.stance_center_from_tail_mm + spec.stance_width_mm / 2

    return {
        "schema_version": SCHEMA_VERSION,
        "units": {
            "length": "mm",
            "area": "mm2",
            "volume": "L",
        },
        "spec": {
            "name": spec.name,
            "discipline": spec.discipline,
            "skill_level": spec.skill_level,
            "rider_weight_kg": _round(spec.rider_weight_kg),
            "target_volume_l": _round(spec.target_volume_l),
            "foil_area_cm2": _round(spec.foil_area_cm2),
            "stance_width_mm": _round(spec.stance_width_mm),
        },
        "dimensions": {
            "length_mm": _round(geometry.length_mm),
            "max_width_mm": _round(geometry.max_width_mm),
            "max_thickness_mm": _round(geometry.max_thickness_mm),
            "length_to_width_ratio": _round(geometry.length_mm / geometry.max_width_mm, 3),
            "volume_estimate_l": _round(geometry.volume_estimate_l),
            "target_volume_delta_l": _round(geometry.volume_estimate_l - spec.target_volume_l),
        },
        "stock_envelope": {
            "length_mm": _round(geometry.stock_length_mm),
            "width_mm": _round(geometry.stock_width_mm),
            "thickness_mm": _round(geometry.stock_thickness_mm),
        },
        "foil_box": {
            "center_from_tail_mm": _round(geometry.foil_box_center_from_tail_mm),
            "rear_from_tail_mm": _round(foil_box_rear),
            "front_from_tail_mm": _round(foil_box_front),
            "length_mm": _round(geometry.foil_box_length_mm),
            "width_mm": _round(geometry.foil_box_width_mm),
        },
        "stance": {
            "center_from_tail_mm": _round(geometry.stance_center_from_tail_mm),
            "rear_foot_from_tail_mm": _round(rear_foot),
            "front_foot_from_tail_mm": _round(front_foot),
            "width_mm": _round(spec.stance_width_mm),
        },
        "validation": {
            "outline_closed": geometry.outline_points[0] == geometry.outline_points[-1],
            "station_count": len(geometry.volume_stations),
            "foil_box_inside_outline_length": 0 < foil_box_rear < foil_box_front < geometry.length_mm,
            "stock_exceeds_board": (
                geometry.stock_length_mm > geometry.length_mm
                and geometry.stock_width_mm > geometry.max_width_mm
                and geometry.stock_thickness_mm > geometry.max_thickness_mm
            ),
            "minimum_station_width_mm": _round(min(station.width_mm for station in geometry.volume_stations)),
            "minimum_station_thickness_mm": _round(min(station.thickness_mm for station in geometry.volume_stations)),
            "maximum_deck_height_mm": _round(max(point.y_mm for point in geometry.deck_profile_points)),
        },
        "stations": [
            {
                "x_mm": _round(station.x_mm),
                "width_mm": _round(station.width_mm),
                "thickness_mm": _round(station.thickness_mm),
                "rail_thickness_mm": _round(station.rail_thickness_mm),
                "deck_crown_mm": _round(station.deck_crown_mm),
                "bottom_contour_depth_mm": _round(station.bottom_contour_depth_mm),
                "cross_section_area_mm2": _round(station.cross_section_area_mm2),
                "bottom_rocker_mm": _round(rocker.y_mm),
                "deck_height_mm": _round(deck.y_mm),
            }
            for station, rocker, deck in zip(
                geometry.volume_stations,
                geometry.rocker_points,
                geometry.deck_profile_points,
            )
        ],
    }


def geometry_report_to_json(spec: BoardSpec, geometry: BoardGeometry) -> str:
    return json.dumps(geometry_report_dict(spec, geometry), indent=2, sort_keys=True) + "\n"


def _round(value: float, digits: int = 1) -> float:
    return round(float(value), digits)
