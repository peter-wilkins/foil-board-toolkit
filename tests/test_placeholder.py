import unittest

import foil_board_toolkit


class ProjectImportTests(unittest.TestCase):
    def test_project_imports(self):
        self.assertEqual(foil_board_toolkit.__version__, "0.1.0")
