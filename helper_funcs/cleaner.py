import re
import pandas as pd
def cleaner(df):
  """
    Description: 
    Puts data into conversational format where user gives question in content and then model will respond in its content.
    Along with this, cleans up data so it can be put into readable format for model.

    Input:
    df (pd.DataFrame): A DataFrame with columns: ['Entry', 'Organism', 'Length', 'Sequence', 'Function [CC]',
       'Subcellular location [CC]', 'Domain [CC]', 'Protein families']

    Output:
    master_lst list: Cleaned List containing user input content and content of what model should output

    Tests:
    - Case: 
        Input: DataFrame with specified columns and row of ['A0A044RE18',
        'Onchocerca volvulus',
        693,
        'MYWQLVRILVLFDCLQKILAIEHDSICIADVDDACPEPSHTVMRLRERNDKKAHLIAKQHGLEIRGQPFLDGKSYFVTHISKQRSRRRKREIISRLQEHPDILSIEEQRPRVRRKRDFLYPDIAHELAGSSTNIRHTGLISNTEPRIDFIQHDAPVLPFPDPLYKEQWYLNNGAQGGFDMNVQAAWLLGYAGRNISVSILDDGIQRDHPDLAANYDPLASTDINGHDDDPTPQDDGDNKHGTRCAGEVASIAGNVYCGVGVAFHAKIGGVRMLDGPVSDSVEAASLSLNRHHIDIYSASWGPEDDGRTFDGPGPLAREAFYRGVKAGRGGKGSIFVWASGNGGSRQDSCSADGYTTSVYTLSVSSATIDNRSPWYLEECPSTIATTYSSANMNQPAIITVDVPHGCTRSHTGTSASAPLAAGIIALALEANPNLTWRDMQHIVLRTANPVPLLNNPGWSVNGVGRRINNKFGYGLMDAGALVKLALIWKTVPEQHICTYDYKLEKPNPRPITGNFQMNFSLEVNGCESGTPVLYLEHVQVLATFRFGKRGDLKLTLFSPRGTSSVLLPPRPQDFNSNGIHKWPFLSVQTWGEDPRGKWTLMVESVSTNRNVGGTFHDWSLLLYGTAEPAQPNDPRHSSVVPSSVSAESPFDRITQHIASQEKKKKQRDSRDWQPKKVENKKSLLVSAQPELRV',
        'FUNCTION: Serine endoprotease which cleaves substrates at the RX(K/R)R consensus motif. {ECO:0000269|PubMed:12855702}.',
        'SUBCELLULAR LOCATION: Secreted {ECO:0000305|PubMed:12855702}.',
        'None',
        'Peptidase S8 family, Furin subfamily']
        Expected Output: 
        {'conversations': [{'content': 'What information can you tell me about the protein sequence: MYWQLVRILVLFDCLQKILAIEHDSICIADVDDACPEPSHTVMRLRERNDKKAHLIAKQHGLEIRGQPFLDGKSYFVTHISKQRSRRRKREIISRLQEHPDILSIEEQRPRVRRKRDFLYPDIAHELAGSSTNIRHTGLISNTEPRIDFIQHDAPVLPFPDPLYKEQWYLNNGAQGGFDMNVQAAWLLGYAGRNISVSILDDGIQRDHPDLAANYDPLASTDINGHDDDPTPQDDGDNKHGTRCAGEVASIAGNVYCGVGVAFHAKIGGVRMLDGPVSDSVEAASLSLNRHHIDIYSASWGPEDDGRTFDGPGPLAREAFYRGVKAGRGGKGSIFVWASGNGGSRQDSCSADGYTTSVYTLSVSSATIDNRSPWYLEECPSTIATTYSSANMNQPAIITVDVPHGCTRSHTGTSASAPLAAGIIALALEANPNLTWRDMQHIVLRTANPVPLLNNPGWSVNGVGRRINNKFGYGLMDAGALVKLALIWKTVPEQHICTYDYKLEKPNPRPITGNFQMNFSLEVNGCESGTPVLYLEHVQVLATFRFGKRGDLKLTLFSPRGTSSVLLPPRPQDFNSNGIHKWPFLSVQTWGEDPRGKWTLMVESVSTNRNVGGTFHDWSLLLYGTAEPAQPNDPRHSSVVPSSVSAESPFDRITQHIASQEKKKKQRDSRDWQPKKVENKKSLLVSAQPELRV',
        'role': 'user'},
        {'content': 'This sequence Serine endoprotease which cleaves substrates at the RXR consensus moti. Secreted. Peptidase S8 family, Furin subfamil.',
        'role': 'assistant'}]}
        Description: Example of usage for one row
    """
  master_lst = []
  if type(df) != pd.core.frame.DataFrame:
    raise ValueError("df is not a pandas DataFrame!")
  if list(df.columns) != ['Entry','Organism','Length','Sequence','Function [CC]','Subcellular location [CC]','Domain [CC]','Protein families']:
    raise ValueError("DataFrame does not have the right columns or is in incorrect order!")
  df = df.fillna('None')
  for row in range(len(df)):
    lst = []
    part = df.iloc[row].to_dict()
    lst.append({'content':f"What information can you tell me about the protein sequence: {part['Sequence']}", 'role': 'user'})

    vals = list(part.values())[4:]
    ans = ""
    for val in vals:
      if val == 'None':
        #ans.append('Not available')
        pass
      else:
        cleaned = re.sub(r"^[^:]*:\s*", "", val)
        cleaned = re.sub(r"\([^)]*\)", "", cleaned)
        cleaned = re.sub(r"\{[^}]*\}", "", cleaned)
        cleaned = re.sub(r"\.\s*\.", ".", cleaned)
        cleaned = cleaned.strip().rstrip(".")
        cleaned = re.sub(r"\s+([.,!?;:])", r"\1", cleaned)
        cleaned = cleaned + '.'
        #cleaned = cleaned.replace('  ', ' ')
        ans += ' ' + cleaned
    #ans = tool.correct(ans)
    ans = 'This sequence ' + ans
    ans = ans.replace('  ', ' ')
    ans = ans.replace(' .', '.')
    lst.append({'content':ans, 'role':'assistant'})

    master_lst.append(lst)
  return master_lst