import pandas as pd
import streamlit as st
import plotly_express as px

df = pd.read_csv("exchange_rates.csv")

all_symbols = df['symbol'].unique().tolist()
all_symbols.sort()
update_date = df['date'].max()

# Affichage du graphe
st.title("Évolution des taux de change par rapport à l'Euro (€)")
st.markdown('Date de mise à jour : ' + update_date)

selected_symbols = st.multiselect('Monnaies à afficher', all_symbols, default=['USD','GBP','CHF','CAD'])

df = df[df['symbol'].isin(selected_symbols)]
st.select_slider('Choix de la période affichée', min_value=df['Date'].min(), max_value=df['Date'].max(), value=df['Date'].unique().tolist())
          
fig = px.line(df, x="date", y="value", color="currency", hover_name="currency",
        line_shape="spline", render_mode="svg")
st.plotly_chart(fig, use_container_width=True)

          
st.markdown('[Data credit : La Banque de France](https://www.banque-france.fr/statistiques/taux-et-cours/les-taux-de-change-salle-des-marches/parites-quotidiennes)')

