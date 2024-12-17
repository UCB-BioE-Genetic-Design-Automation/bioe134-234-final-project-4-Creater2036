import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper_funcs.cleaner import cleaner  # Import the cleaner function

# Test 1: Happy Path - Correct Input
def test_cleaner_correct_input():
    data = {
        "Entry": ["A0A044RE18"],
        "Organism": ["Onchocerca volvulus"],
        "Length": [693],
        "Sequence": [
            "MYWQLVRILVLFDCLQKILAIEHDSICIADVDDACPEPSHTVMRLRERNDKKAHLIAKQHGLEIRGQPFLDGKSYFVTHISKQRSRRRKREIISRLQEHPDILSIEEQRPRVRRKRDFLYPDIAHELAGSSTNIRHTGLISNTEPRIDFIQHDAPVLPFPDPLYKEQWYLNNGAQGGFDMNVQAAWLLGYAGRNISVSILDDGIQRDHPDLAANYDPLASTDINGHDDDPTPQDDGDNKHGTRCAGEVASIAGNVYCGVGVAFHAKIGGVRMLDGPVSDSVEAASLSLNRHHIDIYSASWGPEDDGRTFDGPGPLAREAFYRGVKAGRGGKGSIFVWASGNGGSRQDSCSADGYTTSVYTLSVSSATIDNRSPWYLEECPSTIATTYSSANMNQPAIITVDVPHGCTRSHTGTSASAPLAAGIIALALEANPNLTWRDMQHIVLRTANPVPLLNNPGWSVNGVGRRINNKFGYGLMDAGALVKLALIWKTVPEQHICTYDYKLEKPNPRPITGNFQMNFSLEVNGCESGTPVLYLEHVQVLATFRFGKRGDLKLTLFSPRGTSSVLLPPRPQDFNSNGIHKWPFLSVQTWGEDPRGKWTLMVESVSTNRNVGGTFHDWSLLLYGTAEPAQPNDPRHSSVVPSSVSAESPFDRITQHIASQEKKKKQRDSRDWQPKKVENKKSLLVSAQPELRV"
        ],
        "Function [CC]": ["FUNCTION: Serine endoprotease which cleaves substrates at the RX(K/R)R consensus motif. {ECO:0000269|PubMed:12855702}."],
        "Subcellular location [CC]": ["SUBCELLULAR LOCATION: Secreted {ECO:0000305|PubMed:12855702}."],
        "Domain [CC]": ["None"],
        "Protein families": ["Peptidase S8 family, Furin subfamily"]
    }
    df = pd.DataFrame(data)

    expected_output = [
        [
            {'content': 'What information can you tell me about the protein sequence: MYWQLVRILVLFDCLQKILAIEHDSICIADVDDACPEPSHTVMRLRERNDKKAHLIAKQHGLEIRGQPFLDGKSYFVTHISKQRSRRRKREIISRLQEHPDILSIEEQRPRVRRKRDFLYPDIAHELAGSSTNIRHTGLISNTEPRIDFIQHDAPVLPFPDPLYKEQWYLNNGAQGGFDMNVQAAWLLGYAGRNISVSILDDGIQRDHPDLAANYDPLASTDINGHDDDPTPQDDGDNKHGTRCAGEVASIAGNVYCGVGVAFHAKIGGVRMLDGPVSDSVEAASLSLNRHHIDIYSASWGPEDDGRTFDGPGPLAREAFYRGVKAGRGGKGSIFVWASGNGGSRQDSCSADGYTTSVYTLSVSSATIDNRSPWYLEECPSTIATTYSSANMNQPAIITVDVPHGCTRSHTGTSASAPLAAGIIALALEANPNLTWRDMQHIVLRTANPVPLLNNPGWSVNGVGRRINNKFGYGLMDAGALVKLALIWKTVPEQHICTYDYKLEKPNPRPITGNFQMNFSLEVNGCESGTPVLYLEHVQVLATFRFGKRGDLKLTLFSPRGTSSVLLPPRPQDFNSNGIHKWPFLSVQTWGEDPRGKWTLMVESVSTNRNVGGTFHDWSLLLYGTAEPAQPNDPRHSSVVPSSVSAESPFDRITQHIASQEKKKKQRDSRDWQPKKVENKKSLLVSAQPELRV', "role": "user"},
            {"content": 'This sequence Serine endoprotease which cleaves substrates at the RXR consensus motif. Secreted. Peptidase S8 family, Furin subfamily.', "role": "assistant"}
        ]
    ]

    result = cleaner(df)
    assert result == expected_output

# Test 2: Incorrect DataFrame Columns
def test_cleaner_incorrect_columns():
    df = pd.DataFrame({"WrongColumn": [1, 2, 3]})
    with pytest.raises(ValueError, match="DataFrame does not have the right columns or is in incorrect order!"):
        cleaner(df)

# Test 3: Non-DataFrame Input
def test_cleaner_non_dataframe_input():
    non_df_input = "This is not a DataFrame"
    with pytest.raises(ValueError, match="df is not a pandas DataFrame!"):
        cleaner(non_df_input)

# Test 4: Missing Values in DataFrame
def test_cleaner_with_missing_values():
    data = {
        "Entry": ["A0A044RE18"],
        "Organism": ["Onchocerca volvulus"],
        "Length": [693],
        "Sequence": ["MSLEQKKGADIISKIL"],
        "Function [CC]": [None],
        "Subcellular location [CC]": [None],
        "Domain [CC]": [None],
        "Protein families": [None]
    }
    df = pd.DataFrame(data)

    expected_output = [
        [
            {"content": "What information can you tell me about the protein sequence: MSLEQKKGADIISKIL", "role": "user"},
            {"content": "This sequence ", "role": "assistant"}
        ]
    ]

    result = cleaner(df)
    assert result == expected_output

# Test 5: Empty DataFrame
def test_cleaner_empty_dataframe():
    df = pd.DataFrame(columns=["Entry", "Organism", "Length", "Sequence", "Function [CC]", "Subcellular location [CC]", "Domain [CC]", "Protein families"])
    result = cleaner(df)
    assert result == []

# Test 6: Multiple Rows
def test_cleaner_multiple_rows():
    data = {
        "Entry": ["A0A1", "A0A2"],
        "Organism": ["Organism1", "Organism2"],
        "Length": [100, 200],
        "Sequence": ["SEQ1", "SEQ2"],
        "Function [CC]": ["FUNCTION: Example1.", "FUNCTION: Example2."],
        "Subcellular location [CC]": ["SUBCELLULAR LOCATION: Example1.", "SUBCELLULAR LOCATION: Example2."],
        "Domain [CC]": ["None", "Domain Example2"],
        "Protein families": ["Family1", "Family2"]
    }
    df = pd.DataFrame(data)

    expected_output = [
        [
            {"content": "What information can you tell me about the protein sequence: SEQ1", "role": "user"},
            {"content": "This sequence Example1. Example1. Family1.", "role": "assistant"}
        ],
        [
            {"content": "What information can you tell me about the protein sequence: SEQ2", "role": "user"},
            {"content": "This sequence Example2. Example2. Domain Example2. Family2.", "role": "assistant"}
        ]
    ]

    result = cleaner(df)
    assert result == expected_output
