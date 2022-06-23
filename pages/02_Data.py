import streamlit as st
from datetime import date
import foo
# %%
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
df = foo.df
variables = df.columns.tolist()
# %% SIDEBAR
st.sidebar.title("Options de Tri de la Table")
with st.sidebar:

    # SELECTION VARIABLES
    sel_variables = st.multiselect("Variables sélectionnées", ["Toutes les variables"] + variables,
                                   default="Toutes les variables")
    if "Toutes les variables" in sel_variables:
        sel_variables = df.columns.tolist()

with st.sidebar:

    # SECLECTION SOURCES
    sel_sources = st.multiselect("Sources sélectionnées",
                                 ["Toutes les sources"] + df.source.unique().tolist(),
                                 default="Toutes les sources")

    if "Toutes les sources" in sel_sources:
        sel_sources = df.source.unique().tolist()

    # SELECTION DES LIGNES
    number_of_line = st.slider('Nombre de lignes', 0, 500, 50)

layout = st.sidebar.columns([1, 1])

with layout[0]:
    dat_deb = st.date_input("Date de début", date(2016, 1, 1))

with layout[-1]:
    dat_fin = st.date_input("Date de fin", date.today())
# %%
df = df[(df['datePublicationDonnees'] >= str(dat_deb)) &
        (df['datePublicationDonnees'] <= str(dat_fin))]
df = df[df['source'].isin(sel_sources)].reset_index(drop=True)
df = df[sel_variables]
st.header(f"Nombre de Marchés dans le DataFrame sélectionne: {len(df)}")
df = df.loc[0:number_of_line]
st.dataframe(df)
