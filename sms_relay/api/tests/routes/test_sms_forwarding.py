from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from api.main import \
    app  # Assuming you have a FastAPI app instance in `main.py`
from database.models.forwarding.message import MessageResponse
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Initialize the FastAPI TestClient
    return TestClient(app)

# Test for the POST endpoint
def test_iphone_automation_hook(client, mock_get_db, mock_verify_my_iphone_request):
    # Prepare mock data
    sms_message = {
        "message": "Hello world",
        "phone_number": "+1234567890"
    }

    # Mock the DB interaction to simulate a successful DB call
    mock_message_response = MagicMock(spec=MessageResponse)
    mock_message_response.model_dump.return_value = {"id": str(uuid4()), "message": "Hello world", "phone_number": "+1234567890"}
    
    mock_get_db.return_value.create_forwarded_message.return_value = mock_message_response

    # Call the endpoint
    response = client.post("/forwarding/message", json=sms_message)

    # Assert the response status code and content
    assert response.status_code == 200
    assert response.json() == {"id": str(mock_message_response.model_dump.return_value['id']),
                               "message": "Hello world", 
                               "phone_number": "+1234567890"}

# Test for the GET endpoint
def test_message_detail(client, mock_get_db):
    # Mock a valid UUID and response data
    message_id = uuid4()
    mock_message_response = MagicMock(spec=MessageResponse)
    mock_message_response.model_dump.return_value = {"id": str(message_id), "message": "Hello world", "phone_number": "+1234567890"}

    # Mock the DB call to return a message with that ID
    mock_get_db.return_value.get.return_value = mock_message_response

    # Call the endpoint
    response = client.get(f"/forwarding/message/{message_id}")

    # Assert the response status code and content
    assert response.status_code == 200
    assert response.json() == {"id": str(message_id), "message": "Hello world", "phone_number": "+1234567890"}

