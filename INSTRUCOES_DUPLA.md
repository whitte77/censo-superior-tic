# Integração da análise

1. Atualizar a branch da dupla com `origin/feat/engenharia-dados` antes de copiar os arquivos.
2. Extrair este ZIP na raiz do clone, preservando as pastas. Não inclui ETL nem dados brutos.
3. Ativar o ambiente Python e executar `python -m pip install -r requirements.txt`.
4. Na raiz: `jupyter nbconvert --to notebook --execute --inplace notebooks/analise_exploratoria.ipynb`. O notebook deve ler o Parquet real, validar o contrato e regenerar os gráficos.
5. Comparar os CSVs regenerados com os do pacote. Os gráficos e textos iniciais foram calculados com as 24 linhas do log do ETL; neste ambiente não foi possível abrir o Parquet por ausência de PyArrow.
6. Completar autor, professor, conferir semestre, referências bibliográficas herdadas do Claude e os termos de reutilização dos dados. Atualizar README (12/12 MD5 confirmados; validação externa ainda parcial). Não declarar validação externa integral.
7. Abrir docs/index.html, conferir gráficos (Plotly usa CDN; PNG disponível), commitar src/analysis.py src/contract.py src/synthetic.py src/viz.py data/data_contract.md notebooks/analise_exploratoria.ipynb docs/.
