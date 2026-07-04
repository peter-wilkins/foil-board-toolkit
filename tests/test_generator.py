import tempfile
import unittest
from pathlib import Path

from foil_board_toolkit.geometry import generate_geometry
from foil_board_toolkit.spec import BoardSpec, load_board_spec
from foil_board_toolkit.svg import geometry_to_svg


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
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "board.svg"
            output.write_text(svg, encoding="utf-8")
            self.assertGreater(output.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
