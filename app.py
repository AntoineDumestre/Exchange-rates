import pandas as pd
import streamlit as st
import plotly_express as px
from datetime import date, datetime, timedelta

# Import et Préparation des données 
df = pd.read_csv("exchange_rates.csv")

df1 = df[~(df['symbol'] == 'BTC')]
df2 = df[df['symbol'] == 'BTC']

all_symbols = df['symbol'].unique().tolist()
all_symbols.sort()

time_period= df['date'].unique().tolist()
time_period.sort(reverse=False)

update_date = df['date'].max()

# Affichage global de la page
st.set_page_config(layout="wide")

# Affichage des filtres
st.title("Évolution des taux de change par rapport à l'Euro (€)")
st.markdown('Date de mise à jour : ' + update_date)

with st.sidebar:
        st.subheader('Filtres')
        st.markdown('#')
        
        selected_symbols = st.multiselect('Monnaies à afficher', all_symbols, default=['USD','GBP','CHF','CAD','BTC'])
        df_filtered = df[df['symbol'].isin(selected_symbols)]
        df1_filtered = df1[df1['symbol'].isin(selected_symbols)]
        df2_filtered = df2[df2['symbol'].isin(selected_symbols)]
        
        
        st.markdown('#')
        
        max_display_date = df_filtered['date'].max()
        min_display_date =  df_filtered['date'].min()
        selected_period = st.select_slider('Choix de la période affichée', options=time_period, value=[min_display_date, max_display_date])
        df_filtered = df_filtered[(df_filtered['date'] >= min(selected_period)) & (df_filtered['date'] <= max(selected_period))]

# Affichage des graphes dans un container

col1, col2 = st.columns(2)

with col1:
        fig = px.line(df1_filtered, x="date", y="value", color="currency", hover_name="currency", line_shape="spline", render_mode="svg")
        st.plotly_chart(fig, use_container_width=True)

with col2:
        fig = px.line(df2_filtered, x="date", y="value", color="currency", hover_name="currency", line_shape="spline", render_mode="svg")
        st.plotly_chart(fig, use_container_width=True)

# Affichage des sources de données

with st.expander('Sources de données'):
        st.markdown('[La Banque de France](https://www.banque-france.fr/statistiques/taux-et-cours/les-taux-de-change-salle-des-marches/parites-quotidiennes)')
        st.markdown('[Yahoo Finance (BTC)](https://fr.finance.yahoo.com/quote/BTC-EUR/)')
        st.download_button('Télécharger les données', data=df.to_csv().encode('utf-8'), file_name="exchange_rates.csv", mime='text/csv')
