# Conferência do guia e das branches — 19/11/2026

## Resultado

A integração contém o ETL original, o Parquet real e os arquivos de análise do ZIP. A pendência de execução em Python 3.12 foi resolvida nesta revisão: as nove células de código foram executadas em Python 3.12.14, sem erros. Os três CSVs exportados continuam iguais aos do pacote recebido, com tolerâncias absoluta/relativa de 1e-12.

## Conferência item a item

A referência é o arquivo [INSTRUCOES_DUPLA.md](INSTRUCOES_DUPLA.md) recebido no ZIP e o guia de integração fornecido no chat.

| Pedido | Situação e evidência |
|---|---|
| Preservar alterações locais antes da integração | Foi usada uma cópia separada, inicialmente limpa; os outros clones do usuário não foram alterados. |
| Atualizar a análise com `feat/engenharia-dados` | Confirmado por ancestralidade Git: `c8e67c0` está contido na branch de análise. Partir diretamente desse commit atende ao resultado do merge pedido, sem um merge artificial. |
| Usar a branch `feat/analise-artigo` | Existe na conta `whitte77`. A revisão foi feita nela; a versão completa de `main` é mantida em sincronia por avanço direto. |
| Preservar `src/`, `data/`, `notebooks/` e `docs/` | Todos os arquivos pedidos estão presentes. Os sete módulos da engenharia e os bytes do Parquet foram comparados à branch original e permanecem iguais. |
| Confirmar Parquet e metadados | Presentes; origem INEP; grade completa de 24 linhas, 2019–2024, dois escopos e duas modalidades. SHA-256 do manifesto confere com os metadados. |
| Usar ambiente Python 3.12 e instalar `requirements.txt` | Executado em ambiente virtual isolado Python 3.12.14; instalação concluída e `pip check` sem dependências quebradas. A referência original do ETL era 3.12.3; a revisão utiliza a mesma série 3.12, em outro patch. |
| Executar o notebook real | Nove células de código executadas, nenhum erro. A versão do kernel consta dos metadados e da primeira saída do notebook. |
| Validar o contrato | Sem avisos. Também foram conferidas as rejeições de chave duplicada, grade incompleta, contagens negativas e escopo inválido. |
| Regenerar gráficos | Três HTML Plotly e três PNG Matplotlib presentes; as tabelas e os gráficos vieram do Parquet real. A conferência visual do artigo e dos gráficos foi realizada na integração/publicação. |
| Comparar CSVs ao ZIP | RQ1: 6 linhas; RQ2: 12; RQ3: 18. Todos os CSVs efetivamente exportados coincidem com o ZIP e com os cálculos de `analysis.py`. |
| Separar dados sintéticos | Leitura padrão de sintéticos recusada, marca d’água presente e gravação de figuras sintéticas em `docs/` bloqueada. |
| Completar autor e professor | Hiago Arruda e Alessandro Davi; professor Alexandre Neves Louzada. Os dados de Alessandro e do professor vieram do projeto anterior da mesma disciplina. Nenhum campo de preenchimento permanece no artigo. |
| Conferir semestre | Mantido 2026.2, compatível com a atividade de novembro de 2026; o calendário específico da turma não foi consultado. |
| Conferir referências bibliográficas | Conferidas na etapa de integração: páginas editoriais SBC, metadados DOI/Crossref, anais SciPy e documentação Plotly. DOIs e páginas SBC incluídos; referência genérica do Plotly corrigida. |
| Conferir termos de reutilização | Fonte INEP e política de dados abertos citadas; licença específica dos seis pacotes não confirmada. A licença MIT é do código e não foi estendida aos dados. |
| Atualizar README com 12/12 MD5 e validação externa parcial | Feito. As 12 linhas do relatório recebido têm status OK e MD5 esperado/calculado coincidentes. Os ZIPs brutos não foram baixados novamente nesta revisão. |
| Preservar mensagens completas em caso de erro | Não houve erro de execução. A saída de `nbconvert`, incluindo avisos do Jupyter no Windows, foi registrada em `data/processed/audit/execucao_python312.txt`, com caminhos locais substituídos por marcadores. |
| Conferir artigo e commitar arquivos | Arquivos pedidos versionados. Artigo publicado pelo GitHub Pages a partir de `main/docs`. |

## Como as branches devem ficar

| Branch | Conteúdo | Uso |
|---|---|---|
| `feat/engenharia-dados` | Engenharia original do Hiago, commit `c8e67c0` | Referência do ETL e da base; preservada. |
| `feat/analise-artigo` | Base da engenharia mais contrato, indicadores, notebook, gráficos e artigo | Desenvolvimento e revisão da análise. |
| `main` | Versão completa da entrega, igual à análise nesta revisão | Clonar/executar o trabalho completo e publicar o artigo. |

A análise já inclui a engenharia; não há necessidade de copiar os módulos do ETL por cima dela. Para mudanças futuras, desenvolva em `feat/analise-artigo`, execute o notebook, revise as tabelas e interpretações e então integre em `main`. A branch `feat/engenharia-dados` continua como referência original até uma nova entrega do responsável pelo ETL.

## Como o código se encaixa

1. `src/download.py`: obtém os seis ZIPs oficiais, quando for necessário refazer o ETL.
2. `src/integrity.py`, `inventory.py`, `schema.py` e `profile.py`: conferem integridade e estrutura dos dados brutos.
3. `src/etl.py`: agrega os dados e entrega `data/processed/agregado_anual.parquet` e os metadados de proveniência.
4. `src/contract.py`: valida o formato entregue pelo ETL e controla a aceitação de dados sintéticos.
5. `src/analysis.py`: calcula os indicadores RQ1, RQ2 e RQ3 e as estatísticas descritivas.
6. `src/viz.py`: transforma os indicadores em gráficos interativos e estáticos.
7. `notebooks/analise_exploratoria.ipynb`: coordena leitura, validação, análise e exportação de gráficos/CSVs.
8. `docs/index.html`: apresenta o artigo, as interpretações e os gráficos exportados. O texto interpretativo deve ser revisado quando os dados mudarem; não é reescrito automaticamente pelo notebook.

Para apenas repetir a análise, comece pelo notebook: o Parquet já está incluído e não é preciso baixar os microdados brutos.

## Evidências e limites

- `data/processed/audit/verificacao_guia.json`: ancestralidade, preservação do ETL/Parquet, kernel e comparações dos CSVs.
- `data/processed/audit/verificacao_integracao.json`: verificações estruturais e proteções de sintéticos, repetidas em Python 3.12.14.
- `data/processed/audit/execucao_python312.txt`: registro da execução em Python 3.12.

A reconciliação externa integral das estatísticas, a auditoria de reclassificações em nível de curso e a confirmação de uma licença específica dos pacotes continuam abertas e são declaradas no artigo. A revisão não afirma validação externa integral nem reexecução dos MD5 sobre os ZIPs brutos.
