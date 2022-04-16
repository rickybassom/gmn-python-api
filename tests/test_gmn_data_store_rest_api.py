"""Tests for the gmn_data_store_rest_api module."""
import unittest
from unittest import mock
from urllib.parse import urlencode

from requests import HTTPError
from tests import _mock_response

from gmn_python_api import gmn_data_store_rest_api


class TestGmnDataStoreRestApi(unittest.TestCase):
    """Tests for the gmn_data_store_rest_api module."""

    @mock.patch("gmn_python_api.gmn_data_store_rest_api._http_get_response")
    def test_get_data_response(self, mock_http_get_response: mock.Mock) -> None:
        """
        Test: That get_data returns the expected response.
        When: Calling get_data with a mocked response.
        """
        expected_data = "test", "next_url"
        mock_http_get_response.return_value = expected_data
        actual_data = gmn_data_store_rest_api.get_data()
        self.assertEqual(expected_data, actual_data)

    @mock.patch("gmn_python_api.gmn_data_store_rest_api._http_get_response")
    def test_get_data_query_url(self, mock_http_get_response: mock.Mock) -> None:
        """
        Test: That get_data uses the correct query url based on function arguments.
        When: Calling get_data with a mocked response.
        """
        expected_query_url = (
            "http://0.0.0.0:8001/gmn_data_store{table}.{data_format}"
            "?_shape={data_shape}"
        )
        with mock.patch(
            "gmn_python_api.gmn_data_store_rest_api.QUERY_URL", expected_query_url
        ):
            mock_http_get_response.return_value = ""

            expected_table = "test_table"
            expected_table_arguments = {
                "test_arg1": "test_arg1_value",
                "_test_arg2": "test_arg2_value",
                "__test_arg3": "test_arg3_value",
            }
            expected_data_format = gmn_data_store_rest_api.DataFormat.CSV
            expected_data_shape = gmn_data_store_rest_api.DataShape.ARRAY
            gmn_data_store_rest_api.get_data(
                table=expected_table,
                table_arguments=expected_table_arguments,
                data_format=expected_data_format,
                data_shape=expected_data_shape,
            )
            expected_url = expected_query_url.format(
                table="/" + expected_table,
                data_format=expected_data_format,
                data_shape=expected_data_shape,
            )
            expected_url += "&" + urlencode(expected_table_arguments)
            mock_http_get_response.assert_called_with(expected_url)

    @mock.patch("gmn_python_api.gmn_data_store_rest_api.get_data")
    def test_get_data_with_sql(self, mock_get_data: mock.Mock) -> None:
        """
        Test: That get_data_with_sql returns the expected data.
        When: Calling get_data_with_sql with a mocked response.
        """
        expected_data = "test"
        mock_get_data.return_value = expected_data
        actual_data = gmn_data_store_rest_api.get_data_with_sql("test_sql")
        self.assertEqual(expected_data, actual_data)

    @mock.patch("gmn_python_api.gmn_data_store_rest_api.get_data")
    def test_get_meteor_summary_data(self, mock_get_data: mock.Mock) -> None:
        """
        Test: That get_meteor_summary_data returns the expected data.
        When: Calling get_meteor_summary_data with a mocked response.
        """
        expected_data = "test"
        mock_get_data.return_value = expected_data
        actual_data = gmn_data_store_rest_api.get_meteor_summary_data()
        self.assertEqual(expected_data, actual_data)

    @mock.patch("gmn_python_api.gmn_data_store_rest_api.get_meteor_summary_data")
    def test_get_meteor_summary_data_reader_compatible(
        self, mock_get_meteor_summary_data: mock.Mock
    ) -> None:
        """
        Test: That get_meteor_summary_data_reader_compatible returns the expected data.
        When: Calling get_meteor_summary_data_reader_compatible with a mocked response.
        """
        expected_data = "test"
        mock_get_meteor_summary_data.return_value = expected_data
        actual_data = (
            gmn_data_store_rest_api.get_meteor_summary_data_reader_compatible()
        )
        self.assertEqual(expected_data, actual_data)

    @mock.patch("requests.get")
    def test_http_get_response(self, mock_requests_get: mock.Mock) -> None:
        """
        Test: That _http_get_response returns the expected response.
        When: Calling _http_get_response with a mocked response.
        """
        expected_data = "test", "next_url"
        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.text = "test"
        mock_requests_get.return_value.links = {"next": {"url": "next_url"}}
        actual_data = gmn_data_store_rest_api._http_get_response("test_url")

        self.assertEqual(expected_data, actual_data)

    @mock.patch("requests.get")
    def test_http_get_response_no_next(self, mock_requests_get: mock.Mock) -> None:
        """
        Test: That _http_get_response returns the expected response.
        When: Calling _http_get_response with a mocked response.
        """
        expected_data = "test", None
        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.text = "test"
        mock_requests_get.return_value.links = {}
        actual_data = gmn_data_store_rest_api._http_get_response("test_url")

        self.assertEqual(expected_data, actual_data)

    @mock.patch("requests.get")
    def test_http_get_response_with_bad_response(
        self, mock_requests_get: mock.Mock
    ) -> None:
        """
        Test: That _http_get_response() raises an exception when the HTTP
        response is bad.
        When: _http_get_response() is called with an HTTP mocked response.
        """
        mock_requests_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(
            HTTPError, gmn_data_store_rest_api._http_get_response, "test_url"
        )
