# ============================================================
# dashboard.py - Dashboard Interativo com Streamlit
# Projeto Integrador - Flor de Aco: Analise de Feminicidio no Brasil
# SENAC EAD - Curso: Tecnologo em ADS
# ============================================================
# Este arquivo sera implementado na Etapa 2 do projeto.
# Visualizacoes planejadas:
#
#   - Grafico de linha: Evolucao anual de casos (2006-atual)
#   - Mapa coropletico: Intensidade de casos por UF
#   - Grafico de barras/pizza: Distribuicao por raca/cor
#   - Histograma: Distribuicao por faixa etaria
#   - Grafico de barras: Local de ocorrencia (domicilio, via publica, hospital)
#   - Grafico de barras: Estado civil das vitimas
#   - Sidebar com filtros interativos: ano, UF e raca/cor
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise Feminicídio", layout="wide")

df = pd.read_csv("base_tratada.csv")
# Implementar tudo na Etapa 2
st.title('Flor de Aco: Analise de Feminicidio no Brasil')

with st.sidebar:
    st.title("Análise Feminicídio no Brasil - SENAC EAD")

    st.write("Este dashboard interativo apresenta uma análise da violência letal contra mulheres no Brasil com base em dados públicos do DATASUS/SIM.")

    st.write("A plataforma reúne visualizações dinâmicas sobre a evolução anual dos casos, distribuição geográfica por estado, perfil das vítimas e locais de ocorrência, além de filtros interativos que permitem uma exploração mais detalhada dos dados por período, unidade federativa e raça/cor.")

#AQUI EU FIZ O GRAFICO DE LINHA NO CASOS DO ANO (LUCAS G)
casos_ano = (df.groupby("ANO_OBITO").size().reset_index(name="CASOS"))
casos_ano["ANO_OBITO"] = casos_ano["ANO_OBITO"].astype(str)

fig_linha = px.line(casos_ano, x="ANO_OBITO", y="CASOS", title="Evolução Anual dos Casos de Feminicídio", markers=True, color_discrete_sequence=["#FF2600"])

#AQUI EU FIZ O MAPA COROPLÉTICO POR ESTADO (LUCAS G)
casos_estado = (df.groupby("UF").size().reset_index(name="CASOS POR ESTADO"))
url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"


fig_mapa = px.choropleth(casos_estado, geojson=url_geojson, locations="UF", featureidkey="properties.sigla", color="CASOS POR ESTADO", color_continuous_scale="Reds", title="Distribuição Geográfica dos Casos de Feminicídio por Estado")

fig_mapa.update_geos(fitbounds="locations", visible=False)

#AQUI EU FIZ O GRAFICO DE BARRAS NO POR RAÇA/COR (LUCAS G)
casos_raca = (df[df["RACA_COR"] != "Ignorado"].groupby("RACA_COR").size().reset_index(name="CASOS POR RAÇA/COR"))

fig_pizza = px.pie(casos_raca, names="RACA_COR", values="CASOS POR RAÇA/COR", title="Distribuição de Casos de Feminicídio por Raça/Cor", color_discrete_sequence=["#FF2F00", "#1F77B4", "#2CA02C", "#FFD700", "#8A2BE2"])
 
col1, col2 = st.columns([1,1], gap="large")
with col1:
    st.subheader("Evolução Anual dos Casos de Feminicídio")
    st.plotly_chart(fig_linha)
    
with col2:
    st.subheader("Distribuição de Casos de Feminicídio por Raça/Cor")
    st.plotly_chart(fig_pizza)

col3, col4 = st.columns([1, 1], gap="large")
with col3:
    st.subheader("Mapa Coroplético dos Casos de Feminicídio por Estado")
    st.plotly_chart(fig_mapa)
