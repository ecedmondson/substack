import pytest

from fastapi import HTTPException
from starlette.requests import Request

from api.security.verify_my_iphone import verify_my_iphone_request

class TestVerifyMyIphoneRequest:
    @pytest.fixture
    def valid_headers(self):
        return Request({
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [(b"x-iphone-api-key", b"iphonesecretvalue")],
            "query_string": b"",
            "app": None,
        })

    @pytest.fixture
    def invalid_header_value(self):
        return Request({
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [(b"x-iphone-api-key", b"iphonesecretvaluebutincorrectnow")],
            "query_string": b"",
            "app": None,
        })

    @pytest.fixture
    def empty_header(self):
        return Request({
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [],
            "query_string": b"",
            "app": None,
        })

    def test_valid_headers_do_not_raise_error(self, valid_headers):
        verify_my_iphone_request(valid_headers)

    def test_invalid_header_value_raises_error(self, invalid_header_value):
        with pytest.raises(HTTPException):
            verify_my_iphone_request(invalid_header_value)

    def test_empty_headers_raises_error(self, invalid_header_value):
        with pytest.raises(HTTPException):
            verify_my_iphone_request(invalid_header_value)
