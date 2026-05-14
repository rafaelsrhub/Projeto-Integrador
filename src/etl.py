# ============================================================
# etl.py — Projeto Integrador: Flor de Aço
# Análise de Feminicídio no Brasil — SENAC EAD
# ============================================================

import pandas as pd

# ============================================================
# EXTRACT — carregar os arquivos
# ============================================================
print("Carregando arquivos...")

df  = pd.read_csv("data/base original/feminicidio_serie_historica.csv", low_memory=False)
geo = pd.read_csv("data/base original/geo_macroregiao.csv")
pns = pd.read_csv("data/base original/pns_violencia_fem_2019.csv")

print(f"Série histórica: {len(df)} registros carregados.")

# ============================================================
# TRANSFORM — normalização dos dados
# ============================================================
print("\nIniciando normalização...")

# 1. Converter datas para o formato correto
df["DT_OBITO"]      = pd.to_datetime(df["DT_OBITO"].astype(str).str.zfill(8), format="%d%m%Y", errors="coerce")
df["DT_NASCIMENTO"] = pd.to_datetime(df["DT_NASCIMENTO"].astype(str).str.replace(".0","").str.zfill(8), format="%d%m%Y", errors="coerce")

# 2. Extrair o ANO do óbito (gráficos 1 e 3)
df["ANO_OBITO"] = df["DT_OBITO"].dt.year

# 3. Calcular idade no momento do óbito
df["IDADE_OBITO"] = (df["DT_OBITO"] - df["DT_NASCIMENTO"]).dt.days // 365

# 4. Criar faixa etária de 10 em 10 anos (gráfico 4)
def classificar_faixa(idade):
    if pd.isna(idade) or idade < 0: return "Ignorado"
    elif idade < 10:  return "0–9"
    elif idade < 20:  return "10–19"
    elif idade < 30:  return "20–29"
    elif idade < 40:  return "30–39"
    elif idade < 50:  return "40–49"
    elif idade < 60:  return "50–59"
    else:             return "60+"

df["FAIXA_ETARIA"] = df["IDADE_OBITO"].apply(classificar_faixa)

# 5. Padronizar ESTADO CIVIL (gráfico 6)
mapa_estado_civil = {
    "SOLTEIRA":       "Solteira",
    "CASADA":         "Casada",
    "VIUVA":          "Viúva",
    "DIVORCIADA":     "Divorciada",
    "UNIÃO ESTAVEL":  "União estável"
}
df["EST_CIVIL"] = df["EST_CIVIL"].astype(str).str.strip().map(mapa_estado_civil).fillna("Ignorado")

# 6. Padronizar LOCAL DE OCORRÊNCIA (gráfico 5)
mapa_local = {
    "DOMICILIO":                         "Domicílio",
    "VIA PUBLICA":                       "Via pública",
    "HOSPITAL":                          "Hospital",
    "OUTROS":                            "Outros",
    "OUTROS ESTABELECIMENTOS DE SAUDE":  "Outro estab. de saúde",
    "ALDEIA INDIGENA":                   "Aldeia indígena"
}
df["LOCAL_OCORRENCIA_OBITO"] = df["LOCAL_OCORRENCIA_OBITO"].astype(str).str.strip().map(mapa_local).fillna("Ignorado")

# 7. Padronizar RAÇA/COR
mapa_raca = {
    "BRANCA":   "Branca",
    "PRETA":    "Preta",
    "AMARELA":  "Amarela",
    "PARDA":    "Parda",
    "INDIGENA": "Indígena"
}
df["RACA_COR"] = df["RACA_COR"].astype(str).str.strip().map(mapa_raca).fillna("Ignorado")

# 8. Cruzar com geo para trazer UF e Região (gráfico 2)
# Corrigindo formatos: df tem 7 dígitos, geo tem 6 dígitos
# Pegamos os 6 primeiros dígitos do código do município do df
df["COD_MUN_6"] = df["COD_MUNICIPIO_OBITO"].astype(str).str[:6]
geo["MUNCOD_6"] = geo["MUNCOD"].astype(str).str.replace(".0","").str.strip().str[:6]

df = df.merge(
    geo[["MUNCOD_6", "sg_uf", "regiao_pais"]],
    left_on="COD_MUN_6",
    right_on="MUNCOD_6",
    how="left"
)

df.rename(columns={"sg_uf": "UF", "regiao_pais": "REGIAO"}, inplace=True)

# 9. Remover linhas sem ano de óbito
df = df.dropna(subset=["ANO_OBITO"])
df["ANO_OBITO"] = df["ANO_OBITO"].astype(int)

print(f"Registros após limpeza: {len(df)}")
print("\nAmostra do resultado:")
print(df[["DT_OBITO", "ANO_OBITO", "FAIXA_ETARIA", "EST_CIVIL",
          "LOCAL_OCORRENCIA_OBITO", "RACA_COR", "UF", "REGIAO"]].head(5))

# Verificar se UF foi preenchida
print(f"\nUF preenchida em {df['UF'].notna().sum()} de {len(df)} registros")

# ============================================================
# LOAD — salvar base tratada
# ============================================================
df.to_csv("data/base_tratada.csv", index=False, encoding="utf-8-sig")
print("\nBase tratada salva em: data/base_tratada.csv")
