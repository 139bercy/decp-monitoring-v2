import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import date
import plotly.graph_objects as go
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
color_set = px.colors.qualitative.Light24
# %%
data_chart = data[["source", "datePublicationDonnees"]]
data_chart = data_chart.sort_values(by="datePublicationDonnees")
data_chart = data_chart.groupby(by=['datePublicationDonnees', "source"]).size().to_frame()
data_chart = data_chart.reset_index()
for x in data.source.unique():
    data_chart[x] = data_chart[0][data_chart["source"] == x]
data_chart.set_index("datePublicationDonnees", inplace=True)
data_chart = data_chart[data.source.unique()]
data_chart = data_chart.groupby(by="datePublicationDonnees").first()
data_chart = data_chart.fillna(0)
data_chart = data_chart.cumsum()
data_chart = data_chart.reset_index()
data_chart = data_chart.loc[data_chart['datePublicationDonnees'] >= "2018-01-01"]
# %%
order_fig1 = data_chart.iloc[-1][1:].sort_values(ascending=False).index.tolist()
# %%

fig1 = go.Figure()
for i in range(len(order_fig1)):
    fig1.add_trace(go.Scatter(x=data_chart['datePublicationDonnees'], y=data_chart[order_fig1[i]],
                              stackgroup='one', name=order_fig1[i], line=dict(color=color_set[i])))
fig1.update_layout(height=680, width=800, paper_bgcolor='rgb(245,245,245)')
# %%
data_pie = data[["id", "uid", "source", "montant"]]
data_pie = data_pie['source'].value_counts().to_frame().reset_index()
data_pie = data_pie.rename(columns={"index": "Source", "source": "Nombre de marchés"})
# %%

fig2 = px.pie(data_pie, values="Nombre de marchés", names="Source", hole=0.5)
fig2.update_layout(height=680, width=800, paper_bgcolor='rgb(245,245,245)')
fig2.update_traces(textposition='inside', textinfo='percent+label', showlegend=False,
                   direction="clockwise", marker=dict(colors=color_set[:len(data.source.unique())]))

# %%
data_chart["total"] = data_chart.sum(axis=1)
# %%
historique = data_chart[["datePublicationDonnees", "total"]]
date_vector = pd.date_range(data_chart["datePublicationDonnees"].tolist()[0],
                            data_chart["datePublicationDonnees"].tolist()[-1]).strftime("%Y-%m-%d")
date_vector = date_vector.to_frame().reset_index(drop=True)
date_vector["datePublicationDonnees"] = date_vector[0]
final_hist = date_vector.merge(historique, how="left", on="datePublicationDonnees")
final_hist = final_hist.fillna(method='ffill')
final_hist = final_hist["total"].tolist()
# %%
st.title("Données essentielles de la commande publique")
row1_1, row1_2, row1_3, row1_4 = st.columns((1, 1, 1, 1))

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgb(245, 245, 245);
   border: 1px solid rgb(245, 245, 245);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: rgb(255, 75, 75);
}
</style>
""", unsafe_allow_html=True)

with row1_1:
    st.metric("Marchés publiés", str(len(data)))

with row1_2:
    st.metric("Marchés publiés les 10 derniers jours", int(final_hist[-1]-final_hist[-10]))

with row1_3:
    st.metric("Marchés publiés les 365 derniers jours", int(final_hist[-1]-final_hist[-365]))

with row1_4:
    st.metric("A définir", 1)

row2_1, row2_2 = st.columns((2, 2))

with row2_1:
    st.header("Evolution du nombre de marchés")
    st.plotly_chart(fig1)

with row2_2:
    st.header('Répartition des marchés par source')
    st.plotly_chart(fig2)
