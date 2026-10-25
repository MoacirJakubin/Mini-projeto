# Guia de versionamento (Sprint 6)

O histórico de commits precisa mostrar o progresso, então **faça um commit por sprint**.
Nome do repositório (público): `Miniprojeto_NomeAluno_Analise_de_Dados_T1` (troque `NomeAluno` pelo seu nome).

```bash
git init
git branch -M main

# Sprint 1
git add Miniprojeto_Varejo.py requirements.txt
git commit -m "Sprint 1: importacao do Varejo.csv com csv.DictReader"

# Sprint 2
git commit -am "Sprint 2: limpeza de strings, inteiros, decimais e datas"

# Sprint 3
git commit -am "Sprint 3: tratamento de nulos, duplicatas e inconsistencias"

# Sprint 4
git commit -am "Sprint 4: estatisticas de numero de filhos e agrupamentos"

# Sprint 5
git add README.md README_NomeDoAluno_Turma.md df_limpo.csv relatorio_insights.md
git commit -m "Sprint 5: relatorio final, insights e documentacao"

# Sprint 6: enviar ao GitHub
git remote add origin https://github.com/SEU_USUARIO/Miniprojeto_NomeAluno_Analise_de_Dados_T1.git
git push -u origin main
```

> Dica: como o script final já está pronto, para ter commits reais por sprint você pode ir adicionando o código
> por partes (um sprint de cada vez) antes de cada `git commit`, em vez de commitar tudo de uma vez.

Depois do push: confira se o repositório está **público** e envie o link na tarefa
*Módulo 1 – Mini-Projeto Avaliativo* (Semana 07) no AVA, **até 26/10/2026 às 22h**.
