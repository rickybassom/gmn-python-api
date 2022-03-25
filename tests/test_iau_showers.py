"""Tests for the iau_showers module."""
import unittest
from unittest import mock

from requests.exceptions import HTTPError
from tests import _mock_response

from gmn_python_api import iau_showers


class TestIAUShowers(unittest.TestCase):
    """Tests for the iau_showers module."""

    @mock.patch("requests.get")
    def test_get_iau_showers_bad_response(self, mock_get: mock.Mock) -> None:
        """
        Test: That get_iau_showers() raises an exception when the response is not 200.
        When: get_iau_showers() is called with an HTTP mocked response.
        """
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        # iau_showers.get_iau_showers()
        self.assertRaises(HTTPError, iau_showers.get_iau_showers)

    @mock.patch("requests.get")
    def test_get_iau_showers_retrieve(self, mock_get: mock.Mock) -> None:
        """
        Test: That get_iau_showers() returns the expected dictionary of iau information.
        When: get_iau_showers() is called with an HTTP mocked response.
        """
        expected_content = ""
        mock_get.return_value = _mock_response(status=200, text=expected_content)
        self.assertEqual({}, iau_showers.get_iau_showers())


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
