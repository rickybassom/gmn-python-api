"""Unit tests for the gmn_python_api library."""
from typing import Optional
from unittest import mock


def _mock_response(
    status: int = 200, text: str = "text", raise_for_status: Optional[Exception] = None
) -> mock.Mock:
    """
    Mock a requests.Response object.

    :param status: The HTTP status code.
    :param content: The HTTP response content.
    :param raise_for_status: The exception to be raised when the HTTP status code is
     not 200.

    :return: The mock requests.Response object.
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
