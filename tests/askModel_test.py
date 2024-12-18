import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper_funcs.askModel import Question


@pytest.mark.parametrize("input_sequence", ["ACDEFGHIKL", "MNPQRSTVWY"])
def test_valid_input(input_sequence):
    """Test valid amino acid sequences."""
    result = Question(input_sequence)
    assert isinstance(result, str), "Output should be a string."
    #assert result == "Mock output", "Unexpected mock output from the model."

@pytest.mark.parametrize("invalid_input", [123, 3.14, None, ["A", "C"], {"seq": "ACD"}])
def test_invalid_type(invalid_input):
    """Test non-string inputs."""
    with pytest.raises(ValueError, match="Input must be a string!"):
        Question(invalid_input)

@pytest.mark.parametrize("invalid_sequence", ["ACDEXYZ", "123ACD", "!@#"])
def test_invalid_characters(invalid_sequence):
    """Test inputs with invalid characters."""
    with pytest.raises(ValueError, match="Input contains invalid characters!"):
        Question(invalid_sequence)

@pytest.mark.parametrize("empty_sequence", [""])
def test_empty_input(empty_sequence):
    """Test empty or whitespace-only inputs."""
    with pytest.raises(ValueError, match="Input cannot be an empty string!"):
        Question(empty_sequence)
