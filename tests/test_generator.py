import tempfile
import unittest
import json
from pathlib import Path

from foil_board_toolkit.cli import main
from foil_board_toolkit.geometry import generate_geometry
from foil_board_toolkit.report import SCHEMA_VERSION, geometry_report_dict, geometry_report_to_json
from foil_board_toolkit.spec import BoardSpec, load_board_spec
from foil_board_toolkit.svg import geometry_to_svg


def width_at_fraction(geometry, fraction):
    target_x = geometry.length_mm * fraction
    return min(geometry.station_widths, key=lambda point: abs(point.x_mm - target_x)).y_mm


class GeneratorTests(unittest.TestCase):
    def test_all_examples_generate_sane_geometry(self):
        for spec_path in sorted(Path("examples").glob("*.json")):
            with self.subTest(spec=spec_path.name):
                spec = load_board_spec(spec_path)
                geometry = generate_geometry(spec)

                self.assertGreater(geometry.length_mm, 700)
                self.assertLess(geometry.length_mm, 2600)
                self.assertGreater(geometry.max_width_mm, 350)
                self.assertLess(geometry.max_width_mm, 950)
                self.assertGreater(geometry.max_thickness_mm, 35)
                self.assertLess(geometry.max_thickness_mm, 190)
                self.assertAlmostEqual(geometry.volume_estimate_l, spec.target_volume_l, delta=0.2)
                self.assertEqual(geometry.outline_points[0], geometry.outline_points[-1])
                self.assertEqual(len(geometry.station_widths), 49)
                self.assertEqual(len(geometry.volume_stations), len(geometry.station_widths))
                self.assertEqual(len(geometry.deck_profile_points), len(geometry.rocker_points))
                self.assertAlmostEqual(
                    max(station.thickness_mm for station in geometry.volume_stations),
                    geometry.max_thickness_mm,
                    delta=0.1,
                )
                self.assertTrue(all(station.cross_section_area_mm2 > 0 for station in geometry.volume_stations))
                self.assertTrue(all(station.rail_thickness_mm > 0 for station in geometry.volume_stations))
                self.assertGreater(geometry.stock_length_mm, geometry.length_mm)
                self.assertGreater(geometry.stock_width_mm, geometry.max_width_mm)
                self.assertGreater(geometry.stock_thickness_mm, geometry.max_thickness_mm)
                self.assertGreater(geometry.foil_box_length_mm, 250)
                self.assertGreater(geometry.foil_box_width_mm, 70)
                self.assertGreater(geometry.foil_box_center_from_tail_mm - geometry.foil_box_length_mm / 2, 0)
                self.assertLess(
                    geometry.foil_box_center_from_tail_mm + geometry.foil_box_length_mm / 2,
                    geometry.length_mm,
                )
                self.assertLess(geometry.foil_box_width_mm, width_at_fraction(geometry, 0.4))

    def test_example_generates_sane_geometry(self):
        spec = load_board_spec("examples/midlength-wing-85l.json")
        geometry = generate_geometry(spec)

        self.assertGreater(geometry.length_mm, 1600)
        self.assertLess(geometry.length_mm, 1900)
        self.assertGreater(geometry.max_width_mm, 520)
        self.assertLess(geometry.max_width_mm, 590)
        self.assertAlmostEqual(geometry.volume_estimate_l, 85, delta=0.2)
        self.assertGreater(geometry.foil_box_center_from_tail_mm, 550)
        self.assertLess(geometry.foil_box_center_from_tail_mm, 750)

    def test_outline_is_closed_and_has_no_negative_widths(self):
        spec = load_board_spec("examples/midlength-wing-85l.json")
        geometry = generate_geometry(spec)

        self.assertEqual(geometry.outline_points[0], geometry.outline_points[-1])
        self.assertTrue(all(point.y_mm >= 0 for point in geometry.station_widths))

    def test_volume_station_model_has_deck_rail_and_bottom_features(self):
        geometry = generate_geometry(load_board_spec("examples/midlength-wing-85l.json"))

        tail, middle, nose = geometry.volume_stations[0], geometry.volume_stations[24], geometry.volume_stations[-1]

        self.assertLess(tail.thickness_mm, middle.thickness_mm)
        self.assertLess(nose.thickness_mm, middle.thickness_mm)
        self.assertGreater(middle.deck_crown_mm, tail.deck_crown_mm)
        self.assertGreater(middle.bottom_contour_depth_mm, tail.bottom_contour_depth_mm)
        self.assertLess(middle.rail_thickness_mm, middle.thickness_mm)
        self.assertGreater(middle.cross_section_area_mm2, tail.cross_section_area_mm2)

    def test_family_outline_character_is_distinct(self):
        downwind = generate_geometry(load_board_spec("examples/downwind-sup-86l.json"))
        compact = generate_geometry(load_board_spec("examples/compact-wing-50l.json"))
        pump = generate_geometry(load_board_spec("examples/pump-13l.json"))
        beginner_sup = generate_geometry(load_board_spec("examples/beginner-sup-foil-122l.json"))

        self.assertGreater(downwind.length_mm / downwind.max_width_mm, 4.0)
        self.assertLess(downwind.station_widths[0].y_mm / downwind.max_width_mm, 0.16)
        self.assertLess(downwind.station_widths[-1].y_mm / downwind.max_width_mm, 0.20)
        self.assertLess(width_at_fraction(downwind, 0.12), width_at_fraction(downwind, 0.88))

        self.assertLess(compact.length_mm / compact.max_width_mm, 2.7)
        self.assertGreater(compact.station_widths[0].y_mm / compact.max_width_mm, 0.50)
        self.assertGreater(pump.station_widths[0].y_mm / pump.max_width_mm, 0.60)
        self.assertGreater(pump.station_widths[-1].y_mm / pump.max_width_mm, 0.40)
        self.assertGreater(beginner_sup.station_widths[-1].y_mm / beginner_sup.max_width_mm, 0.34)

    def test_invalid_spec_rejected(self):
        with self.assertRaises(ValueError):
            BoardSpec.from_dict(
                {
                    "name": "bad",
                    "rider_weight_kg": 80,
                    "target_volume_l": 85,
                    "discipline": "clone_named_board",
                    "skill_level": "intermediate",
                    "foil_area_cm2": 1200,
                    "stance_width_mm": 560,
                }
            )

    def test_svg_export_writes_template(self):
        spec = load_board_spec("examples/midlength-wing-85l.json")
        geometry = generate_geometry(spec)
        svg = geometry_to_svg(spec, geometry)

        self.assertIn("<svg", svg)
        self.assertIn("foil box centre", svg)
        self.assertIn("Stock envelope", svg)
        self.assertIn("class=\"deck\"", svg)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "board.svg"
            output.write_text(svg, encoding="utf-8")
            self.assertGreater(output.stat().st_size, 1000)

    def test_geometry_report_contains_measurable_validation_data(self):
        spec = load_board_spec("examples/midlength-wing-85l.json")
        geometry = generate_geometry(spec)
        report = geometry_report_dict(spec, geometry)

        self.assertEqual(report["schema_version"], SCHEMA_VERSION)
        self.assertEqual(report["units"]["length"], "mm")
        self.assertEqual(report["spec"]["name"], "midlength-wing-85l")
        self.assertEqual(report["dimensions"]["length_mm"], round(geometry.length_mm, 1))
        self.assertEqual(report["dimensions"]["volume_estimate_l"], round(geometry.volume_estimate_l, 1))
        self.assertTrue(report["validation"]["outline_closed"])
        self.assertTrue(report["validation"]["foil_box_inside_outline_length"])
        self.assertTrue(report["validation"]["stock_exceeds_board"])
        self.assertEqual(report["validation"]["station_count"], len(geometry.volume_stations))
        self.assertEqual(len(report["stations"]), len(geometry.volume_stations))
        self.assertIn("deck_height_mm", report["stations"][24])

        parsed = json.loads(geometry_report_to_json(spec, geometry))
        self.assertEqual(parsed["schema_version"], SCHEMA_VERSION)

    def test_cli_can_write_svg_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            svg_path = Path(tmp) / "board.svg"
            report_path = Path(tmp) / "board.report.json"

            exit_code = main(
                [
                    "generate",
                    "examples/midlength-wing-85l.json",
                    "--out",
                    str(svg_path),
                    "--report-out",
                    str(report_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertGreater(svg_path.stat().st_size, 1000)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["spec"]["name"], "midlength-wing-85l")


if __name__ == "__main__":
    unittest.main()
