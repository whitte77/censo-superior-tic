# Censo Superior TIC (2019–2024)

Análise exploratória da evolução da formação superior em Computação e Tecnologias da Informação e Comunicação no Brasil com microdados do INEP.

**Autores:** Hiago Arruda; Alessandro Davi

**Instituição:** UNILASALLE-RJ — Bacharelado em Sistemas de Informação

**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python

**Professor:** Alexandre Neves Louzada

**Semestre:** 2026.2

**Palavras-chave:** ensino superior; Computação e TIC; educação a distância; participação feminina; engenharia de dados; INEP.

## Perguntas de pesquisa

1. Como evoluíram as matrículas em TIC, em números absolutos e em proporção ao total da graduação?
2. Como evoluiu a participação do EaD nas matrículas e nos ingressos em TIC?
3. Como evoluiu a participação feminina nas matrículas em TIC por modalidade?

## Fonte e recorte

[Microdados do Censo da Educação Superior — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior). Período de 2019 a 2024; graduação ofertada no Brasil; área geral 06 da Cine Brasil para TIC. As dimensões 3 e 4 são excluídas das métricas estudadas conforme as regras documentadas em `data/data_dictionary.md`.

## Reprodução

Python 3.12.3 de referência do ETL; integração executada e verificada em Python 3.14.7, com as versões de `requirements.txt`. Execute na raiz do repositório, em Bash:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m src.download
```

Se a aquisição automática falhar por conectividade ou certificado TLS, baixe os seis ZIPs pela página oficial, em ambiente que valide o HTTPS, sem extrair, e coloque-os em `data/raw/` com nomes `microdados_censo_da_educacao_superior_ANO.zip`. Não desative a validação TLS. O ETL registra aquisições manuais e verifica arquivos contra o manifesto existente; arquivos divergentes não devem ser substituídos sem investigação.

```bash
mkdir -p data/processed/audit
set -o pipefail
python -m src.integrity | tee data/processed/audit/integrity.log
python -m src.inventory | tee data/processed/audit/inventory.log
python -m src.schema | tee data/processed/audit/schema.log
python -m src.profile | tee data/processed/audit/profile.log
python -m src.etl | tee data/processed/audit/etl.log
```

Após gerar o Parquet, execute a análise na raiz:

```bash
python -m nbconvert --to notebook --execute --inplace notebooks/analise_exploratoria.ipynb
```

A cópia integrada inclui o Parquet real de 24 linhas e os metadados versionados na branch de engenharia de dados. Para refazer apenas a análise, os ZIPs brutos não são necessários: instale as dependências e execute o comando acima. Para refazer o ETL, obtenha os seis ZIPs oficiais primeiro.

O notebook valida o contrato, o SHA-256 do manifesto e o período 2019–2024; produz `docs/assets/rq1.csv`, `rq2.csv`, `rq3.csv` e gráficos HTML/PNG. Os resultados foram comparados aos CSVs recebidos, com tolerância numérica de 1e-12.

[Artigo local](docs/index.html). O artigo é publicado pelo GitHub Pages a partir de `main`, pasta `docs/`: [abrir artigo](https://whitte77.github.io/censo-superior-tic/). Para visualizar por HTTP, execute `python -m http.server 8000 --directory docs` e abra `http://localhost:8000`. Os gráficos interativos usam a CDN do Plotly; versões PNG estão disponíveis no artigo.

No PowerShell, a preparação do ambiente é:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m nbconvert --to notebook --execute --inplace notebooks/analise_exploratoria.ipynb
```

Os arquivos de texto usam LF por `.gitattributes`, preservando o hash do manifesto também em clones no Windows.

## Estrutura

- `src/`: módulos de aquisição, inventário, inspeção de dicionários, perfil e ETL.
- `data/raw/`: arquivos oficiais locais (não versionados) e manifesto de procedência.
- `data/processed/`: resultados gerados pelo pipeline e relatórios de auditoria.
- `data/data_dictionary.md`: metadados das variáveis originais e derivadas.
- `notebooks/`: análise exploratória.
- `docs/`: artigo e visualizações para publicação.

## Declaração FAIR

- **Localizável:** descrição, palavras-chave, autoria e fonte oficial no README.
- **Acessível:** código e instruções disponíveis no repositório público; dados originais obtidos na fonte oficial sem credenciais pagas.
- **Interoperável:** saída Parquet, relatórios CSV e metadados JSON, com dicionário de dados.
- **Reutilizável:** código autoral sob licença MIT, dependências congeladas e regras de transformação documentadas. A licença do código não se estende aos dados de terceiros; observar os termos aplicáveis do INEP.

## Validação e limitações

A execução dos seis anos gerou 24 linhas. O manifesto registra SHA-256 e a verificação CRC dos ZIPs; a aquisição manual não registrou cabeçalhos HTTP nem instante exato de download. A auditoria verificou os domínios e a identidade entre as contagens por sexo nos registros retidos. O relatório de integridade recebido e versionado registra **12/12 MD5 correspondentes** aos manifestos distribuídos dentro dos ZIPs; essa verificação não foi repetida nesta integração, pois os arquivos brutos não acompanham o repositório. A validação externa é **parcial**: a reconciliação externa integral e a auditoria de chaves/reclassificações permanecem pendentes. MD5 e CRC verificam integridade e não equivalem a reconciliação com estatísticas externas. Matrículas não equivalem a pessoas únicas; o estudo é descritivo e não identifica efeitos causais.

## Revisão bibliográfica e reutilização

As referências foram conferidas nas páginas editoriais da SBC, nos metadados DOI/Crossref, nos anais SciPy e na documentação oficial do Plotly; DOIs e páginas dos artigos SBC foram incluídos. A referência genérica do Plotly foi substituída pela documentação da biblioteca Python.

A fonte oficial disponibiliza as seis edições utilizadas. A política de dados abertos do INEP descreve a reutilização com crédito da autoria ou fonte ([política oficial](https://download.inep.gov.br/publicacoes/institucionais/gestao_e_governanca/politica_e_plano_de_dados_abertos.pdf)). Uma licença específica dos seis pacotes não foi confirmada; por isso não se atribui MIT aos dados. Consulte [o registro da integração](RELATORIO_INTEGRACAO.md).

## Repositório e origem da engenharia de dados

[Repositório desta entrega](https://github.com/whitte77/censo-superior-tic). A engenharia de dados e seu histórico foram incorporados de [H-Arruda/censo-superior-tic](https://github.com/H-Arruda/censo-superior-tic), branch `feat/engenharia-dados`, commit `c8e67c0`. A licença MIT e a atribuição original foram preservadas.
