def formatter_LLM(tokenizer, amino_acids):
  """
    Description: 
    Adds amino acids to the tokenizer vocabulary and forces model to consider amino acids as either alone tokens or in groups

    Input:
    tokenizer (transformers.tokenization_utils_fast.PreTrainedTokenizerFast)
    amino_acids (list): What amino acids to consider as individual tokens

    Output:
    tokenizer (transformers.tokenization_utils_fast.PreTrainedTokenizerFast): New tokenizer with correct vocabulary

    Tests:
    - Case: 
        Input: tokenizer, list("ACDEFGHIKLMNPQRSTVWY")
        Expected Output: (transformers.tokenization_utils_fast.PreTrainedTokenizerFast)
        Description: Tokenizer will now represent each amino acid as individual token
    - Case: 
        Input: tokenizer, list("WKL")
        Expected Output: (transformers.tokenization_utils_fast.PreTrainedTokenizerFast)
        Description: Tokenizer will now represent amino acids W, K, and L as inidivudal tokens but consider rest as grouped
        
    """
  if type(amino_acids) != list:
    raise ValueError("amino_acids parameter should be a list!")
  amino_acids = amino_acids # All amino acid letters
  tokenizer.add_tokens(amino_acids)

  # Resize the model's token embeddings to match the updated tokenizer
  return tokenizer