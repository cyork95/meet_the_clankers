import pytest
from src.script_generator import generate_script

def test_generate_script_empty_input():
    """Test that empty input returns an empty list or handles it gracefully."""
    script = generate_script({})
    assert isinstance(script, list)
    assert len(script) == 0 # Should probably return empty or a default intro

# Note: Testing generate_script with real input requires an API key.
# We should mock the API call for a proper unit test.
