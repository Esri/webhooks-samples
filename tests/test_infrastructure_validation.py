"""
Infrastructure validation tests to ensure testing setup works correctly.
"""

import json
import os
import sys
from pathlib import Path

import pytest


class TestInfrastructureValidation:
    """Test suite to validate the testing infrastructure setup."""

    def test_pytest_is_working(self):
        """Test that pytest is functioning correctly."""
        assert True

    def test_pytest_markers_registered(self, pytestconfig):
        """Test that custom markers are properly registered."""
        markers = pytestconfig.getini("markers")
        markers_str = str(markers)
        expected_markers = ["unit", "integration", "slow"]
        for marker in expected_markers:
            assert marker in markers_str, f"Marker '{marker}' not found in registered markers"

    def test_python_path_includes_project_dirs(self):
        """Test that Python path includes project directories."""
        project_root = Path(__file__).parent.parent
        assert project_root.exists()
        
        # Check that we can import from the project structure
        sys.path.insert(0, str(project_root))
        
        # Test that we can access the project directories
        developer_dir = project_root / "Developer"
        sample_workflows_dir = project_root / "sample-workflows"
        
        assert developer_dir.exists(), "Developer directory should exist"
        assert sample_workflows_dir.exists(), "sample-workflows directory should exist"

    @pytest.mark.unit
    def test_unit_marker_works(self):
        """Test that the unit marker works correctly."""
        assert True

    @pytest.mark.integration
    def test_integration_marker_works(self):
        """Test that the integration marker works correctly."""
        assert True

    @pytest.mark.slow
    def test_slow_marker_works(self):
        """Test that the slow marker works correctly."""
        assert True

    def test_mock_fixture_works(self, mock_config):
        """Test that the mock_config fixture works."""
        assert isinstance(mock_config, dict)
        assert "debug" in mock_config
        assert "host" in mock_config
        assert "port" in mock_config

    def test_temp_dir_fixture_works(self, temp_dir):
        """Test that the temp_dir fixture works."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test we can create files in the temp directory
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.read_text() == "test content"

    def test_json_file_fixture_works(self, json_file):
        """Test that the json_file fixture works."""
        test_data = {"test": "data", "number": 42}
        file_path = json_file(test_data, "validation.json")
        
        assert file_path.exists()
        with open(file_path, "r") as f:
            loaded_data = json.load(f)
        assert loaded_data == test_data

    def test_sample_webhook_payload_fixture(self, sample_webhook_payload):
        """Test that the sample_webhook_payload fixture works."""
        assert isinstance(sample_webhook_payload, dict)
        assert "webhookId" in sample_webhook_payload
        assert "eventType" in sample_webhook_payload
        assert "features" in sample_webhook_payload
        assert isinstance(sample_webhook_payload["features"], list)

    def test_mock_environment_variables_fixture(self, mock_environment_variables):
        """Test that environment variables fixture works."""
        assert isinstance(mock_environment_variables, dict)
        assert "AZURE_STORAGE_CONNECTION_STRING" in mock_environment_variables
        assert "SLACK_BOT_TOKEN" in mock_environment_variables
        
        # Verify environment variables are actually set
        for key in mock_environment_variables:
            assert os.getenv(key) is not None

    def test_project_structure_exists(self):
        """Test that the expected project structure exists."""
        project_root = Path(__file__).parent.parent
        
        # Check main directories
        assert (project_root / "Developer").exists()
        assert (project_root / "sample-workflows").exists()
        assert (project_root / "tests").exists()
        assert (project_root / "tests" / "unit").exists()
        assert (project_root / "tests" / "integration").exists()
        
        # Check configuration files
        assert (project_root / "pyproject.toml").exists()
        assert (project_root / ".gitignore").exists()
        assert (project_root / "tests" / "conftest.py").exists()

    def test_coverage_configuration(self):
        """Test that coverage configuration is set up correctly."""
        import coverage
        
        # This just tests that coverage can be imported and initialized
        cov = coverage.Coverage()
        assert cov is not None

    def test_pytest_mock_available(self):
        """Test that pytest-mock is available."""
        pytest_mock = pytest.importorskip("pytest_mock")
        assert pytest_mock is not None


class TestFixtureValidation:
    """Additional tests specifically for fixture validation."""

    def test_all_mock_fixtures_available(self, mock_config, mock_azure_function_context, 
                                       mock_azure_function_request, mock_flask_app,
                                       mock_requests_session, mock_slack_client,
                                       mock_hash_validator):
        """Test that all mock fixtures are available and working."""
        fixtures = {
            "mock_config": mock_config,
            "mock_azure_function_context": mock_azure_function_context,
            "mock_azure_function_request": mock_azure_function_request,
            "mock_flask_app": mock_flask_app,
            "mock_requests_session": mock_requests_session,
            "mock_slack_client": mock_slack_client,
            "mock_hash_validator": mock_hash_validator,
        }
        
        for name, fixture in fixtures.items():
            assert fixture is not None, f"Fixture {name} should not be None"

    def test_sample_data_fixtures(self, sample_webhook_payload, sample_arcgis_changes):
        """Test that sample data fixtures contain expected structure."""
        # Webhook payload validation
        assert "webhookId" in sample_webhook_payload
        assert "eventType" in sample_webhook_payload
        assert "features" in sample_webhook_payload
        
        # ArcGIS changes validation
        assert "changes" in sample_arcgis_changes
        assert "exceededTransferLimit" in sample_arcgis_changes
        assert isinstance(sample_arcgis_changes["changes"], list)