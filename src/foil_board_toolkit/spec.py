"""Board specification records and validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


DISCIPLINES = {"wing", "downwind_sup", "parawing", "prone", "race"}
SKILL_LEVELS = {"beginner", "intermediate", "advanced", "race"}


@dataclass(frozen=True)
class BoardSpec:
    """Inputs a builder cares about before any geometry is generated."""

    name: str
    rider_weight_kg: float
    target_volume_l: float
    discipline: str
    skill_level: str
    foil_area_cm2: float
    stance_width_mm: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BoardSpec":
        spec = cls(
            name=str(data["name"]),
            rider_weight_kg=float(data["rider_weight_kg"]),
            target_volume_l=float(data["target_volume_l"]),
            discipline=str(data["discipline"]),
            skill_level=str(data["skill_level"]),
            foil_area_cm2=float(data["foil_area_cm2"]),
            stance_width_mm=float(data["stance_width_mm"]),
        )
        spec.validate()
        return spec

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("name is required")
        if self.discipline not in DISCIPLINES:
            raise ValueError(f"discipline must be one of {sorted(DISCIPLINES)}")
        if self.skill_level not in SKILL_LEVELS:
            raise ValueError(f"skill_level must be one of {sorted(SKILL_LEVELS)}")
        if not 35 <= self.rider_weight_kg <= 140:
            raise ValueError("rider_weight_kg must be between 35 and 140")
        if not 20 <= self.target_volume_l <= 180:
            raise ValueError("target_volume_l must be between 20 and 180")
        if not 400 <= self.foil_area_cm2 <= 2600:
            raise ValueError("foil_area_cm2 must be between 400 and 2600")
        if not 300 <= self.stance_width_mm <= 800:
            raise ValueError("stance_width_mm must be between 300 and 800")


def load_board_spec(path: str | Path) -> BoardSpec:
    with Path(path).open(encoding="utf-8") as file:
        return BoardSpec.from_dict(json.load(file))

