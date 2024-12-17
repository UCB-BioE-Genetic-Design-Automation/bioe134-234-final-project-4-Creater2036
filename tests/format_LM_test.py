import pytest
from transformers import PreTrainedTokenizerFast
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper_funcs.format_LM import formatter_LLM # Import the formatter_LLM function
from unsloth import FastLanguageModel

# Load the tokenizer from Unsloth
@pytest.fixture(scope="module")
def unsloth_tokenizer():
    # Use a small tokenizer to reduce resource usage
    model_name = "unsloth/Llama-3.2-3B-Instruct"
    max_seq_length = 2048  # Set this as per your needs
    dtype = None  # Or use torch.float16/float32 as needed
    load_in_4bit = True

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
    )
    return tokenizer

# Test 1: Happy Path - Adding all amino acids as tokens
def test_formatter_LLM_all_amino_acids(unsloth_tokenizer):
    amino_acids = list("ACDEFGHIKLMNPQRSTVWY")

    updated_tokenizer = formatter_LLM(unsloth_tokenizer, amino_acids)

    # Ensure all amino acids are added to the tokenizer
    for aa in amino_acids:
        tokenized = updated_tokenizer.tokenize(aa)
        assert len(tokenized) == 1, f"Token '{aa}' not added correctly to tokenizer"

    # Test a sequence to confirm tokenization
    test_sequence = "ACDEFGHIKLMNPQRSTVWY"
    tokens = updated_tokenizer.tokenize(test_sequence)
    assert tokens == list(test_sequence), f"Tokenization failed: {tokens}"

# Test 2: Adding a subset of amino acids
def test_formatter_LLM_subset_amino_acids(unsloth_tokenizer):
    amino_acids = ["W", "K", "L"]

    updated_tokenizer = formatter_LLM(unsloth_tokenizer, amino_acids)

    # Ensure only specified amino acids are individually tokenized
    for aa in amino_acids:
        tokenized = updated_tokenizer.tokenize(aa)
        assert len(tokenized) == 1, f"Token '{aa}' not tokenized correctly"

    # Test mixed input
    test_sequence = "WKLXYZ"
    tokens = updated_tokenizer.tokenize(test_sequence)
    expected_tokens = ["W", "K", "L", "X", "Y", "Z"]  # Other letters may remain grouped
    assert tokens == expected_tokens, f"Unexpected tokenization: {tokens}"

# Test 3: Invalid amino_acids input (not a list)
def test_formatter_LLM_invalid_input(unsloth_tokenizer):
    with pytest.raises(ValueError, match="amino_acids parameter should be a list!"):
        formatter_LLM(unsloth_tokenizer, "ACDEFG")

# Test 4: Empty amino_acids list
def test_formatter_LLM_empty_list(unsloth_tokenizer):
    amino_acids = []

    updated_tokenizer = formatter_LLM(unsloth_tokenizer, amino_acids)
    test_sequence = "ACDEFG"
    tokens = updated_tokenizer.tokenize(test_sequence)

    # Tokenizer should behave as it originally does (no new tokens added)
    assert tokens == ["A", "C", "D", "E", "F", "G"], f"Unexpected tokenization: {tokens}"