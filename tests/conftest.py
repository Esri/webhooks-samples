"""
Shared pytest fixtures for webhook samples testing.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "debug": True,
        "host": "localhost",
        "port": 5000,
        "webhook_secret": "test-secret-key",
        "azure_connection_string": "test-connection-string",
        "slack_token": "test-slack-token",
    }


@pytest.fixture
def sample_webhook_payload():
    """Sample webhook payload for testing."""
    return {
        "webhookId": "test-webhook-123",
        "eventType": "FeaturesCreated",
        "serviceName": "TestService",
        "layerId": 0,
        "changesUrl": "https://services.arcgis.com/test/changes",
        "when": 1234567890000,
        "features": [
            {
                "attributes": {"OBJECTID": 1, "Name": "Test Feature"},
                "geometry": {"x": -122.0, "y": 37.0}
            }
        ]
    }


@pytest.fixture
def mock_azure_function_context():
    """Mock Azure Functions context for testing."""
    context = Mock()
    context.invocation_id = "test-invocation-123"
    context.function_name = "TestFunction"
    context.function_directory = "/test/function"
    context.trace_context = Mock()
    context.retry_context = Mock()
    return context


@pytest.fixture
def mock_azure_function_request():
    """Mock Azure Functions HTTP request for testing."""
    request = Mock()
    request.method = "POST"
    request.url = "https://test.azurewebsites.net/api/webhook"
    request.headers = {"Content-Type": "application/json"}
    request.get_body = Mock(return_value=b'{"test": "data"}')
    request.get_json = Mock(return_value={"test": "data"})
    return request


@pytest.fixture
def mock_flask_app():
    """Mock Flask application for testing."""
    from unittest.mock import MagicMock
    app = MagicMock()
    app.config = {"TESTING": True, "SECRET_KEY": "test-key"}
    app.test_client = Mock()
    return app


@pytest.fixture
def mock_requests_session():
    """Mock requests session for HTTP calls."""
    session = Mock()
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"success": True}
    response.text = '{"success": true}'
    session.get.return_value = response
    session.post.return_value = response
    session.put.return_value = response
    session.delete.return_value = response
    return session


@pytest.fixture
def mock_slack_client():
    """Mock Slack client for testing."""
    client = Mock()
    client.api_call.return_value = {"ok": True, "channel": "C1234567890"}
    client.files_upload.return_value = {"ok": True, "file": {"id": "F1234567890"}}
    return client


@pytest.fixture
def sample_arcgis_changes():
    """Sample ArcGIS changes data for testing."""
    return {
        "changes": [
            {
                "id": 1,
                "changeType": "insert",
                "geometry": {"x": -122.0, "y": 37.0},
                "attributes": {"OBJECTID": 1, "Name": "New Feature"}
            },
            {
                "id": 2,
                "changeType": "update",
                "geometry": {"x": -122.1, "y": 37.1},
                "attributes": {"OBJECTID": 2, "Name": "Updated Feature"}
            }
        ],
        "exceededTransferLimit": False
    }


@pytest.fixture
def mock_environment_variables(monkeypatch):
    """Set up mock environment variables for testing."""
    env_vars = {
        "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=test;EndpointSuffix=core.windows.net",
        "SLACK_BOT_TOKEN": "xoxb-test-token",
        "WEBHOOK_SECRET": "test-webhook-secret",
        "DEBUG": "true"
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    return env_vars


@pytest.fixture
def json_file(temp_dir):
    """Create a temporary JSON file for testing."""
    def _create_json_file(data: Dict[str, Any], filename: str = "test.json") -> Path:
        file_path = temp_dir / filename
        with open(file_path, "w") as f:
            json.dump(data, f)
        return file_path
    
    return _create_json_file


@pytest.fixture
def mock_hash_validator():
    """Mock hash validator for webhook security testing."""
    validator = Mock()
    validator.validate_signature.return_value = True
    validator.generate_signature.return_value = "test-signature"
    return validator


@pytest.fixture(autouse=True)
def reset_modules():
    """Reset any cached modules between tests."""
    import sys
    modules_to_reset = [m for m in sys.modules.keys() if m.startswith(('Developer', 'sample-workflows'))]
    for module in modules_to_reset:
        if module in sys.modules:
            del sys.modules[module]