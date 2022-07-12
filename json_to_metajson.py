# %% Modules import
import json
import pandas as pd
from datetime import date


# %% Json import
with open("data/decp.json", 'r+') as f:
    data_json = json.load(f)
    data_json = data_json["marches"]
data = pd.DataFrame.from_dict(data_json)
data = data.astype(str)
data = data.loc[data['datePublicationDonnees'] >= "2016-01-01"]
data = data.loc[data['datePublicationDonnees'] <= str(date.today())]
data = data.drop_duplicates()
data = data[["source", "datePublicationDonnees"]]

# %% Json export
data.to_json(r'data/decp_extracted.json')
