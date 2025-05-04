from fastapi import HTTPException, Request
from settings.iphone_settings import MyIphoneSettings
from starlette.status import HTTP_403_FORBIDDEN

my_iphone_settings = MyIphoneSettings()

def verify_my_iphone_request(request: Request):
    expected_header_key = my_iphone_settings.expected_header_key
    expected_header_value = my_iphone_settings.expected_header_value

    actual_header_value = request.headers.get(expected_header_key, None)
    if actual_header_value != expected_header_value:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Unauthorized request.")
