import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Flor de Aço - Dashboard",
    page_icon="🌸",
    layout="wide"
)

# 2. FUNÇÃO PARA GERAR DADOS FICTÍCIOS (MOCK DATA)
# Quando o ETL estiver pronto, você vai apagar essa função e usar o pd.read_csv()
@st.cache_data # Isso faz o Streamlit não gerar novos dados a cada clique
def carregar_dados_mock():
    np.random.seed(42)
    tamanho_amostra = 500
    
    dados = {
        'ANO': np.random.choice([2021, 2022, 2023, 2024], tamanho_amostra),
        'UF': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'PI', 'RS'], tamanho_amostra),
        'RACA_COR': np.random.choice(['Branca', 'Preta', 'Parda', 'Indígena', 'Amarela'], tamanho_amostra),
        'LOCAL_OCORRENCIA': np.random.choice(['Domicílio', 'Via Pública', 'Hospital', 'Outros'], tamanho_amostra)
    }
    return pd.DataFrame(dados)

# Carregando os dados (Fictícios por enquanto)
df = carregar_dados_mock()

# 3. CABEÇALHO DO DASHBOARD
st.title("🌸 Flor de Aço: Análise de Feminicídio no Brasil")
st.markdown("Dashboard interativo desenvolvido para o Projeto Integrador - Dados Fictícios para teste de layout.")
st.divider()

# 4. BARRA LATERAL (FILTROS)
st.sidebar.header("Filtros de Análise")

# Filtro de Ano
anos_disponiveis = sorted(df['ANO'].unique())
ano_selecionado = st.sidebar.multiselect("Selecione o Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Estado
ufs_disponiveis = sorted(df['UF'].unique())
uf_selecionada = st.sidebar.multiselect("Selecione o Estado (UF)", ufs_disponiveis, default=ufs_disponiveis)

# Aplicando os filtros no DataFrame
df_filtrado = df[
    (df['ANO'].isin(ano_selecionado)) & 
    (df['UF'].isin(uf_selecionada))
]

# 5. VISUALIZAÇÕES (GRÁFICOS)
# Criando duas colunas para organizar o layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Evolução de Casos por Ano")
    # Agrupando dados por ano
    casos_por_ano = df_filtrado['ANO'].value_counts().sort_index()
    st.line_chart(casos_por_ano)

with col2:
    st.subheader("🗺️ Casos por Estado")
    # Agrupando dados por UF
    casos_por_uf = df_filtrado['UF'].value_counts()
    st.bar_chart(casos_por_uf)

st.divider()

# Mais duas colunas para outros gráficos
col3, col4 = st.columns(2)

with col3:
    st.subheader("👤 Distribuição por Raça/Cor")
    casos_por_raca = df_filtrado['RACA_COR'].value_counts()
    st.bar_chart(casos_por_raca)

with col4:
    st.subheader("📍 Local de Ocorrência")
    casos_por_local = df_filtrado['LOCAL_OCORRENCIA'].value_counts()
    st.bar_chart(casos_por_local)

# 6. MOSTRAR DADOS BRUTOS (Opcional, bom para testes)
if st.checkbox("Mostrar tabela de dados (Mock)"):
    st.dataframe(df_filtrado)
