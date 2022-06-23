import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import foo

# %%
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


@st.cache
def load_data():
    with open("data/decp.json", 'r+') as f:
        data_json = json.load(f)
    data_json = data_json["marches"]
    data = pd.DataFrame.from_dict(data_json)
    data = data.loc[data['datePublicationDonnees'] >= "2016-01-01"]
    data = data.loc[data['datePublicationDonnees'] <= str(date.today())]
    data = data.astype(str)
    return data


data = load_data()
foo.df = data
# %%
data_chart = data[["source", "datePublicationDonnees"]]
data_chart = data_chart.sort_values(by="datePublicationDonnees")
data_chart = data_chart.groupby(by=['datePublicationDonnees']).size().to_frame()
# liste_source = data_chart["source"].unique()
# %%
# Load data
fig1 = go.Figure(data=[go.Histogram(x=data_chart[0], cumulative_enabled=True)])
fig1.update_layout(height=680, width=800, paper_bgcolor='rgb(245,245,245)')

# %%
data_pie = data[["id", "uid", "source", "montant"]]
data_pie = data_pie['source'].value_counts().to_frame().reset_index()
data_pie = data_pie.rename(columns={"index": "Source", "source": "Nombre de marchés"})
# %%

fig2 = px.pie(data_pie, values="Nombre de marchés", names="Source", hole=0.5,
              title='Répartition des marchés par source')
fig2.update_layout(height=680, width=800, paper_bgcolor='rgb(245,245,245)')
fig2.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)

# %%
# st.title("Données essentielles de la commande publique")
row1_1, row1_2, row1_3, row1_4 = st.columns((1, 1, 1, 1))
with row1_1:
    st.metric("Marchés publiés", str(len(data)))

with row1_2:
    st.write("marchés publiés les 10 derniers jours")

with row1_3:
    st.write("marchés publiés les 365 derniers jours")

with row1_4:
    st.write("partenaires sans données depuis 10 jours")

row2_1, row2_2 = st.columns((2, 2))

with row2_1:
    # st.header("Evolution du nombre de marchés par source")
    st.plotly_chart(fig1, height=680, width=800)

with row2_2:
    # st.header('Répartition des marchés par source')
    st.plotly_chart(fig2, height=680, width=800)
