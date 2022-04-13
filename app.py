import pandas as pd
import streamlit as st
import plotly_express as px

df = pd.read_csv("exchange_rates.csv")

all_symbols = df['symbol'].unique().tolist()
all_symbols.sort()


# Affichage du graphe
st.title("Évolution des taux de change par rapport à l'Euro (€)")
st.markdown('[Data credit : La Banque de France](https://www.banque-france.fr/statistiques/taux-et-cours/les-taux-de-change-salle-des-marches/parites-quotidiennes)')

selected_symbols = st.multiselect('Monnaies à afficher', all_symbols)

df = df[df['symbol'].isin(selected_symbols)]

fig = px.line(df, x="date", y="value", color="symbol", hover_name="currency",
        line_shape="spline", render_mode="svg")
st.plotly_chart(fig, use_container_width=True)
