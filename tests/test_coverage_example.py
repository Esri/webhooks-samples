"""
Example test to demonstrate coverage functionality.
"""

import sys
from pathlib import Path

# Add the project root to the path so we can import sample code
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def sample_function(x, y):
    """Sample function for testing coverage."""
    if x > 0:
        return x + y
    else:
        return y - x


def untested_function(x):
    """This function won't be tested to show coverage gaps."""
    return x * 2


class TestCoverageExample:
    """Test class to demonstrate coverage reporting."""

    def test_sample_function_positive(self):
        """Test sample function with positive input."""
        result = sample_function(5, 3)
        assert result == 8

    def test_sample_function_negative(self):
        """Test sample function with negative input."""
        result = sample_function(-2, 3)
        assert result == 5

    def test_sample_function_zero(self):
        """Test sample function with zero input."""
        result = sample_function(0, 7)
        assert result == 7