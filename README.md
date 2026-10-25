# Mini-Projeto – Análise Exploratória da Base Varejo

Mini-projeto avaliativo do Módulo 1 (Semana 07) do curso **Análise de Dados com Python**.
O script lê a base **Varejo** (Kaggle), faz o diagnóstico de qualidade, limpa os dados, calcula estatísticas
descritivas do **número de filhos** dos clientes, explora agrupamentos e gera um relatório no terminal.

- Base: https://www.kaggle.com/datasets/namespaiva/base-varejo/data
- Linguagem: Python 3.9+ | Bibliotecas: `pandas`, `numpy` (e `csv`, `re`, `datetime` da biblioteca padrão)

## Estrutura do repositório

```
Miniprojeto_MoacirJakubin_Analise_de_Dados_T1/
├── Miniprojeto_Varejo.py              # script principal (Sprints 1 a 5)
├── Varejo.csv                         # base baixada do Kaggle (você adiciona)
├── df_limpo.csv                       # base tratada (gerada pelo script)
├── df_inconsistentes.csv              # registros separados por inconsistência (gerado)
├── relatorio_insights.md              # conclusões geradas pelo script
├── requirements.txt
├── README.md                          # este arquivo
├── README_NomeDoAluno_Turma.md        # instruções de execução
                 
```

## Como executar

```bash
pip install -r requirements.txt
python Miniprojeto_Varejo.py            # espera Varejo.csv na mesma pasta
python Miniprojeto_Varejo.py caminho/Varejo.csv
```

## O que o script faz (sprints)

| Sprint | Conteúdo |
|---|---|
| 1 | Leitura do CSV com `csv.DictReader` (detecta separador e encoding); mostra nº de registros, colunas e tipos |
| 2 | Limpeza de texto, inteiros e decimais com **regex**; conversão de datas com o módulo `datetime` |
| 3 | Nulos, duplicatas e inconsistências; regra do identificador de compra |
| 4 | Estatísticas de **número de filhos** + agrupamentos com `groupby()` e `pivot_table()` |
| 5 | Relatório final no terminal e geração de `relatorio_insights.md` |

## Decisões de limpeza (e justificativas)

- **Duplicatas:** linhas 100% idênticas são removidas, pois representam a mesma venda registrada duas vezes e inflariam os totais.
- **Categoria vazia:** recebe `"Sem Categoria"` (lógica `if/else`), preservando a venda sem inventar uma categoria.
- **Dimensões físicas nulas (peso, altura etc.):** imputadas com a **mediana**, mais robusta a outliers que a média.
- **Valor monetário ausente ou negativo:** o registro é **separado** em `df_inconsistentes.csv`, em vez de imputado, para não distorcer receita.
- **Identificador de compra:** um mesmo `id_compra` pode ter várias linhas (itens), mas deve ter um único cliente e uma única data. Quem viola a regra é separado.
- **Número de filhos fora de 0–20:** vira nulo e fica fora das estatísticas (não imputado, para não distorcer a distribuição).

## Insights da análise

> Preencha com os números reais depois de rodar o script na base completa
> (o arquivo `relatorio_insights.md` já traz uma versão gerada automaticamente).

1. **Qualidade dos dados:** _(ex.: X duplicatas removidas, Y registros inconsistentes separados)_
2. **Número de filhos:** _(média, mediana, moda e quartis encontrados)_
3. **Gênero com mais vendas:** _(qual e qual percentual do total)_
4. **Categoria líder:** _(qual e valor vendido)_
5. **Sazonalidade:** _(mês de pico e mês de menor movimento)_
6. **Problemas remanescentes:** _(nulos que sobraram, outliers, categorias com grafia parecida)_

## Reflexão teórica: ETL e qualidade de dados

**ETL** (*Extract, Transform, Load*) é o processo de extrair dados de uma fonte, transformá-los e carregá-los num
destino pronto para análise. Este projeto é um ETL em miniatura:

- **Extract:** leitura do `Varejo.csv` com `csv.DictReader` (Sprint 1).
- **Transform:** padronização de textos, conversão de tipos, tratamento de nulos, remoção de duplicatas e
  validação de regras de negócio (Sprints 2 e 3).
- **Load:** gravação de `df_limpo.csv` e dos relatórios, prontos para um dashboard ou análise posterior.

**Qualidade de dados** é o que torna os resultados confiáveis. As dimensões mais relevantes aqui foram:

- **Completude** (nulos), **unicidade** (duplicatas), **validade** (datas e valores plausíveis),
  **consistência** (o mesmo `id_compra` com cliente e data únicos) e **padronização** (grafias e formatos).

Dados sujos geram conclusões erradas (*garbage in, garbage out*): duplicatas inflam vendas, datas inválidas
quebram análises temporais e nulos viesam médias. Por isso, cada decisão de limpeza foi registrada e justificada,
e os registros problemáticos foram **separados em vez de apagados em silêncio**, o que deixa o processo auditável
e reproduzível.

## Autor

Moacir Jakubin – Turma Analise_de_Dados_T1
