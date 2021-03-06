# %% Importations
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go


# %% Définition des variables globales et paramètres
# %%% Configuration des paramètres globaux des pages du streamlit
height_graph = 675
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# %%% Supression de la barre blanche en haut de page
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


# %%% Importation et mise en cache des données
@st.cache
def load_data():
    with open("data/decp_extracted.json", 'r+') as f:
        data_json = json.load(f)
    data = pd.DataFrame.from_dict(data_json)
    return data


data = load_data()

# %%% Récupération d'une liste de couleurs
color_set = px.colors.qualitative.Light24

# %% FIG 1
# %%% Création d'un DF de stock cumulatif du nombre de marchés par source pour FIG1
data_chart = data[["source", "datePublicationDonnees"]].sort_values(by="datePublicationDonnees")
data_chart = data_chart.groupby(by=['datePublicationDonnees', "source"]).size().to_frame()
data_chart = data_chart.reset_index()
for x in data.source.unique():
    data_chart[x] = data_chart[0][data_chart["source"] == x]
data_chart.set_index("datePublicationDonnees", inplace=True)
data_chart = data_chart[data.source.unique()].groupby(by="datePublicationDonnees").first()
data_chart = data_chart.fillna(0).cumsum().reset_index()
data_chart = data_chart.loc[data_chart['datePublicationDonnees'] >= "2018-01-01"]
# Pour le graph 1, on ne prend en compte que les marchés publiés à partir de 2018 pour des
# questions de lisibilité

# %%% Triage de la dernière ligne de data_chart afin de savoir dans quel ordre afficher les courbes
order_fig1 = data_chart.iloc[-1][1:].sort_values(ascending=False).index.tolist()
# %%% Création du graphique FIG1
fig1 = go.Figure()
for i in range(len(order_fig1)):
    fig1.add_trace(go.Scatter(x=data_chart['datePublicationDonnees'], y=data_chart[order_fig1[i]],
                              stackgroup='one', name=order_fig1[i], line=dict(color=color_set[i])))
fig1.update_layout(paper_bgcolor='rgb(245,245,245)', xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ), height=height_graph
)

# %% FIG 2
# %%% Création du dataframe source pour FIG 2
data_pie = data[["source"]]
data_pie = data_pie['source'].value_counts().to_frame().reset_index()
data_pie = data_pie.rename(columns={"index": "Source", "source": "Nombre de marchés"})

# %%% Création de FIG 2
fig2 = px.pie(data_pie, values="Nombre de marchés", names="Source", hole=0.5)
fig2.update_layout(paper_bgcolor='rgb(245,245,245)', height=height_graph)
fig2.update_traces(textposition='inside', textinfo='percent+label', showlegend=False,
                   direction="clockwise", marker=dict(colors=color_set[:len(data.source.unique())]))

# %% Historisation du nombre de marchés pour stats des
data_chart["total"] = data_chart.sum(axis=1)
historique = data_chart[["datePublicationDonnees", "total"]]
date_vector = pd.date_range(data_chart["datePublicationDonnees"].tolist()[0][0:10],
                            data_chart["datePublicationDonnees"].tolist()[-1][0:10]
                            ).strftime("%Y-%m-%d")
date_vector = date_vector.to_frame().reset_index(drop=True)
date_vector["datePublicationDonnees"] = date_vector[0]
final_hist = date_vector.merge(historique, how="left", on="datePublicationDonnees")
final_hist = final_hist.fillna(method='ffill')
final_hist = final_hist["total"].tolist()
# %% Création de la Page 1 du Streamlit
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
    st.metric("Marchés publiés", len(data))

with row1_2:
    st.metric("Marchés publiés les 10 derniers jours", int(final_hist[-1]-final_hist[-10]))

with row1_3:
    st.metric("Marchés publiés les 365 derniers jours", int(final_hist[-1]-final_hist[-365]))

with row1_4:
    st.metric("Nombre de sources", len(data.source.unique()))

row2_1, row2_2 = st.columns((1, 1))

with row2_1:
    st.header("Evolution du nombre de marchés")
    st.plotly_chart(fig1, use_container_width=True, use_container_height=True)

with row2_2:
    st.header('Répartition des marchés par source')
    st.plotly_chart(fig2, use_container_width=True)
