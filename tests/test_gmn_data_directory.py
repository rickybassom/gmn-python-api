"""Tests for the gmn_data_directory module."""
import datetime
import unittest
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from unittest import mock

from requests.exceptions import HTTPError

from gmn_python_api import gmn_data_directory


class TestGmnDataDirectory(unittest.TestCase):
    """Tests for the gmn_data_directory module."""

    def test_get_all_daily_file_urls_with_correct_file_extensions(self) -> None:
        """
        Test: That get_all_daily_file_urls() returns the expected list of files.
        When: get_all_daily_file_urls() is called with an HTTP mocked response.
        """
        expected_filenames = ["filename1.txt", "filename2.txt", "filename3.txt"]
        self.assertEqual(
            *self._get_all_method_against_mock_directory_listing(
                gmn_data_directory.get_all_daily_file_urls,
                expected_filenames,
                "daily",
            )
        )

    def test_get_all_monthly_file_urls_with_correct_file_extensions(self) -> None:
        """
        Test: That get_all_daily_file_urls() returns the expected list of files.
        When: get_all_daily_file_urls() is called with an HTTP mocked response.
        """
        expected_filenames = ["filename1.txt", "filename2.txt", "filename3.txt"]
        self.assertEqual(
            *self._get_all_method_against_mock_directory_listing(
                gmn_data_directory.get_all_monthly_file_urls,
                expected_filenames,
                "monthly",
            )
        )

    def test_get_all_daily_file_urls_with_incorrect_file_extensions(self) -> None:
        """
        Test: That get_all_daily_file_urls() returns the expected list of files.
        When: get_all_daily_file_urls() is called with an HTTP mocked response.
        """
        expected_filenames = ["filename1.png", "filename2.jpg", "filename3.gif"]
        self.assertEqual(
            [],
            self._get_all_method_against_mock_directory_listing(
                gmn_data_directory.get_all_daily_file_urls,
                expected_filenames,
                "daily",
            )[1],
        )

    def test_get_all_monthly_file_urls_with_incorrect_file_extensions(self) -> None:
        """
        Test: That get_all_daily_file_urls() returns the expected list of files.
        When: get_all_daily_file_urls() is called with an HTTP mocked response.
        """
        expected_filenames = ["filename1.png", "filename2.jpg", "filename3.gif"]
        self.assertEqual(
            [],
            self._get_all_method_against_mock_directory_listing(
                gmn_data_directory.get_all_monthly_file_urls,
                expected_filenames,
                "monthly",
            )[1],
        )

    @mock.patch("requests.get")
    def test_get_all_daily_file_urls_with_bad_response(
        self, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_all_daily_file_urls() raises an exception when the HTTP response is bad.
        When: get_all_daily_file_urls() is called with an HTTP mocked response.
        """
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(HTTPError, gmn_data_directory.get_all_daily_file_urls)

    @mock.patch("requests.get")
    def test_get_all_monthly_file_urls_with_bad_response(
        self, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_all_monthly_file_urls() raises an exception when the HTTP response is bad.
        When: get_all_monthly_file_urls() is called with an HTTP mocked response.
        """
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(HTTPError, gmn_data_directory.get_all_monthly_file_urls)

    def test_get_daily_file_url_by_date(self) -> None:
        """
        Test: That get_daily_file_url_by_date() returns the expected file url.
        When: get_daily_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = "filename-20190101-XYZ123.txt"
        self.assertEqual(
            [gmn_data_directory.BASE_URL + "daily/" + expected_filename],
            self._get_all_method_against_mock_directory_listing(
                lambda: [
                    gmn_data_directory.get_daily_file_url_by_date(
                        datetime.datetime(2019, 1, 1)
                    )
                ],
                [expected_filename, "hgahfgasjghi.txt", "filename-20190102-XYZ123.txt"],
                "daily",
            )[1],
        )

    def test_get_monthly_file_url_by_date(self) -> None:
        """
        Test: That get_monthly_file_url_by_date() returns the expected file url.
        When: get_monthly_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = "filename-201901-XYZ123.txt"
        self.assertEqual(
            [gmn_data_directory.BASE_URL + "monthly/" + expected_filename],
            self._get_all_method_against_mock_directory_listing(
                lambda: [
                    gmn_data_directory.get_monthly_file_url_by_month(
                        datetime.datetime(2019, 1, 1)
                    )
                ],
                [expected_filename, "hgahfgasjghi.txt", "filename-201902-XYZ123.txt"],
                "monthly",
            )[1],
        )

    def test_get_daily_file_url_current_date_today(self) -> None:
        """
        Test: That get_daily_file_url_by_date() returns the expected file url for the current day.
        When: get_daily_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = gmn_data_directory.SUMMARY_TODAY_FILENAME
        self.assertEqual(
            [gmn_data_directory.BASE_URL + "daily/" + expected_filename],
            self._get_all_method_against_mock_directory_listing(
                lambda: [
                    gmn_data_directory.get_daily_file_url_by_date(
                        datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 1)
                    )
                ],
                [expected_filename, "hgahfgasjghi.txt", "filename-20181204-XYZ123.txt"],
                "daily",
            )[1],
        )

    def test_get_daily_file_url_current_date_yesterday(self) -> None:
        """
        Test: That get_daily_file_url_by_date() returns the expected file url for the yesterday.
        When: get_daily_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = gmn_data_directory.SUMMARY_YESTERDAY_FILENAME
        self.assertEqual(
            [gmn_data_directory.BASE_URL + "daily/" + expected_filename],
            self._get_all_method_against_mock_directory_listing(
                lambda: [
                    gmn_data_directory.get_daily_file_url_by_date(
                        datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 2)
                    )
                ],
                [expected_filename, "hgahfgasjghi.txt", "filename-20181204-XYZ123.txt"],
                "daily",
            )[1],
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.gmn_data_directory._get_url_paths")
    def test_get_daily_file_content_by_date(
        self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_daily_file_content_by_date() returns the expected file content.
        When: get_daily_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            gmn_data_directory.BASE_URL
            + "daily/traj_summary_20181209_solrange_257.0-258.0.txt",
            gmn_data_directory.BASE_URL + "daily/filename2.txt",
        ]
        expected_content = open(
            "tests/test_data/traj_summary_20181209_solrange_257.0-258.0.txt"
        ).read()
        mock_get.return_value = _mock_response(text=expected_content)
        self.assertEqual(
            expected_content,
            gmn_data_directory.get_daily_file_content_by_date(
                datetime.datetime(2018, 12, 9)
            ),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.gmn_data_directory._get_url_paths")
    def test_get_monthly_file_content_by_date(
        self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_monthly_file_content_by_date() returns the expected file content.
        When: get_monthly_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            gmn_data_directory.BASE_URL + "daily/traj_summary_monthly_201812.txt",
            gmn_data_directory.BASE_URL + "daily/filename2.txt",
        ]
        expected_content = open(
            "tests/test_data/traj_summary_monthly_201812.txt"
        ).read()
        mock_get.return_value = _mock_response(text=expected_content)
        self.assertEqual(
            expected_content,
            gmn_data_directory.get_monthly_file_content_by_date(
                datetime.datetime(2018, 12, 1)
            ),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.gmn_data_directory._get_url_paths")
    def test_get_daily_file_content_by_date_bad_response(
        self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_daily_file_content_by_date() raises an exception when the HTTP response is bad.
        When: get_daily_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            gmn_data_directory.BASE_URL
            + "daily/traj_summary_20181209_solrange_257.0-258.0.txt",
            gmn_data_directory.BASE_URL + "daily/filename2.txt",
        ]
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(
            HTTPError,
            gmn_data_directory.get_daily_file_content_by_date,
            datetime.datetime(2018, 12, 9),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.gmn_data_directory._get_url_paths")
    def test_get_monthly_file_content_by_date_with_bad_response(
        self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_monthly_file_content_by_date() raises an exception when the HTTP response is bad.
        When: get_monthly_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            gmn_data_directory.BASE_URL + "daily/traj_summary_monthly_201812.txt",
            gmn_data_directory.BASE_URL + "daily/filename2.txt",
        ]
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(
            HTTPError,
            gmn_data_directory.get_monthly_file_content_by_date,
            datetime.datetime(2018, 12, 1),
        )

    @mock.patch("requests.get")
    def _get_all_method_against_mock_directory_listing(
        self,
        func: Callable[..., Any],
        filenames: List[str],
        directory: str,
        mock_get: mock.Mock,
    ) -> Tuple[List[str], List[str]]:
        """
        Mock the GMN data directory response run by get_all_daily_file_urls using expected_filenames and return result.
        :param func: The function to be tested under the mocked server response.
        :param filenames: The expected filenames to be returned by the mock directory listing.
        :param directory: The directory to be mocked (e.g. daily or monthly).
        :param mock_get: The requests.get mock object. Ignore and leave blank for method calls.
        :return: The expected file urls and the actual filenames returned by the mocked directory.
        """
        expected_file_urls = [
            gmn_data_directory.BASE_URL + directory + "/" + filename
            for filename in filenames
        ]
        mock_get.return_value = _mock_response(
            text="<html>"
            f"{''.join(f'<a href={url}></a>' for url in filenames)}"
            "</html>"
        )
        return expected_file_urls, func()


def _mock_response(
    status: int = 200, text: str = "text", raise_for_status: Optional[Exception] = None
) -> mock.Mock:
    """
    Mock a requests.Response object.
    :param status:
    :param content:
    :param raise_for_status:
    :return:
    """
    mock_resp = mock.Mock()
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status

    mock_resp.status_code = status
    if status != 200:
        mock_resp.ok = False

    mock_resp.text = text
    return mock_resp


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
