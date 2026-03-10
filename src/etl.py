# ============================================================
# etl.py - Script de ETL (Extract, Transform, Load)
# Projeto Integrador - Flor de Aco: Analise de Feminicidio no Brasil
# SENAC EAD - Curso: Tecnologo em ADS
# ============================================================
# Este arquivo sera implementado na Etapa 2 do projeto.
#
# EXTRACT: Carregar feminicidio_serie_historica.parquet e geo_macroregiao.parquet
# TRANSFORM: Limpeza, calculo de faixa etaria, join geografico, agregacoes
# LOAD: Salvar base tratada em ../data/base_tratada.csv
# ============================================================

import pandas as pd

# TODO: Implementar na Etapa 2
def extract():
    pass

def transform(df):
    pass

def load(df):
    pass

if __name__ == '__main__':
    df_raw = extract()
    df_tratado = transform(df_raw)
    load(df_tratado)
