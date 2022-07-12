# %% Modules import
import pandas as pd
import json


# %% Json import
def load_data():
    data = pd.read_csv("data/data.csv", header=0, sep=";")
    return data


# %%
data = load_data()
dico = {'marches': [{k: v for k, v in m.items() if str(v) != 'nan'}
                    for m in data.to_dict(orient='records')]}

with open("data/decp.json", 'w') as f:
    json.dump(dico, f, indent=2, ensure_ascii=False)
