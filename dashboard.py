
# dashboard.py - Dashboard Interativo com Streamlit
# Projeto Integrador - Flor de Aco: Analise de Feminicidio no Brasil
# SENAC EAD - Curso: Tecnologo em ADS
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


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise Feminicídio", layout="wide")


df = pd.read_csv("data/base_tratada.csv")
# Implementar tudo na Etapa 2
st.title('Flor de Aço: Análise de Feminicídio no Brasil')

# Filtros Interativos
with st.sidebar:
    st.title("Análise Feminicídio no Brasil - SENAC EAD")
    st.write("Este dashboard interativo apresenta uma análise da violência letal contra mulheres no Brasil com base em dados públicos do DATASUS/SIM.")
    st.write("A plataforma reúne visualizações dinâmicas sobre a evolução anual dos casos, distribuição geográfica por estado, perfil das vítimas e locais de ocorrência.")
    st.markdown("---")
    st.subheader("Filtros")
    
    # Filtro por ano
    anos_disponiveis = sorted(df["ANO_OBITO"].dropna().unique())
    ano_selecionado = st.multiselect(
        "Ano do Óbito",
        options=anos_disponiveis,
        default=anos_disponiveis
    )
    
    # Filtro por UF
    ufs_disponiveis = sorted(df["UF"].dropna().unique())
    uf_selecionada = st.multiselect(
        "Estado (UF)",
        options=ufs_disponiveis,
        default=ufs_disponiveis
    )
    
    # Filtro por raça/cor
    racas_disponiveis = df["RACA_COR"].dropna().unique().tolist()
    raca_selecionada = st.multiselect(
        "Raça/Cor",
        options=racas_disponiveis,
        default=racas_disponiveis
    )

# APLICAR FILTROS
df_filtrado = df[
    (df["ANO_OBITO"].isin(ano_selecionado)) &
    (df["UF"].isin(uf_selecionada)) &
    (df["RACA_COR"].isin(raca_selecionada))
].copy()

# Métrica resumo
st.metric("Total de Casos (com filtros aplicados)", f"{len(df_filtrado):,}".replace(",", "."))

#AQUI EU FIZ O GRAFICO DE LINHA NO CASOS DO ANO (LUCAS G)
casos_ano = df_filtrado.groupby("ANO_OBITO").size().reset_index(name="CASOS")
casos_ano["ANO_OBITO"] = casos_ano["ANO_OBITO"].astype(str)
fig_linha = px.line(casos_ano,x="ANO_OBITO",y="CASOS",title="Evolução Anual dos Casos de Feminicídio",markers=True,color_discrete_sequence=["#FF2600"]
)
#AQUI EU FIZ O MAPA COROPLÉTICO POR ESTADO (LUCAS G)
casos_estado = df_filtrado.groupby("UF").size().reset_index(name="CASOS POR ESTADO")
url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
fig_mapa = px.choropleth(casos_estado,geojson=url_geojson,locations="UF",featureidkey="properties.sigla",color="CASOS POR ESTADO",color_continuous_scale="Reds",title="Distribuição Geográfica dos Casos por Estado"
)
fig_mapa.update_geos(fitbounds="locations", visible=False)

#AQUI EU FIZ O GRAFICO DE PIZZA NO POR RAÇA/COR (LUCAS G)
casos_raca = df_filtrado[df_filtrado["RACA_COR"] != "Ignorado"].groupby("RACA_COR").size().reset_index(name="CASOS")
fig_pizza = px.pie(casos_raca,names="RACA_COR",values="CASOS",title="Distribuição por Raça/Cor",color_discrete_sequence=["#D36A52", "#1F77B4", "#2CA02C", "#FFD700", "#8A2BE2"]
)

# HISTOGRAMA - Distribuição por Faixa Etária (allessander junior)
if "FAIXA_ETARIA" in df_filtrado.columns:
    # Filtrar valores ignorados/nulos e agrupar pela faixa etária real
    casos_idade = df_filtrado[
        (df_filtrado["FAIXA_ETARIA"] != "Ignorado") & 
        (df_filtrado["FAIXA_ETARIA"].notna())
    ].groupby("FAIXA_ETARIA").size().reset_index(name="CASOS")

    ordem_faixas = ["0–9", "10–19", "20–29", "30–39", "40–49", "50–59", "60–69", "70–79", "80+"]  
    
    casos_idade["FAIXA_ETARIA"] = pd.Categorical(casos_idade["FAIXA_ETARIA"], categories=ordem_faixas, ordered=True)  
    casos_idade = casos_idade.sort_values("FAIXA_ETARIA")  
      
    # Gerar o gráfico de barras
    fig_idade = px.bar(  
        casos_idade,  
        x="FAIXA_ETARIA",  
        y="CASOS",  
        title="Distribuição por Faixa Etária",  
        color_discrete_sequence=["#E75284"]  
    )  
    fig_idade.update_layout(xaxis_title="Faixa Etária", yaxis_title="Número de Casos")
else:
    fig_idade = None

# GRÁFICO DE BARRAS - Local de Ocorrência (allessander junior)
if "LOCAL_OCORRENCIA_OBITO" in df_filtrado.columns:
    casos_local = df_filtrado[df_filtrado["LOCAL_OCORRENCIA_OBITO"] != "Ignorado"].groupby("LOCAL_OCORRENCIA_OBITO").size().reset_index(name="CASOS")
    casos_local = casos_local.sort_values("CASOS", ascending=True)
    
    fig_local = px.bar(
        casos_local,
        x="CASOS",
        y="LOCAL_OCORRENCIA_OBITO",
        orientation="h",
        title="Local de Ocorrência do Óbito",
        color_discrete_sequence=["#3498DB"]
    )
else:
    fig_local = None

# GRÁFICO DE BARRAS - Estado Civil (allessander junior)

if "EST_CIVIL" in df_filtrado.columns:
    casos_civil = df_filtrado[df_filtrado["EST_CIVIL"] != "Ignorado"].groupby("EST_CIVIL").size().reset_index(name="CASOS")
    casos_civil = casos_civil.sort_values("CASOS", ascending=False)
    
    fig_civil = px.bar(
        casos_civil,
        x="EST_CIVIL",
        y="CASOS",
        title="Distribuição por Estado Civil",
        color_discrete_sequence=["#FCA605"]
    )
else:
    fig_civil = None

# LAYOUT DO DASHBOARD 
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.subheader("Evolução Anual dos Casos de Feminicídio")
    st.plotly_chart(fig_linha, use_container_width=True)
with col2:
    st.subheader("Distribuição de Casos por Raça/Cor")
    st.plotly_chart(fig_pizza, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns([1, 1], gap="large")
with col3:
    st.subheader("Mapa Coroplético por Estado")
    st.plotly_chart(fig_mapa, use_container_width=True)
with col4:
        st.subheader("Distribuição por Faixa Etária")
        st.plotly_chart(fig_idade, use_container_width=True)

st.markdown("---")

col5, col6 = st.columns([1, 1], gap="large")
with col5:
        st.subheader("Local de Ocorrência do Óbito")
        st.plotly_chart(fig_local, use_container_width=True)
with col6:
        st.subheader("Distribuição por Estado Civil")
        st.plotly_chart(fig_civil, use_container_width=True)