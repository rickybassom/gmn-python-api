"""Tests for the data_directory module."""
import datetime
import unittest
from typing import Callable
from typing import List
from typing import Tuple
from unittest import mock

from requests.exceptions import HTTPError
from tests.unit import _mock_response

from gmn_python_api import data_directory
from gmn_python_api.data_directory import DAILY_DATE_INPUT_FORMAT, \
    MONTHLY_DATE_INPUT_FORMAT
from gmn_python_api.meteor_trajectory_schema import _MODEL_METEOR_TRAJECTORY_FILE_PATH


class TestGmnDataDirectory(unittest.TestCase):
    """Tests for the data_directory module."""

    def test_get_all_daily_file_urls_with_correct_file_extensions(self) -> None:
        """
        Test: That get_all_daily_file_urls() returns the expected list of files.
        When: get_all_daily_file_urls() is called with an HTTP mocked response.
        """
        expected_filenames = ["filename1.txt", "filename2.txt", "filename3.txt"]
        self.assertEqual(
            *self._run_get_all_method_with_mock_directory_listing(
                data_directory.get_all_daily_file_urls,
                expected_filenames,
                data_directory.DAILY_DIRECTORY,
            )
        )

    def test_get_all_monthly_file_urls_with_correct_file_extensions(self) -> None:
        """
        Test: That get_all_monthly_file_urls() returns the expected list of files.
        When: get_all_monthly_file_urls() is called with an HTTP mocked response.
        """
        expected_filenames = ["filename1.txt", "filename2.txt", "filename3.txt"]
        self.assertEqual(
            *self._run_get_all_method_with_mock_directory_listing(
                data_directory.get_all_monthly_file_urls,
                expected_filenames,
                data_directory.MONTHLY_DIRECTORY,
            )
        )

    def test_get_all_daily_file_urls_with_incorrect_file_extensions(self) -> None:
        """
        Test: That get_all_daily_file_urls() returns [].
        When: get_all_daily_file_urls() is called with an HTTP mocked response and file
        extension don't match.
        """
        expected_filenames = ["filename1.png", "filename2.jpg", "filename3.gif"]
        self.assertEqual(
            [],
            self._run_get_all_method_with_mock_directory_listing(
                data_directory.get_all_daily_file_urls,
                expected_filenames,
                data_directory.DAILY_DIRECTORY,
            )[1],
        )

    def test_get_all_monthly_file_urls_with_incorrect_file_extensions(self) -> None:
        """
        Test: That get_all_daily_file_urls() returns [].
        When: get_all_daily_file_urls() is called with an HTTP mocked response and file
        extension don't match.
        """
        expected_filenames = ["filename1.png", "filename2.jpg", "filename3.gif"]
        self.assertEqual(
            [],
            self._run_get_all_method_with_mock_directory_listing(
                data_directory.get_all_monthly_file_urls,
                expected_filenames,
                data_directory.MONTHLY_DIRECTORY,
            )[1],
        )

    @mock.patch("requests.get")
    def test_get_all_daily_file_urls_with_bad_response(
            self, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_all_daily_file_urls() raises an exception when the HTTP response
        is bad.
        When: get_all_daily_file_urls() is called with an HTTP mocked response.
        """
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(HTTPError, data_directory.get_all_daily_file_urls)

    @mock.patch("requests.get")
    def test_get_all_monthly_file_urls_with_bad_response(
            self, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_all_monthly_file_urls() raises an exception when the HTTP
        response is bad.
        When: get_all_monthly_file_urls() is called with an HTTP mocked response.
        """
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(HTTPError, data_directory.get_all_monthly_file_urls)

    def test_get_daily_file_url_by_date(self) -> None:
        """
        Test: That get_daily_file_url_by_date() returns the expected file url.
        When: get_daily_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = "filename-20190101-XYZ123.txt"
        self.assertEqual(
            [
                data_directory.BASE_URL + data_directory.DAILY_DIRECTORY + expected_filename],
            self._run_get_all_method_with_mock_directory_listing(
                lambda: [data_directory.get_daily_file_url_by_date(
                    datetime.date(2019, 1, 1).strftime(DAILY_DATE_INPUT_FORMAT))],
                [expected_filename, "hgahfgasjghi.txt", "filename-20190102-XYZ123.txt"],
                data_directory.DAILY_DIRECTORY,
            )[1],
        )

    def test_get_monthly_file_url_by_date(self) -> None:
        """
        Test: That get_monthly_file_url_by_date() returns the expected file url.
        When: get_monthly_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = "filename-201901-XYZ123.txt"
        self.assertEqual(
            [
                data_directory.BASE_URL + data_directory.MONTHLY_DIRECTORY + expected_filename],
            self._run_get_all_method_with_mock_directory_listing(
                lambda: [
                    data_directory.get_monthly_file_url_by_month(
                        datetime.date(2019, 1, 1).strftime(MONTHLY_DATE_INPUT_FORMAT)),
                ],
                [expected_filename, "hgahfgasjghi.txt", "filename-201902-XYZ123.txt"],
                data_directory.MONTHLY_DIRECTORY,
            )[1],
        )

    def test_get_all_file_url(self) -> None:
        """
        Test: That get_all_file_url() returns the expected file url.
        When: get_all_file_url() is called with an HTTP mocked response.
        """
        self.assertEqual(
            data_directory.BASE_URL + data_directory.SUMMARY_ALL_FILENAME,
            data_directory.get_all_file_url(),
        )

    @mock.patch("requests.get")
    def test_get_file_content_from_url(self, mock_get: mock.Mock) -> None:
        """
        Test: That get_file_content_from_url() returns the expected file content.
        When: get_file_content_from_url() is called with an HTTP mocked response.
        """
        expected_content = "This is the content of the file."
        mock_get.return_value = _mock_response(status=200, text=expected_content)
        self.assertEqual(
            expected_content,
            data_directory.get_file_content_from_url(
                data_directory.BASE_URL + data_directory.DAILY_DIRECTORY + "filename.txt"
            ),
        )

    def test_get_daily_file_url_current_date_today(self) -> None:
        """
        Test: That get_daily_file_url_by_date() returns the expected file url for the
        current day.
        When: get_daily_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = data_directory.SUMMARY_TODAY_FILENAME
        self.assertEqual(
            [
                data_directory.BASE_URL + data_directory.DAILY_DIRECTORY + expected_filename],
            self._run_get_all_method_with_mock_directory_listing(
                lambda: [
                    data_directory.get_daily_file_url_by_date(
                        datetime.date(2019, 1, 1).strftime(DAILY_DATE_INPUT_FORMAT),
                        datetime.date(2019, 1, 1)
                    )
                ],
                [expected_filename, "hgahfgasjghi.txt", "filename-20181204-XYZ123.txt"],
                data_directory.DAILY_DIRECTORY,
            )[1],
        )

    def test_get_daily_file_url_current_date_yesterday(self) -> None:
        """
        Test: That get_daily_file_url_by_date() returns the expected file url for the
        yesterday.
        When: get_daily_file_url_by_date() is called with an HTTP mocked response.
        """
        expected_filename = data_directory.SUMMARY_YESTERDAY_FILENAME
        self.assertEqual(
            [
                data_directory.BASE_URL + data_directory.DAILY_DIRECTORY + expected_filename],
            self._run_get_all_method_with_mock_directory_listing(
                lambda: [
                    data_directory.get_daily_file_url_by_date(
                        datetime.datetime(2019, 1, 1).strftime(DAILY_DATE_INPUT_FORMAT),
                        datetime.date(2019, 1, 2)
                    )
                ],
                [expected_filename, "hgahfgasjghi.txt", "filename-20181204-XYZ123.txt"],
                data_directory.DAILY_DIRECTORY,
            )[1],
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.data_directory._get_url_paths")
    def test_get_daily_file_content_by_date(
            self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_daily_file_content_by_date() returns the expected file content.
        When: get_daily_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            data_directory.BASE_URL
            + data_directory.DAILY_DIRECTORY
            + "traj_summary_20181209_solrange_257.0-258.0.txt",
            data_directory.BASE_URL + "daily/filename2.txt",
        ]
        expected_content = open(_MODEL_METEOR_TRAJECTORY_FILE_PATH).read()
        mock_get.return_value = _mock_response(text=expected_content)
        self.assertEqual(
            expected_content,
            data_directory.get_daily_file_content_by_date(
                datetime.date(2018, 12, 9).strftime(DAILY_DATE_INPUT_FORMAT)),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.data_directory._get_url_paths")
    def test_get_monthly_file_content_by_date(
            self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_monthly_file_content_by_date() returns the expected file content.
        When: get_monthly_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            data_directory.BASE_URL + data_directory.MONTHLY_DIRECTORY
            + "traj_summary_monthly_201812.txt",
            data_directory.BASE_URL + data_directory.MONTHLY_DIRECTORY
            + "filename2.txt",
        ]
        expected_content = open(_MODEL_METEOR_TRAJECTORY_FILE_PATH).read()
        mock_get.return_value = _mock_response(text=expected_content)
        self.assertEqual(
            expected_content,
            data_directory.get_monthly_file_content_by_date(
                datetime.date(2018, 12, 1).strftime(MONTHLY_DATE_INPUT_FORMAT)),
        )

    @mock.patch("requests.get")
    def test_get_all_file_content(self, mock_get: mock.Mock) -> None:
        """
        Test: That get_all_file_content() returns the expected file content.
        When: get_all_file_content() is called with an HTTP mocked response.
        """
        expected_content = open(_MODEL_METEOR_TRAJECTORY_FILE_PATH).read()
        mock_get.return_value = _mock_response(text=expected_content)
        self.assertEqual(
            expected_content,
            data_directory.get_all_file_content(),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.data_directory._get_url_paths")
    def test_get_daily_file_content_by_date_bad_response(
            self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_daily_file_content_by_date() raises an exception when the HTTP
        response is bad.
        When: get_daily_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            data_directory.BASE_URL
            + data_directory.DAILY_DIRECTORY
            + "traj_summary_20181209_solrange_257.0-258.0.txt",
            data_directory.BASE_URL + data_directory.DAILY_DIRECTORY + "filename2.txt",
        ]
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(
            HTTPError,
            data_directory.get_daily_file_content_by_date,
            datetime.date(2018, 12, 9).strftime(DAILY_DATE_INPUT_FORMAT),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.data_directory._get_url_paths")
    def test_get_daily_file_content_by_date_not_found(
            self, mock_get_url_paths: mock.Mock, _: mock.Mock
    ) -> None:
        """
        Test: That get_daily_file_content_by_date() raises an FileNotFoundError
        exception.
        When: get_daily_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            data_directory.BASE_URL
            + data_directory.DAILY_DIRECTORY
            + "traj_summary_20181209_solrange_257.0-258.0.txt",
            data_directory.BASE_URL + data_directory.DAILY_DIRECTORY + "filename2.txt",
        ]
        self.assertRaises(
            FileNotFoundError,
            data_directory.get_daily_file_content_by_date,
            datetime.date(2018, 12, 10).strftime(DAILY_DATE_INPUT_FORMAT),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.data_directory._get_url_paths")
    def test_get_monthly_file_content_by_date_with_bad_response(
            self, mock_get_url_paths: mock.Mock, mock_get: mock.Mock
    ) -> None:
        """
        Test: That get_monthly_file_content_by_date() raises an exception when the HTTP
        response is bad.
        When: get_monthly_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            data_directory.BASE_URL + data_directory.MONTHLY_DIRECTORY
            + "traj_summary_monthly_201812.txt",
            data_directory.BASE_URL + data_directory.MONTHLY_DIRECTORY
            + "filename2.txt",
        ]
        mock_get.return_value = _mock_response(
            status=500, raise_for_status=HTTPError("Bad response")
        )
        self.assertRaises(
            HTTPError,
            data_directory.get_monthly_file_content_by_date,
            datetime.date(2018, 12, 1).strftime(MONTHLY_DATE_INPUT_FORMAT),
        )

    @mock.patch("requests.get")
    @mock.patch("gmn_python_api.data_directory._get_url_paths")
    def test_get_monthly_file_content_by_date_with_not_found(
            self, mock_get_url_paths: mock.Mock, _: mock.Mock
    ) -> None:
        """
        Test: That get_monthly_file_content_by_date() raises an FileNotFoundError
        exception.
        When: get_monthly_file_content_by_date() is called with an HTTP mocked response.
        """
        mock_get_url_paths.return_value = [
            data_directory.BASE_URL + data_directory.MONTHLY_DIRECTORY
            + "traj_summary_monthly_201812.txt",
            data_directory.BASE_URL + data_directory.MONTHLY_DIRECTORY
            + "filename2.txt",
        ]
        self.assertRaises(
            FileNotFoundError,
            data_directory.get_monthly_file_content_by_date,
            datetime.date(2018, 11, 1).strftime(MONTHLY_DATE_INPUT_FORMAT),
        )

    @mock.patch("requests.get")
    def _run_get_all_method_with_mock_directory_listing(
            self,
            func: Callable[..., List[str]],
            filenames: List[str],
            directory: str,
            mock_get: mock.Mock,
    ) -> Tuple[List[str], List[str]]:
        """
        Mock the GMN data directory response run by mocking the files produced in a
        directory listing and return result.

        :param func: The function to be tested under the mocked server response.
        :param filenames: The expected filenames to be returned by the mock directory
         listing.
        :param directory: The directory to be mocked (e.g. daily/ or monthly/).
        :param mock_get: The requests.get mock object. Ignore and leave blank for
         method calls.

        :return: The expected file urls and the actual filenames returned by the mocked
         directory.
        """
        expected_file_urls = [
            data_directory.BASE_URL + directory + filename for filename in filenames
        ]
        mock_get.return_value = _mock_response(
            text="<html>"
                 f"{''.join(f'<a href={url}></a>' for url in filenames)}"
                 "</html>"
        )
        return expected_file_urls, func()


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
