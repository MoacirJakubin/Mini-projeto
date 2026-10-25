# Instruções de execução – Miniprojeto Varejo

**Aluno:** Moacir Jakubin | **Turma:** Analise_de_Dados_T1

## No VS Code

1. Baixe a base no Kaggle (https://www.kaggle.com/datasets/namespaiva/base-varejo/data) e salve como `Varejo.csv.csv` na mesma pasta do script (no repositório, o arquivo já está incluído).
2. No terminal, instale as dependências: `pip install -r requirements.txt`
3. Rode: `python Miniprojeto_Varejo.py`

## No Google Colab

1. Faça upload de `Miniprojeto_Varejo.py` e `Varejo.csv.csv` (painel de arquivos à esquerda).
2. Em uma célula, execute:

```python
!pip install pandas numpy
!python Miniprojeto_Varejo.py Varejo.csv.csv
```

## Saídas

O relatório aparece no terminal e é gerado o arquivo `df_limpo.csv`.