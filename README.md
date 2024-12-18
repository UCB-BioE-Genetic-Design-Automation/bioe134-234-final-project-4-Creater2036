# Genetic Frame Final Project Submission

## Project Overview
This project provides core bioinformatics utilities for analyzing protein sequences and improving the tokenization process for transformer models. The focus is on automating sequence data preparation for large language models (LLMs) in bioinformatics applications. The main part of this model is done in the ipynb notebook and individual functions are listed out here along with their uses. Lora_model is provided as well to view the end result.

The project includes the following functionalities:
1. **Cleaner**: Converts protein data into a conversational format for LLMs and cleans up data for better readability.
2. **Formatter_LLM**: Updates the tokenizer to treat amino acids as individual tokens for LLMs, improving the handling of protein sequences in transformer models.
3. **Genetic_Frame_Final_Proj.ipynb**: Main notebook. Goes through data downloading process, preprocessing, tokenizing data, putting into Llama format, training LLama model, and testing model with the help of the 2 functions above.

Both functions are designed to preprocess protein sequences, enabling efficient model training and data analysis for bioinformatics tasks.

## Scope of Work
For this final project, I developed two functions aimed at simplifying the preprocessing of protein data for large language models, along with the notebook:
1. **Cleaner**: This function processes protein data, converting it into a format that LLMs can understand. The function takes a dataset and cleans it by removing unnecessary information while structuring it as a dialogue between a user and a model.
   
2. **Formatter_LLM**: This function updates the tokenizer to treat individual amino acids as distinct tokens. This is crucial for improving how protein sequences are tokenized, ensuring that each amino acid is processed correctly by the model.
   
3. **Genetic_Frame_Final_Proj.ipynb**: Notebook implements fine tuning to tune Llama so it can understand protein sequencing data and predict the function of a protein given its amino acid sequence.
   
4. **Lora_model**: Resulting Llama model created from training the data. The last cells of the Jupyter notebook show how the model is used. When given a proteins amino acid sequence, the model will predict the functionality, subcellular location, domain, and family of the given protein

## Function Descriptions

### 1. Cleaner (`cleaner`)
**Description**: This function transforms protein data into a conversational format suitable for LLMs. It cleans up data by removing unnecessary information and structures it into a question-response format.

- **Input**: A pandas DataFrame containing protein information such as `Entry`, `Organism`, `Sequence`, `Function`, `Subcellular Location`, `Domain`, and `Protein Families`.
- **Output**: A list of conversational pairs where the user asks about a protein sequence, and the model responds with relevant information about the protein.
  
**Example**:

```python
cleaner(df)
# Returns: [{'content': 'What information can you tell me about the protein sequence: ...', 'role': 'user'}, 
#            {'content': 'This sequence...', 'role': 'assistant'}]
```
### 2. Formatter_LLM (`formatter_LLM`)
**Description**: This function modifies a tokenizer by adding amino acids as individual tokens, enabling the tokenizer to handle protein sequences more accurately in a transformer model.

- **Input**: A tokenizer (from FastLanguageModel) and a list of amino acids to treat as individual tokens.
- **Output**: A tokenizer updated with new tokens for the specified amino acids.
**Example**:

```python
formatter_LLM(tokenizer, ["A", "C", "D", "E"])
# Returns: Updated tokenizer with amino acids A, C, D, E as individual tokens
```
## Error Handling

### Cleaner
- **Raises `ValueError`** if the input DataFrame does not have the required columns or is not in the correct format.

### Formatter_LLM
- **Raises `ValueError`** if the `amino_acids` parameter is not provided as a list.

## Testing
Both functions have been thoroughly tested with various input cases, including standard, edge, and invalid cases. Testing was implemented using **pytest**.

### Test Files:
- `tests/test_cleaner.py`
- `tests/test_formatter.py`

The tests include:
- Valid protein sequences.
- Sequences with missing or invalid data.
- Validation of tokenizer behavior for different amino acids.
- Proper error handling for incorrect input types.

## Usage Instructions
To use these utilities, clone the repository and install the required dependencies.

1. **Clone the repository**:
   ```bash
   git clone <your-github-repo-url>

Install dependencies: requirements.txt file
```bash
pip install -r requirements.txt
```

## Example Usage

1. **Clone the repository** and install dependencies as described in the usage instructions.

2. **Example usage**:

```python
from helper_funcs.cleaner_function import cleaner
from helper_funcs.formatter_function import formatter_LLM

# Example DataFrame for cleaner
import pandas as pd
df = pd.DataFrame({
    'Entry': ['A0A044RE18'],
    'Organism': ['Onchocerca volvulus'],
    'Length': [693],
    'Sequence': ['MYWQLVRILVLFDCLQKILAIEHDSICIADVDDACPEPSHTVMRLRERNDKKAHLIAKQHGLEIRGQPFLDGKSYFVTHISKQRSRRRKREIISRLQEHPDILSIEEQRPRVRRKRDFLYPDIAHELAGSSTNIRHTGLISNTEPRIDFIQHDAPVLPFPDPLYKEQWYLNNGAQGGFDMNVQAAWLLGYAGRNISVSILDDGIQRDHPDLAANYDPLASTDINGHDDDPTPQDDGDNKHGTRCAGEVASIAGNVYCGVGVAFHAKIGGVRMLDGPVSDSVEAASLSLNRHHIDIYSASWGPEDDGRTFDGPGPLAREAFYRGVKAGRGGKGSIFVWASGNGGSRQDSCSADGYTTSVYTLSVSSATIDNRSPWYLEECPSTIATTYSSANMNQPAIITVDVPHGCTRSHTGTSASAPLAAGIIALALEANPNLTWRDMQHIVLRTANPVPLLNNPGWSVNGVGRRINNKFGYGLMDAGALVKLALIWKTVPEQHICTYDYKLEKPNPRPITGNFQMNFSLEVNGCESGTPVLYLEHVQVLATFRFGKRGDLKLTLFSPRGTSSVLLPPRPQDFNSNGIHKWPFLSVQTWGEDPRGKWTLMVESVSTNRNVGGTFHDWSLLLYGTAEPAQPNDPRHSSVVPSSVSAESPFDRITQHIASQEKKKKQRDSRDWQPKKVENKKSLLVSAQPELRV'],
    'Function [CC]': ['FUNCTION: Serine endoprotease which cleaves substrates at the RX(K/R)R consensus motif. {ECO:0000269|PubMed:12855702}.'],
    'Subcellular location [CC]': ['SUBCELLULAR LOCATION: Secreted {ECO:0000305|PubMed:12855702}.'],
    'Domain [CC]': ['None'],
    'Protein families': ['Peptidase S8 family, Furin subfamily']
})

# Clean the data
cleaned_data = cleaner(df)

# Tokenizer example for formatter_LLM
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True
)

# Update tokenizer with amino acids
updated_tokenizer = formatter_LLM(tokenizer, ["A", "C", "D", "E"])

print(cleaned_data)
```
## Conclusion
These functions provide foundational utilities for working with protein sequences and enhancing the tokenization process for large language models in bioinformatics. They have been thoroughly tested and are ready for integration into bioinformatics pipelines.

