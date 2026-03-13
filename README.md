# Projeto Integrador — Desenvolvimento Low Code em Ciência de Dados
## Flor de Aço: Análise de Feminicídio no Brasil

---

## Integrantes do Grupo

| Nome | GitHub |
|------|--------|
| Rafael | [@rafaelsrhub](https://github.com/rafaelsrhub) |
| vitoriano | [@vitorianorvp](https://github.com/vitorianorvp) |
| Lucas Garcia | [@Lukym19](https://github.com/Lukym19) |
| Victor Soares | [@vs0arez](https://github.com/vs0arez) |
| João Marcos | [@joao-ntz](https://github.com/joao-ntz) |
| Allessander da silva oliveira junior | [@GAMEOFGODSJ](https://github.com/GAMEOFGODSJ) |
---

## Tema do Projeto

Análise da violência letal contra mulheres no Brasil com base em dados públicos do sistema oficial de mortalidade (DATASUS/SIM), com foco na identificação de padrões temporais, territoriais e de perfil das vítimas.

---

## Objetivo da Análise

Este projeto tem como objetivo investigar a evolução dos casos de feminicídio no Brasil entre 2006 e os anos mais recentes, buscando responder às seguintes perguntas:

1. Como os casos de feminicídio evoluíram ao longo dos anos no Brasil?
2. Quais estados/regiões concentram o maior número de casos?
3. Qual o perfil predominante das vítimas (faixa etária, raça/cor, estado civil)?
4. Quais são os locais de ocorrência mais frequentes (domicílio, via pública, hospital)?
5. Existe correlação entre períodos e variações no número de casos?

---

## Base de Dados

**Nome:** Flor de Aço: Dados contra o Feminicídio  
**Fonte:** Kaggle  
**Link:** https://www.kaggle.com/datasets/rafatrindade/feminicidio-br  
**Licença:** CC0 - Domínio Público  
**Origem dos dados:** SIM (Sistema de Informações sobre Mortalidade) — DATASUS/Ministério da Saúde  
**Cobertura temporal:** 2006 até dados preliminares mais recentes  
**Atualização:** Semanal (automática)

### Arquivos utilizados no projeto:

| Arquivo | Descrição |
|---------|-----------|
| `feminicidio_serie_historica.parquet` | Base consolidada e validada de óbitos femininos por causas externas — principal arquivo de análise |
| `feminicidio_prelim.parquet` | Base preliminar com registros mais recentes, sujeitos a revisão |
| `geo_macroregiao.parquet` | Base auxiliar com municípios, regiões e macrorregiões de saúde para cruzamento geográfico |

### Principais colunas disponíveis:

- `DT_NASCIMENTO` — Data de nascimento da vítima
- `DT_OBITO` — Data do óbito
- `RACA_COR` — Raça/cor da vítima
- `EST_CIVIL` — Estado civil
- `COD_MUNICIPIO_RESID` — Município de residência
- `COD_MUNICIPIO_OBITO` — Município de ocorrência do óbito
- `LOCAL_OCORRENCIA_OBITO` — Local do óbito (domicílio, via pública, hospital, etc.)

---

## Planejamento do Processo ETL

### Extract (Extração)
- Carregamento dos arquivos `.parquet` da base `feminicidio_serie_historica` e `geo_macroregiao` utilizando a biblioteca `pandas`
- Leitura da base preliminar `feminicidio_prelim.parquet` para dados recentes

### Transform (Transformação)
Transformações planejadas:
- Conversão de colunas de data (`DT_NASCIMENTO`, `DT_OBITO`) para o tipo `datetime`
- Cálculo da **faixa etária** das vítimas no momento do óbito
- Extração do **ano** e **mês** do óbito para análise de série temporal
- Tratamento de valores **nulos e "IGNORADO"** (preenchimento ou exclusão conforme impacto)
- Padronização de campos categóricos (`RACA_COR`, `EST_CIVIL`, `LOCAL_OCORRENCIA_OBITO`)
- Join com a base geográfica (`geo_macroregiao`) pelo código do município para obter estado (UF) e região
- Agregações por ano, UF, faixa etária e raça/cor

### Load (Carga)
- Armazenamento da base tratada em arquivo CSV: `data/base_tratada.csv`
- Possibilidade de carga em banco SQLite para consultas estruturadas

---

## Ideia Inicial do Dashboard (Streamlit)

O dashboard interativo será desenvolvido com **Streamlit** e apresentará:

| Visualização | Tipo | Descrição |
|---|---|---|
| Evolução anual de casos | Gráfico de linha | Total de casos por ano (2006–atual) |
| Mapa por estado | Mapa coroplético | Intensidade de casos por UF |
| Distribuição por raça/cor | Gráfico de barras/pizza | Perfil racial das vítimas |
| Distribuição por faixa etária | Histograma | Faixa etária mais afetada |
| Local de ocorrência | Gráfico de barras | Domicílio x Via Pública x Hospital |
| Estado civil das vítimas | Gráfico de barras | Solteiras, Casadas, etc. |
| Filtros interativos | Sidebar | Por ano, estado (UF) e raça/cor |

---

## Estrutura de Pastas do Repositório

```
projeto-integrador-grupo/
│
├── data/
│   ├── base_original/          # Arquivos originais do Kaggle (.parquet, .csv)
│   └── base_tratada.csv        # Base após processo ETL com Pandas
│
├── src/
│   └── etl.py                  # Script do processo Extract, Transform, Load
│
├── app/
│   └── dashboard.py            # Aplicação Streamlit com dashboard interativo
│
└── README.md                   # Documentação completa do projeto
```

---

## Cronograma de Desenvolvimento

| Etapa | Atividade | Responsável | Prazo |
|-------|-----------|-------------|-------|
| 1 | Criação do repositório e README | Rafael | 23/03/2026 |
| 1 | Estrutura de pastas e colaboradores | Grupo | 23/03/2026 |
| 2 | Download e exploração inicial dos dados | A definir | Abril/2026 |
| 2 | Desenvolvimento do script ETL (`etl.py`) | A definir | Abril/2026 |
| 2 | Tratamento e limpeza dos dados com Pandas | A definir | Abril/2026 |
| 2 | Desenvolvimento do dashboard Streamlit | A definir | Abril/2026 |
| 2 | Testes, ajustes e entrega final | Grupo | A confirmar |

---

## Tecnologias Utilizadas

- **Python 3.x**
- **Pandas** — Manipulação e transformação dos dados
- **Streamlit** — Dashboard interativo
- **GitHub** — Versionamento e colaboração

---

## Divisão de Tarefas

| Tarefa | Responsável |
|--------|-------------|
| Configuração do repositório GitHub | Rafael |
| Documentação do README | Rafael |
| Script ETL | A definir |
| Dashboard Streamlit | A definir |
| Testes e validação | A definir |

> **Nota:** Este planejamento é inicial e pode ser ajustado na Etapa 2 conforme o desenvolvimento e aprendizado da equipe.

---

## Referências

- [Dataset no Kaggle — Flor de Aço](https://www.kaggle.com/datasets/rafatrindade/feminicidio-br)
- [DATASUS — Sistema de Informações sobre Mortalidade](https://datasus.saude.gov.br/)
- [Documentação Pandas](https://pandas.pydata.org/docs/)
- [Documentação Streamlit](https://docs.streamlit.io/)
- [Documentação GitHub](https://docs.github.com/pt)

---

*Projeto desenvolvido para a disciplina PI - Desenvolvimento Low Code em Ciência de Dados*  
*Curso: Tecnólogo em Análise e Desenvolvimento de Sistemas — SENAC EAD*  
*Professora: Fernanda Caetano | Período: Fevereiro a Março de 2026*
