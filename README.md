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

A base agregada real já acompanha o projeto. Para executar a análise, use **Python 3.12**. A execução desta revisão foi verificada em **3.12.14**, com as versões fixadas em `requirements.txt`; a referência original do ETL era 3.12.3.

### Executar a análise no Windows (PowerShell)

Na raiz do projeto, com Python 3.12 instalado:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace notebooks/analise_exploratoria.ipynb
```

Esses comandos usam o Python do ambiente diretamente, sem depender da ativação do PowerShell. Se você já tem um ambiente Python 3.12 preparado, use o executável desse ambiente nos três últimos comandos.

### Executar a análise em Linux/macOS (Bash)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m nbconvert --to notebook --execute --inplace notebooks/analise_exploratoria.ipynb
```

O notebook lê `data/processed/agregado_anual.parquet`, valida o contrato, o SHA-256 do manifesto e a grade de 24 linhas (2019–2024), calcula as três RQs e regenera os CSVs e gráficos HTML/PNG em `docs/assets/`. As saídas foram comparadas aos CSVs do ZIP recebido, com tolerâncias absoluta e relativa de 1e-12.

### Ver o artigo pronto

[Artigo online](https://whitte77.github.io/censo-superior-tic/) · [arquivo local](docs/index.html).

Para servir a cópia local:

```bash
python -m http.server 8000 --directory docs
```

Abra `http://localhost:8000`. Também é possível abrir `docs/index.html` diretamente no navegador. Plotly usa CDN; os PNGs oferecem alternativa estática.

### Refazer o ETL completo (opcional para executar a análise)

Os seis ZIPs brutos do INEP não são versionados. No ambiente Python, obtenha-os com:

```bash
python -m src.download
```

Se a aquisição automática falhar por conectividade ou certificado TLS, baixe os seis ZIPs pela página oficial, em ambiente que valide o HTTPS, sem extrair, e coloque-os em `data/raw/` com nomes `microdados_censo_da_educacao_superior_ANO.zip`. Não desative a validação TLS. Os arquivos são verificados contra o manifesto existente; divergências exigem investigação.

Execute, na raiz, após obter os dados brutos:

```bash
python -m src.integrity
python -m src.inventory
python -m src.schema
python -m src.profile
python -m src.etl
python -m nbconvert --to notebook --execute --inplace notebooks/analise_exploratoria.ipynb
```

Os arquivos de texto usam LF por `.gitattributes`, preservando o hash do manifesto também em clones no Windows. A validação externa permanece parcial.

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

## Branches e fluxo do código

| Branch | Responsabilidade |
|---|---|
| `feat/engenharia-dados` | Base original do Hiago: aquisição, auditoria, ETL e Parquet real; commit `c8e67c0`. |
| `feat/analise-artigo` | Engenharia incorporada, contrato, indicadores, notebook executado e artigo. |
| `main` | Versão completa da entrega, com o mesmo código de `feat/analise-artigo`; fonte do GitHub Pages. |

Fluxo: `download/integrity/inventory/schema/profile/etl` → Parquet e metadados → `contract` → `analysis` → `viz` → `docs/assets` → artigo `docs/index.html`. O notebook coordena a leitura, análise e exportação; o artigo HTML apresenta as interpretações e deve ser revisado se os dados mudarem.

[Conferência item a item do guia](AUDITORIA_GUIA.md) · [instruções originais recebidas](INSTRUCOES_DUPLA.md).
