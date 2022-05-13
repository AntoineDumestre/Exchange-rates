import pandas as pd
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, datetime, timedelta

#-------------- Import des données --------------#
df = pd.read_csv("exchange_rates.csv")

df1 = df[~(df['symbol'] == 'BTC')]
df2 = df[df['symbol'] == 'BTC']

filtre_par_defaut = []

df_trend = pd.read_csv("trends.csv")

#-------------- Affichage global de la page --------------#
st.set_page_config(layout="wide")

## choix de la page : monnaies ou cryptomonnaies
with st.sidebar:
    page = st.selectbox("Page à afficher", ["Monnaies", "Cryptomonnaies"]) 
    if page == "Monnaies":
        df3 = df1
        filtre_par_defaut = ['USD','GBP','CHF','CAD']
    elif page == "Cryptomonnaies":
        df3 = df2
        filtre_par_defaut = ['BTC']

## Préparation des données
all_symbols = df3['symbol'].unique().tolist()
all_symbols.sort()

time_period= df3['date'].unique().tolist()
time_period.sort(reverse=False)

update_date = df3['date'].max()

#-------------- Affichage des filtres --------------#
st.title("Évolution des taux de change par rapport à l'Euro (€)")
st.markdown('Date de mise à jour : ' + update_date)

st.markdown("""---""")

st.subheader('Filtres')

selected_symbols = st.multiselect('Monnaies à afficher', all_symbols, default = filtre_par_defaut)

df_filtered = df3[df3['symbol'].isin(selected_symbols)]

max_display_date = df_filtered['date'].max()
min_display_date =  df_filtered['date'].min()
selected_period = st.select_slider('Choix de la période affichée', options=time_period, value=[min_display_date, max_display_date])
df_filtered = df_filtered[(df_filtered['date'] >= min(selected_period)) & (df_filtered['date'] <= max(selected_period))]

st.markdown("""---""")

#-------------- Affichage des graphes dans un container --------------#

st.subheader('Tendances')

c1 = st.container()

fig = px.line(df_filtered, x="date", y="value", color="currency", hover_name="currency", line_shape="spline", render_mode="svg")
c1.plotly_chart(fig, use_container_width=True)

#-------------- Affichage des tendances dans un container --------------#

specif = []
specif2=[]
for i in range(len(selected_symbols)):
    specif.append({"type": "domain"})
for j in range(4):
    specif2.append(specif)

fig = make_subplots(rows=len(selected_symbols), cols=4, specs=specif2)
#fig = go.Figure()
                    
for i in range(len(selected_symbols)):
    
    symbol = selected_symbols[i]
    v_last = round(float(df_trend[df_trend['symbol'] == symbol]['last_value']),2)
    v_oneday = round(float(df_trend[df_trend['symbol'] == symbol]['value_onedayago']),2)
    v_onemonth = round(float(df_trend[df_trend['symbol'] == symbol]['value_onemonthago']),2)
    v_oneyear = round(float(df_trend[df_trend['symbol'] == symbol]['value_oneyearago']),2)
        
    fig.add_trace(go.Indicator(
        mode = "number",
        value = v_last,
        #title = {"text": "<span style='font-size:0.8em;color:gray'>Current</span>"}),
        title = {"text": symbol}),
        row=i+1,col=1)

    fig.add_trace(go.Indicator(
        mode = "delta",
        value = v_last,
        title = {"text": "<span style='font-size:0.8em;color:gray'>1D</span>"},
        delta = {'reference': v_oneday, 'relative': True}),
        row=i+1,col=2)
        
    fig.add_trace(go.Indicator(
        mode = "delta",
        value = v_last,
        title = {"text": "<span style='font-size:0.8em;color:gray'>1M</span>"},
        delta = {'reference': v_onemonth, 'relative': True}),
        row=i+1,col=3)
            
    fig.add_trace(go.Indicator(
        mode = "delta",
        value = v_last,
        title = {"text": "<span style='font-size:0.8em;color:gray'>1Y</span>"},
        delta = {'reference': v_oneyear, 'relative': True}),
        row=i+1,col=4)

## tracé des tendances
#fig.update_layout(height=300, width=800)
st.plotly_chart(fig, use_container_width=True)



#-------------- Affichage des sources de données --------------#

with st.expander('Sources de données'):
        st.markdown('[La Banque de France](https://www.banque-france.fr/statistiques/taux-et-cours/les-taux-de-change-salle-des-marches/parites-quotidiennes)')
        st.markdown('[Yahoo Finance (BTC)](https://fr.finance.yahoo.com/quote/BTC-EUR/)')
        st.download_button('Télécharger les données', data=df.to_csv().encode('utf-8'), file_name="exchange_rates.csv", mime='text/csv')
