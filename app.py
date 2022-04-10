import pandas as pd
import streamlit as st
import plotly_express as px

df = pd.read_csv("exchange_rates.csv")

st.title("Évolution des taux de change par rapport à l'Euro (€)")

fig = px.line(df, x="date", y="value", color="currency", hover_name="symbol",
        line_shape="spline", render_mode="svg")
st.plotly_chart(fig, use_container_width=True)

st.markdown('[Data credit : La Banque de France](https://www.banque-france.fr/statistiques/taux-et-cours/les-taux-de-change-salle-des-marches/parites-quotidiennes)')
