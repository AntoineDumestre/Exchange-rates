import pandas as pd
import streamlit as st
import plotly_express as px
from datetime import date, datetime, timedelta

#-------------- Import des données --------------#
df = pd.read_csv("exchange_rates.csv")

df1 = df[~(df['symbol'] == 'BTC')]
df2 = df[df['symbol'] == 'BTC']

filtre_par_defaut = []

#-------------- Affichage global de la page --------------#
st.set_page_config(layout="wide")

#-------------- Choix de la page : monnaies ou cryptomonnaies --------------#
with st.sidebar:
    page = st.selectbox("Page à afficher", ["Monnaies", "Cryptomonnaies"]) 
    if page == "Monnaies":
        df3 = df1
        filtre_par_defaut = ['USD','GBP','CHF','CAD']
    elif page == "Cryptomonnaies":
        df3 = df2
        filtre_par_defaut = ['BTC']

#-------------- Préparation des données --------------#
all_symbols = df3['symbol'].unique().tolist()
all_symbols.sort()

time_period= df3['date'].unique().tolist()
time_period.sort(reverse=False)

update_date = df3['date'].max()

#-------------- Affichage des filtres --------------#
st.title("Évolution des taux de change par rapport à l'Euro (€)")
st.markdown('Date de mise à jour : ' + update_date)

col1, col2 = st.columns(2)

st.subheader('Filtres')

selected_symbols = col1.multiselect('Monnaies à afficher', all_symbols, default = filtre_par_defaut)

df_filtered = df3[df3['symbol'].isin(selected_symbols)]

max_display_date = df_filtered['date'].max()
min_display_date =  df_filtered['date'].min()
selected_period = col2.select_slider('Choix de la période affichée', options=time_period, value=[min_display_date, max_display_date])
df_filtered = df_filtered[(df_filtered['date'] >= min(selected_period)) & (df_filtered['date'] <= max(selected_period))]

#-------------- Affichage des graphes dans un container --------------#

c1 = st.container()

fig = px.line(df_filtered, x="date", y="value", color="currency", hover_name="currency", line_shape="spline", render_mode="svg")
c1.plotly_chart(fig, use_container_width=True)


#-------------- Affichage des sources de données --------------#

with st.expander('Sources de données'):
        st.markdown('[La Banque de France](https://www.banque-france.fr/statistiques/taux-et-cours/les-taux-de-change-salle-des-marches/parites-quotidiennes)')
        st.markdown('[Yahoo Finance (BTC)](https://fr.finance.yahoo.com/quote/BTC-EUR/)')
        st.download_button('Télécharger les données', data=df.to_csv().encode('utf-8'), file_name="exchange_rates.csv", mime='text/csv')
