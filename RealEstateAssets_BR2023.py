# Módulos/pacotes:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup Storytelling (matplotlib):
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.size'] = 8
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['figure.facecolor'] = '#464545' 
plt.rcParams['axes.facecolor'] = '#464545' 
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlecolor'] = 'black'
plt.rcParams['axes.titlesize'] = 9
plt.rcParams['axes.labelcolor'] = 'darkgray'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.2
plt.rcParams['ytick.color'] = 'darkgray'
plt.rcParams['xtick.color'] = 'darkgray'
plt.rcParams['axes.titlecolor'] = '#FFFFFF'
plt.rcParams['axes.titlecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.85
plt.rcParams['ytick.major.size'] = 0

# --- App (begin):
BR_real_estate_appreciation = pd.read_csv('BR_real_estate_appreciation_2023.csv')
BR_real_estate_appreciation['Valorizacao_anual_12m'] = round(BR_real_estate_appreciation['Valorizacao_anual_12m'], 2)*100
BR_real_estate_appreciation['BRL_metro_quad'] = BR_real_estate_appreciation['BRL_metro_quad']

# Page setup:
st.set_page_config(
    page_title="Imóveis Residencais (Brasil)",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Header:
st.markdown('### Valorização de imóveis residenciais no Brasil')

st.sidebar.markdown('''> **Como utilizar este aplicativo**

1. Selecionar uma cidade (*ponto verde*)
2. Comparar nos gráficos com as outras cidades (*pontos brancos*)
3. Comparar com a *média nacional* e com a distribuição dos dados
4. **Extrair insights:** valorização acima da média e preço abaixo = possível *oportunindade*
''')

# Widgets:
cities = sorted(list(BR_real_estate_appreciation['Cidade_estado'].unique()))
city_selection = st.selectbox(
    '🌎 Selecione uma cidade',
    cities
)

# City selection:
your_city = city_selection
selected_city = BR_real_estate_appreciation.query('Cidade_estado == @your_city')
other_cities = BR_real_estate_appreciation.query('Cidade_estado != @your_city')

# CHART 1: Annual appreciation (12 months):
chart_1, ax = plt.subplots(figsize=(3, 4.125))
# Background:
sns.stripplot(
    data= other_cities,
    y = 'Valorizacao_anual_12m',
    color = 'white',
    jitter=0.85,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
# Highlight:
sns.stripplot(
    data= selected_city,
    y = 'Valorizacao_anual_12m',
    color = '#00FF7F',
    jitter=0.15,
    size=12,
    linewidth=1,
    edgecolor='k',
    label=f'{your_city}'
)

# Showing up position measures:
avg_annual_val = BR_real_estate_appreciation['Valorizacao_anual_12m'].median()
q1__annual_val = np.percentile(BR_real_estate_appreciation['Valorizacao_anual_12m'], 25)
q3__annual_val = np.percentile(BR_real_estate_appreciation['Valorizacao_anual_12m'], 75)

# Plotting lines (reference):
ax.axhline(y=avg_annual_val, color='#DA70D6', linestyle='--', lw=0.75)
ax.axhline(y=q1__annual_val, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3__annual_val, color='white', linestyle='--', lw=0.75)

# Adding the labels for position measures:
ax.text(1.15, q1__annual_val, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.3, avg_annual_val, 'Mediana', ha='center', va='center', color='#DA70D6', fontsize=8, fontweight='bold')
ax.text(1.15, q3__annual_val, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# to fill the area between the lines:
ax.fill_betweenx([q1__annual_val, q3__annual_val], -2, 1, alpha=0.2, color='gray')
# to set the x-axis limits to show the full range of the data:
ax.set_xlim(-1, 1)

# Axes and titles:
plt.xticks([])
plt.ylabel('Valorização média %')
plt.title('Valorização (%) nos últimos 12 meses', weight='bold', loc='center', pad=15, color='gainsboro')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.tight_layout()


# CHART 2: Price (R$) by m²:
chart_2, ax = plt.subplots(figsize=(3, 3.95))
# Background:
sns.stripplot(
    data= other_cities,
    y = 'BRL_metro_quad',
    color = 'white',
    jitter=0.95,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
# Highlight:
sns.stripplot(
    data= selected_city,
    y = 'BRL_metro_quad',
    color = '#00FF7F',
    jitter=0.15,
    size=12,
    linewidth=1,
    edgecolor='k',
    label=f'{your_city}'
)

# Showing up position measures:
avg_price_m2 = BR_real_estate_appreciation['BRL_metro_quad'].median()
q1_price_m2 = np.percentile(BR_real_estate_appreciation['BRL_metro_quad'], 25)
q3_price_m2 = np.percentile(BR_real_estate_appreciation['BRL_metro_quad'], 75)

# Plotting lines (reference):
ax.axhline(y=avg_price_m2, color='#DA70D6', linestyle='--', lw=0.75)
ax.axhline(y=q1_price_m2, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_price_m2, color='white', linestyle='--', lw=0.75)

# Adding the labels for position measures:
ax.text(1.15, q1_price_m2, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.35, avg_price_m2, 'Mediana', ha='center', va='center', color='#DA70D6', fontsize=8, fontweight='bold')
ax.text(1.15, q3_price_m2, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# to fill the area between the lines:
ax.fill_betweenx([q1_price_m2, q3_price_m2], -2, 1, alpha=0.2, color='gray')
# to set the x-axis limits to show the full range of the data:
ax.set_xlim(-1, 1)

# Axes and titles:
plt.xticks([])
plt.ylabel('Preço (R\$)')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.title('Preço médio (R\$) por $m^2$', weight='bold', loc='center', pad=15, color='gainsboro')
plt.tight_layout()

# Splitting the charts into two columns:
left, right = st.columns(2)

# Columns (content):
with left:
    st.pyplot(chart_1)
with right:
    st.pyplot(chart_2)

# Informational text:
st.markdown('''
<span style="color:white;font-size:10pt"> ⚪ Cada ponto representa uma cidade </span>
<span style="color:#DA70D6;font-size:10pt"> ▫ <b> Valor médio </b></span>
<span style="color:white;font-size:10pt"> ◽ Valores menores (<b> fundo </b>)
◽ Valores maiores (<b> topo </b>) <br>
◽ **Q1** (primeiro quartil): representa 25% dos dados
◽ **Q3** (teceiro quartil): representa 75% dos dados
</span>

''',unsafe_allow_html=True)

# Showing up the numerical data (as a dataframe):
st.dataframe(
    BR_real_estate_appreciation.query('Cidade_estado == @your_city')[[
      'Cidade_estado', 'Valorizacao_anual_12m', 
      'BRL_metro_quad']]
)

# Adding some reference indexes:
st.markdown(''' > **REFEÊNCIAS (Valorização 12 meses):**

* IPCA: **6%**
* IGP-M: **4%**
* Índice FipeZAP+: **6%**

> Dados baseados nos informes FipeZAP (leva em conta imóveis residenciais para 50 cities brasilieras).
''')

# Authorship:
st.markdown('---')
st.markdown(''' **Criado por Vinícius Oviedo**  

*(mais informações na barra lateral - expandir)*

[![Linkedin Badge](https://img.shields.io/badge/-Linkedin-0A66C2?&logo=Linkedin&link=https://www.linkedin.com/in/vinicius-oviedo/)](https://www.linkedin.com/in/vinicius-oviedo/)
[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?&logo=Medium&link=https://github.com/OviedoVR)](https://github.com/OviedoVR)
[![Medium Badge](https://img.shields.io/badge/-Medium-green?&logo=Medium&link=https://medium.com/@vo.freelancer5)](https://medium.com/@vo.freelancer5/)
[![Website Badge](https://img.shields.io/badge/-Website-whitesmoke?&link=https://oviedovr.github.io/OviedoVR-ViniciusOviedo.github.io/)](https://oviedovr.github.io/OviedoVR-ViniciusOviedo.github.io/)
''')
st.markdown('---')
# --- (End of the App)
