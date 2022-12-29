"""Integration tests for the IAU showers API."""
import unittest
from gmn_python_api import iau_showers


class TestIAUShowers(unittest.TestCase):
    """Tests for live integration with the IAU showers API."""

    def test_get_iau_showers(self) -> None:
        """
        Test: That get_iau_showers() returns the expected dictionary of iau information.
        When: get_iau_showers() is called.
        """
        showers = iau_showers.get_iau_showers()
        self.assertGreater(len(showers), 0)
        self.assertIn("00001", showers)
        self.assertEqual(showers["00001"],
                         {"id": "00001", "code": "CAP", "name": "alpha Capricornids"})


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
