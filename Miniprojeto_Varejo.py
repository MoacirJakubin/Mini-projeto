"""
Mini-Projeto Avaliativo - Modulo 1 - Analise de Dados com Python
Analise Exploratoria (AED) da base Varejo
Aluno: SEU NOME COMPLETO | Turma: Analise_de_Dados_T1

Como executar:  python Miniprojeto_Varejo.py
(o arquivo da base deve estar na mesma pasta do script)

Colunas da base:
  DATA       data da compra          CO_ID   numero (identificador) da compra
  CL_ID      identificador do cliente CL_GENERO genero do cliente
  CL_EC      estado civil            CL_FHL  numero de filhos do cliente
  CL_SEG     segmento do cliente     PR_ID   identificador do produto
  PR_CAT     categoria do produto    PR_NOME nome do produto
Obs.: a base nao tem coluna de valor (R$). "Vendas" = itens e compras.
"""

import csv
import os
import re
from datetime import datetime

import pandas as pd

# ------------------------------------------------------------------
# CONFIGURACAO
# ------------------------------------------------------------------
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA, "Varejo.csv.csv")   # nome real do arquivo
DELIMITADOR = ";"
ENCODING = "utf-8"

COL_DATA = "DATA"
COL_ID_COMPRA = "CO_ID"
COL_CLIENTE = "CL_ID"
COL_GENERO = "CL_GENERO"
COL_ESTADO_CIVIL = "CL_EC"
COL_FILHOS = "CL_FHL"
COL_SEGMENTO = "CL_SEG"
COL_ID_PRODUTO = "PR_ID"
COL_CATEGORIA = "PR_CAT"
COL_PRODUTO = "PR_NOME"
COLS_FISICAS = []   # a base nao possui dimensoes fisicas (peso, altura...)

# Linhas 100% iguais podem ser o mesmo produto comprado 2x na mesma compra
# (a base nao tem coluna de quantidade). Mantenha True para seguir o
# enunciado (eliminar duplicatas) e discuta esse risco no README.
REMOVER_DUPLICATAS = True


def titulo(texto):
    """Imprime um cabecalho de secao no terminal."""
    print("\n" + "=" * 64)
    print(texto)
    print("=" * 64)


# ==================================================================
# SPRINT 1 - IMPORTACAO DOS DADOS (csv.DictReader + pandas)
# ==================================================================
def carregar_csv(caminho, delimitador, encoding):
    """Le o CSV com csv.DictReader e devolve (lista de dicts, colunas)."""
    try:
        with open(caminho, newline="", encoding=encoding) as arq:
            leitor = csv.DictReader(arq, delimiter=delimitador)
            linhas = list(leitor)
            colunas = leitor.fieldnames
    except UnicodeDecodeError:
        # Se o arquivo nao for UTF-8, tenta o padrao do Windows (latin-1)
        with open(caminho, newline="", encoding="latin-1") as arq:
            leitor = csv.DictReader(arq, delimiter=delimitador)
            linhas = list(leitor)
            colunas = leitor.fieldnames
    return linhas, colunas


titulo("SPRINT 1 - IMPORTACAO")
linhas, colunas = carregar_csv(ARQUIVO, DELIMITADOR, ENCODING)
df = pd.DataFrame(linhas)  # tudo entra como texto (string)
del linhas                 # libera memoria (a base tem centenas de milhares de linhas)

# Colunas sem nome sao sobra dos ";;;" no fim de cada linha e nao tem dados
sem_nome = [c for c in df.columns if not isinstance(c, str) or c.strip() == ""]
df = df.loc[:, [isinstance(c, str) and c.strip() != "" for c in df.columns]]
print("Colunas sem nome removidas:", len(sem_nome))

print("Numero de registros:", len(df))
print("Numero de colunas:", len(df.columns))
print("Colunas:", list(df.columns))
print("\nTipos de dados (antes da limpeza):")
print(df.dtypes)


# ==================================================================
# SPRINT 2 - TRANSFORMACAO DE STRING, INTEGER, FLOAT E DATETIME
# ==================================================================
# Textos que significam "sem informacao" (ex.: erro #N/D do Excel gravado no CSV)
VALORES_NULOS = {"#N/D", "#N/A", "N/D", "N/A", "NULL", "NAN", "NONE", "-", "?"}


def limpar_texto(valor):
    """Tira espacos extras e transforma texto vazio ou '#N/D' em None."""
    if valor is None:
        return None
    texto = re.sub(r"\s+", " ", str(valor)).strip()
    if texto == "" or texto.upper() in VALORES_NULOS:
        return None
    return texto


def para_inteiro(valor):
    """Converte texto em int usando regex; devolve None se nao der."""
    texto = limpar_texto(valor)
    if texto is None:
        return None
    texto = re.sub(r"[^\d\-]", "", texto)
    if texto in ("", "-"):
        return None
    return int(texto)


def para_float(valor):
    """Converte texto em float (aceita 1.234,56 e 1234.56)."""
    texto = limpar_texto(valor)
    if texto is None:
        return None
    texto = re.sub(r"[^\d,.\-]", "", texto)
    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def para_data(valor, formatos=("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y")):
    """Converte texto em datetime tentando varios formatos."""
    texto = limpar_texto(valor)
    if texto is None:
        return None
    for formato in formatos:
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            continue
    return None


def aplicar(serie, funcao):
    """Aplica a funcao apenas nos valores UNICOS da coluna e devolve a
    coluna convertida. Em 800 mil linhas isso e muito mais rapido."""
    mapa = {v: funcao(v) for v in serie.dropna().unique()}
    return serie.map(mapa)


titulo("SPRINT 2 - TRANSFORMACAO DE TIPOS")
# 2.1 Limpeza de texto em todas as colunas
df.columns = [str(c).strip() for c in df.columns]
for col in df.columns:
    df[col] = aplicar(df[col], limpar_texto)

# 2.2 Colunas totalmente vazias (sem nenhum dado) tambem sao removidas
colunas_vazias = [c for c in df.columns if df[c].isna().all()]
df = df.drop(columns=colunas_vazias)
print("Colunas vazias removidas:", colunas_vazias)

# 2.3 Diagnostico ANTES do tratamento (problemas encontrados)
nulos_antes = df.isna().sum()
duplicatas_antes = int(df.duplicated().sum())
print("\nValores nulos por coluna (antes):")
print(nulos_antes)
print("Linhas duplicadas (antes):", duplicatas_antes)

# 2.4 Ajuste de tipos
df[COL_DATA] = pd.to_datetime(aplicar(df[COL_DATA], para_data), errors="coerce")
df[COL_FILHOS] = pd.to_numeric(
    aplicar(df[COL_FILHOS], para_inteiro), errors="coerce"
).astype("Int64")
for col in (COL_ID_COMPRA, COL_CLIENTE, COL_ID_PRODUTO):
    df[col] = pd.to_numeric(aplicar(df[col], para_inteiro), errors="coerce").astype("Int64")
for col in COLS_FISICAS:
    df[col] = pd.to_numeric(aplicar(df[col], para_float), errors="coerce")

datas_invalidas = int(df[COL_DATA].isna().sum())
print("Datas ausentes ou invalidas:", datas_invalidas)
print("Periodo da base:", df[COL_DATA].min(), "ate", df[COL_DATA].max())
print("\nTipos de dados (depois):")
print(df.dtypes)


# ==================================================================
# SPRINT 3 - LIMPEZA DE NULOS E DUPLICATAS
# ==================================================================
def preencher_categoria(valor):
    """Se a categoria estiver vazia, usa 'Sem Categoria'."""
    if pd.isna(valor):
        return "Sem Categoria"
    else:
        return valor


titulo("SPRINT 3 - NULOS E DUPLICATAS")
total_inicial = len(df)

# 3.1 Categoria vazia (ou #N/D) -> "Sem Categoria" (nao perde o registro)
categorias_vazias = int(df[COL_CATEGORIA].isna().sum())
df[COL_CATEGORIA] = df[COL_CATEGORIA].apply(preencher_categoria)
print("Categorias vazias preenchidas com 'Sem Categoria':", categorias_vazias)

# 3.2 Genero, estado civil e segmento vazios -> "Nao informado"
for col in (COL_GENERO, COL_ESTADO_CIVIL, COL_SEGMENTO, COL_PRODUTO):
    df[col] = df[col].fillna("Nao informado")

# 3.3 Data, compra ou cliente ausentes -> remover (sem eles o registro
#     nao entra nas analises por periodo, por compra nem por cliente)
df = df.dropna(subset=[COL_DATA, COL_ID_COMPRA, COL_CLIENTE])
removidas_nulos = total_inicial - len(df)

# 3.4 Numero de filhos ausente ou negativo -> mediana (robusta a outliers)
filhos_negativos = int((df[COL_FILHOS] < 0).sum())
df.loc[df[COL_FILHOS] < 0, COL_FILHOS] = pd.NA
if df[COL_FILHOS].notna().any():
    mediana_filhos = int(round(float(df[COL_FILHOS].median())))
    nulos_filhos = int(df[COL_FILHOS].isna().sum())
    df[COL_FILHOS] = df[COL_FILHOS].fillna(mediana_filhos)
    print("Filhos: nulos/negativos preenchidos com a mediana",
          mediana_filhos, "->", nulos_filhos, "registros")

# 3.5 Dimensoes fisicas ausentes -> mediana da propria coluna (se existirem)
for col in COLS_FISICAS:
    df[col] = df[col].fillna(df[col].median())

# 3.6 Duplicatas: so remove linhas 100% identicas. O mesmo CO_ID repete
#     (uma compra tem varios itens), por isso nunca se remove duplicata
#     olhando apenas para o identificador.
removidas_dup = 0
if REMOVER_DUPLICATAS:
    antes_dup = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removidas_dup = antes_dup - len(df)

# 3.7 Regra do identificador de compra: um CO_ID representa UMA compra,
#     portanto deve ter um unico cliente e uma unica data.
por_compra = df.groupby(COL_ID_COMPRA)
n_compras = int(df[COL_ID_COMPRA].nunique())
ids_com_varios_clientes = int((por_compra[COL_CLIENTE].nunique() > 1).sum())
ids_com_varias_datas = int((por_compra[COL_DATA].nunique() > 1).sum())

print("Linhas removidas por nulo critico:", removidas_nulos)
print("Linhas removidas por duplicata:", removidas_dup)
print("Compras distintas (CO_ID):", n_compras)
print("CO_ID com mais de 1 cliente:", ids_com_varios_clientes)
print("CO_ID com mais de 1 data:", ids_com_varias_datas)


# ==================================================================
# SPRINT 4 - ESTATISTICA DESCRITIVA (NUMERO DE FILHOS)
# ==================================================================
def estatisticas(serie):
    """Devolve os parametros descritivos pedidos no enunciado."""
    s = serie.astype(int)
    return {
        "Contagem": int(s.count()),
        "Media": round(float(s.mean()), 2),
        "Mediana": float(s.median()),
        "Desvio padrao": round(float(s.std()), 2),
        "Moda": list(s.mode()),
        "Minimo": int(s.min()),
        "Maximo": int(s.max()),
        "Q1 (25%)": float(s.quantile(0.25)),
        "Q2 (50%)": float(s.quantile(0.50)),
        "Q3 (75%)": float(s.quantile(0.75)),
    }


titulo("SPRINT 4 - ESTATISTICAS: NUMERO DE FILHOS")
# Filhos e uma caracteristica do CLIENTE. Calcular por registro faria quem
# compra mais pesar mais; por isso calculamos por cliente unico (principal)
# e tambem por registro (comparacao).
clientes_unicos = df.drop_duplicates(subset=[COL_CLIENTE])
print("Por CLIENTE unico (", len(clientes_unicos), "clientes ):")
for nome, valor in estatisticas(clientes_unicos[COL_FILHOS]).items():
    print(f"  {nome:15s}: {valor}")
print("\nPor REGISTRO (todas as linhas):")
for nome, valor in estatisticas(df[COL_FILHOS]).items():
    print(f"  {nome:15s}: {valor}")


# ==================================================================
# AGRUPAMENTOS (groupby e pivot_table)
# ==================================================================
titulo("AGRUPAMENTOS")
# Agrupamento 1: genero (itens, compras distintas e clientes distintos)
por_genero = (
    df.groupby(COL_GENERO)
    .agg(itens=(COL_PRODUTO, "size"),
         compras=(COL_ID_COMPRA, "nunique"),
         clientes=(COL_CLIENTE, "nunique"))
    .sort_values("compras", ascending=False)
)
print("\n1) Compras por genero:")
print(por_genero)

# Agrupamento 2: categoria do produto
por_categoria = (
    df.groupby(COL_CATEGORIA)
    .agg(itens=(COL_PRODUTO, "size"), compras=(COL_ID_COMPRA, "nunique"))
    .sort_values("itens", ascending=False)
)
print("\n2) Itens e compras por categoria:")
print(por_categoria)

# Agrupamento 3: genero x categoria (pivot_table, contagem de itens)
cruzada = pd.pivot_table(
    df, values=COL_ID_COMPRA, index=COL_GENERO, columns=COL_CATEGORIA,
    aggfunc="count", fill_value=0,
)
print("\n3) Genero x categoria (itens):")
print(cruzada)

# Agrupamento 4: evolucao mensal (compras distintas por mes)
por_mes = df.groupby(df[COL_DATA].dt.to_period("M"))[COL_ID_COMPRA].nunique()
print("\n4) Compras por mes:")
print(por_mes)

# Agrupamento 5: segmento do cliente
por_segmento = (
    df.groupby(COL_SEGMENTO)
    .agg(itens=(COL_PRODUTO, "size"), clientes=(COL_CLIENTE, "nunique"))
    .sort_values("itens", ascending=False)
)
print("\n5) Itens por segmento de cliente:")
print(por_segmento)

# Agrupamento 6: produtos mais vendidos e clientes que mais compram
top_produtos = df.groupby(COL_PRODUTO).size().nlargest(10)
top_clientes = df.groupby(COL_CLIENTE)[COL_ID_COMPRA].nunique().nlargest(5)
print("\n6) Top 10 produtos (itens):")
print(top_produtos)
print("\n   Top 5 clientes (compras distintas):")
print(top_clientes)


# ==================================================================
# SPRINT 5 - RELATORIO FINAL NO TERMINAL
# ==================================================================
titulo("RELATORIO FINAL")
print("Registros iniciais ........:", total_inicial)
print("Registros finais ..........:", len(df))
print("Nulos encontrados (antes) .:", int(nulos_antes.sum()))
print("Duplicatas removidas ......:", removidas_dup)
print("Datas invalidas/ausentes ..:", datas_invalidas)
print("Compras distintas .........:", n_compras)
print("Clientes distintos ........:", len(clientes_unicos))
print("Genero com mais compras ...:", por_genero.index[0])
print("Categoria mais vendida ....:", por_categoria.index[0])
print("Mes com mais compras ......:", por_mes.idxmax())

# Salva a base tratada (sera enviada ao GitHub junto com o script)
df.to_csv(os.path.join(PASTA, "df_limpo.csv"), index=False,
          sep=";", encoding="utf-8")
print("\nArquivo df_limpo.csv gerado com sucesso.")
