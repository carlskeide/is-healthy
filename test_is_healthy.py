#!/bin/env python3
import json
from unittest.mock import patch, Mock
from requests.exceptions import ConnectionError, ReadTimeout

from is_healthy import parse_healthy, parse_status, check_health


def test_parse_healthy():
    # Invalid format
    assert parse_healthy({}) is False
    assert parse_healthy({"healthy": ""}) is False

    # Valid but unhealthy
    assert parse_healthy({"healthy": False}) is False
    assert parse_healthy({"healthy": "False"}) is False
    assert parse_healthy({"healthy": "false"}) is False

    # Valid and unhealthy
    assert parse_healthy({"healthy": True}) is True
    assert parse_healthy({"healthy": "True"}) is True
    assert parse_healthy({"healthy": "true"}) is True


def test_parse_status():
    # Invalid format
    assert parse_status({}) is False
    assert parse_status({"status": ""}) is False
    assert parse_status({"status": True}) is False

    # Valid but unhealthy
    assert parse_status({"status": "warn"}) is False
    assert parse_status({"status": "fail"}) is False
    assert parse_status({"status": "not_ok"}) is False

    # Valid and unhealthy
    assert parse_status({"status": "pass"}) is True
    assert parse_status({"status": "Pass"}) is True
    assert parse_status({"status": "ok"}) is True
    assert parse_status({"status": "up"}) is True


@patch("is_healthy.requests", autospec=True)
def test_check_health(mock_requests):
    mock_response = Mock()
    mock_requests.get.return_value = mock_response

    mock_response.text = json.dumps({"healthy": True})
    assert check_health('foo') is True

    mock_response.text = json.dumps({"healthy": True})
    assert check_health('foo', parser=parse_healthy) is True

    mock_response.text = json.dumps({"healthy": False})
    assert check_health('foo', parser=parse_healthy) is False

    mock_response.text = json.dumps({"status": "ok"})
    assert check_health('foo', parser=parse_status) is True

    with patch("is_healthy.json") as mock_json:
        mock_json.loads.side_effect = ValueError("foo")
        assert check_health('foo') is False

    mock_requests.get.side_effect = ConnectionError("foo")
    assert check_health('foo') is False

    mock_requests.get.side_effect = ReadTimeout("foo")
    assert check_health('foo') is False
