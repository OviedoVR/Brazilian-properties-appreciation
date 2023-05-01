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
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlecolor'] = 'black'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.labelcolor'] = 'darkgray'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.2
plt.rcParams['ytick.color'] = 'darkgray'
plt.rcParams['xtick.color'] = 'darkgray'
plt.rcParams['figure.facecolor'] = '#464545'
plt.rcParams['axes.titlecolor'] = '#FFFFFF'
plt.rcParams['axes.titlecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.85
plt.rcParams['ytick.major.size'] = 0

# --- App:
imoveis_br  = pd.read_excel('ImoveisBR_2023.xlsx', sheet_name='ImoveisBR_2023')
dados_brutos  = pd.read_excel('ImoveisBR_2023.xlsx', sheet_name='dados_brutos')
imoveis_br['Cidade_estado'] = imoveis_br['Rotulo'] + ', ' + imoveis_br['Sigla']
imoveis_br['Var_anual_12m'] = round(imoveis_br['Var_anual_12m'], 2)*100
imoveis_br['BRL_metro_quad'] = imoveis_br['BRL_metro_quad']

# Cabeçalho:
st.markdown('### Valorização de imóveis residenciais no Brasil')
cidades = sorted(list(imoveis_br['Cidade_estado'].unique()))

# Widgets:
selecao = st.selectbox(
    '🌎 Selecione uma cidade',
    cidades
)

# seleção da cidade
your_city = selecao
selected_city = imoveis_br.query('Cidade_estado == @your_city')
other_cities = imoveis_br.query('Cidade_estado != @your_city')

# Valorização anual (12 meses):
fig1, ax = plt.subplots(figsize=(3, 4.125))
#
sns.stripplot(
    data= other_cities,
    y = 'Var_anual_12m',
    color = 'white',
    jitter=0.32,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
#
sns.stripplot(
    data= selected_city,
    y = 'Var_anual_12m',
    color = '#00FF7F',
    jitter=0.15,
    size=12,
    linewidth=1,
    edgecolor='k',
    label=f'{your_city}'
)

# Mostrando a o valor central:
avg_var_anual_12m = imoveis_br['Var_anual_12m'].median()
q1_var_anual_12m = np.percentile(imoveis_br['Var_anual_12m'], 25)
q3_var_anual_12m = np.percentile(imoveis_br['Var_anual_12m'], 75)

# plot:
ax.axhline(y=avg_var_anual_12m, color='#DA70D6', linestyle='--', lw=0.75)
ax.axhline(y=q1_var_anual_12m, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_var_anual_12m, color='white', linestyle='--', lw=0.75)

# adicionando rótulos Q1, mediana e Q3:
ax.text(1.15, q1_var_anual_12m, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.3, avg_var_anual_12m, 'Mediana', ha='center', va='center', color='#DA70D6', fontsize=8, fontweight='bold')
ax.text(1.15, q3_var_anual_12m, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# fill the area between the lines
ax.fill_betweenx([q1_var_anual_12m, q3_var_anual_12m], -2, 1, alpha=0.2, color='gray')
# set the x-axis limits to show the full range of the data
ax.set_xlim(-1, 1)

# Eixos e títulos:
plt.xticks([])
plt.ylabel('Valorização média %')
plt.title('Valorização (%) nos últimos 12 meses', weight='bold', loc='center', pad=15, color='gainsboro')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.tight_layout()


# Preço (R$) por m²:
fig2, ax = plt.subplots(figsize=(2.95, 3.6))
#
sns.stripplot(
    data= other_cities,
    y = 'BRL_metro_quad',
    color = 'white',
    jitter=0.35,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
#
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

# Mostrando a o valor central:
avg_preco_m2 = imoveis_br['BRL_metro_quad'].median()
q1_preco_m2 = np.percentile(imoveis_br['BRL_metro_quad'], 25)
q3_preco_m2 = np.percentile(imoveis_br['BRL_metro_quad'], 75)

# plot:
ax.axhline(y=avg_preco_m2, color='#DA70D6', linestyle='--', lw=0.75)
ax.axhline(y=q1_preco_m2, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_preco_m2, color='white', linestyle='--', lw=0.75)


# adicionando rótulos Q1, mediana e Q3:
ax.text(1.15, q1_preco_m2, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.35, avg_preco_m2, 'Mediana', ha='center', va='center', color='#DA70D6', fontsize=8, fontweight='bold')
ax.text(1.15, q3_preco_m2, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# fill the area between the lines
ax.fill_betweenx([q1_preco_m2, q3_preco_m2], -2, 1, alpha=0.2, color='gray')
# set the x-axis limits to show the full range of the data
ax.set_xlim(-1, 1)


# Eixos e títulos:
plt.xticks([])
plt.ylabel('Preço (R\$)')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.title('Preço médio (R\$) por $m^2$', weight='bold', loc='center', pad=15, color='gainsboro')
plt.tight_layout()

# Separando os gráficos em 2 colunas:
left, right = st.columns(2)

# Colunas:
with left:
    st.pyplot(fig1)
with right:
    st.pyplot(fig2)

st.markdown('''
<span style="color:white;font-size:10pt"> ⚪ Cada ponto representa uma cidade </span>
<span style="color:#DA70D6;font-size:10pt"> ▫ <b> Valor médio </b></span>
<span style="color:white;font-size:10pt"> ◽ Valores menores (<b> fundo </b>)
◽ Valores maiores (<b> topo </b>) </span>
''',unsafe_allow_html=True)

st.dataframe(
    imoveis_br.query('Cidade_estado == @your_city')[[
      'Cidade_estado','Var_anual_12m', 
      'BRL_metro_quad']]
)

st.markdown(''' > **REFEÊNCIAS (Valorização 12 meses):**

* IPCA: **6% a.a.**
* IGP-M: **4% a.a.**
* Índice FipeZAP+: **6% a.a.**

> Dados baseados nos informes FipeZAP (leva em conta imóveis residenciais para 50 cidades brasilieras).
''')


st.markdown('---')
st.markdown(''' **Criado por Vinícius Oviedo** 

[![Linkedin Badge](https://img.shields.io/badge/-Linkedin-0A66C2?&logo=Linkedin&link=https://www.linkedin.com/in/vinicius-oviedo/)](https://www.linkedin.com/in/vinicius-oviedo/)
[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?&logo=Medium&link=https://github.com/OviedoVR)](https://github.com/OviedoVR)
[![Medium Badge](https://img.shields.io/badge/-Medium-green?&logo=Medium&link=https://medium.com/@vo.freelancer5)](https://medium.com/@vo.freelancer5/)
[![Website Badge](https://img.shields.io/badge/-Website-whitesmoke?&link=https://oviedovr.github.io/OviedoVR-ViniciusOviedo.github.io/)](https://oviedovr.github.io/OviedoVR-ViniciusOviedo.github.io/)
''')
st.markdown('---')
# --- (Fim do App)