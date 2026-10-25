# Instruções de execução – Miniprojeto Varejo

**Aluno:*Moacir Jakubin* Nome do Aluno | **Turma:*QA ADPY 2026/2 7* Analise_de_Dados_T1

## No VS Code

1. Baixe a base no Kaggle (https://www.kaggle.com/datasets/namespaiva/base-varejo/data) e salve como `Varejo.csv` na mesma pasta do script.
2. No terminal, instale as dependências: `pip install -r requirements.txt`
3. Rode: `python Miniprojeto_Varejo.py`

## No Google Colab

1. Faça upload de `Miniprojeto_Varejo.py` e `Varejo.csv` (painel de arquivos à esquerda).
2. Em uma célula, execute:

```python
!pip install pandas numpy
!python Miniprojeto_Varejo.py Varejo.csv
```

## Saídas

O relatório aparece no terminal e são gerados `df_limpo.csv`, `df_inconsistentes.csv` e `relatorio_insights.md`.

## Se o script avisar sobre colunas

O script detecta as colunas pelo nome (ex.: "Número de Filhos", "Categoria", "Data da Compra") e imprime o
**mapeamento detectado** no Sprint 2. Se alguma coluna aparecer como `None`, adicione o nome real dela na lista
correspondente do dicionário `APELIDOS`, no topo do script.
