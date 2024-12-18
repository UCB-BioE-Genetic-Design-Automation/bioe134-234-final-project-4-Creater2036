from unsloth import FastLanguageModel
from transformers import TextStreamer
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
      model_name = "lora_model",
      max_seq_length = 6000,
      dtype = None,
      load_in_4bit = True,
  )
FastLanguageModel.for_inference(model)

valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")

def Question(amino_acid):
  if type(amino_acid) != str:
    raise ValueError("Input must be a string!")
  if not all(char in valid_amino_acids for char in amino_acid):
    raise ValueError("Input contains invalid characters! Only valid amino acid letters (A, C, D, etc.) are allowed.")
  if not amino_acid.strip():
    raise ValueError("Input cannot be an empty string!")
  
  messages = [
  {"role": "user", "content": f"What information can you tell me about the protein sequence: {amino_acid}"},
  ]
  device = "cuda" if torch.cuda.is_available() else "cpu"
  inputs = tokenizer.apply_chat_template(
      messages,
      tokenize = True,
      add_generation_prompt = True,
      return_tensors = "pt",
  ).to(device)
  print(f"Your question is: 'What information can you tell me about the protein sequence: {amino_acid}'")
  print("Predicted Answer:")
  text_streamer = TextStreamer(tokenizer, skip_prompt = True)
  _ = model.generate(input_ids = inputs, streamer = text_streamer, max_new_tokens = 128,
                    use_cache = True, temperature = 1.5, min_p = 0.1)
  return 'Done'