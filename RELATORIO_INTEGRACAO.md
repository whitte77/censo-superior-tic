# Relatório da integração — 19/11/2026

## Pedido recebido e execução

O ZIP solicitava integrar análise e artigo à branch de engenharia de dados, executar o notebook sobre o Parquet real, comparar as saídas, completar identificação, revisar referências e atualizar a documentação sem declarar validação externa integral.

Foi criada uma cópia separada do repositório https://github.com/H-Arruda/censo-superior-tic, baseada em `origin/feat/engenharia-dados`, commit `c8e67c015eb04b898a099f04991409cda083d7b2`. A integração está na branch local `feat/integracao-analise-artigo`. Nenhum outro clone foi alterado. Na etapa inicial de integração, não houve push, publicação nem envio a terceiros. O envio posterior foi solicitado pelo usuário e é registrado ao final deste relatório.

## Concluído

- Integração de `analysis.py`, `contract.py`, `synthetic.py`, `viz.py`, contrato de dados, notebook e artigo.
- Instalação de todas as versões de `requirements.txt` em ambiente virtual isolado; `pip check`: nenhuma dependência quebrada.
- Notebook executado integralmente: 9 células de código, sem erros. Python 3.14.7; pandas 3.1.1; PyArrow 26.0.1; NumPy 2.5.5; Matplotlib 3.11.2; Plotly 7.1.0. Python 3.12 permanece como versão de referência do ETL, sem nova execução nesta versão.
- Parquet real: 24 linhas, anos 2019–2024, contrato sem avisos. SHA-256 do manifesto conferido com os metadados: `e7411a740fc5e2db70ff77903343fca5ce339cc6c60e3133edad4bc2c7dbd4d5`.
- Três CSVs regenerados comparados aos originais: RQ1, 6 linhas; RQ2, 12; RQ3, 18. Todos iguais com tolerâncias absoluta/relativa de 1e-12.
- Gráficos HTML e PNG regenerados; artigo e três gráficos conferidos no navegador. Títulos sobrepostos do primeiro gráfico corrigidos.
- Links locais do artigo conferidos e arquivos presentes.
- Testes de rejeição de chave duplicada, grade incompleta, contagem negativa e escopo inválido passaram. Leitura padrão de sintéticos e exportação de figuras sintéticas para docs foram bloqueadas; marcas d’água confirmadas.
- `.gitattributes` adicionado para preservar LF. O checkout Windows alterava as quebras de linha do manifesto, causando divergência de hash; os bytes originais foram preservados sem alterar o conteúdo dos dados.
- README e dicionário corrigidos: o relatório versionado registra 12/12 MD5 correspondentes, e a validação externa é parcial.

## Identificação

Autores: Hiago Arruda e Alessandro Davi. Professor: Alexandre Neves Louzada. Instituição e curso mantidos do artigo: UNILASALLE-RJ, Sistemas de Informação. Nome de Alessandro e do professor obtidos do README do projeto local anterior da mesma disciplina (`Documents/Github/Analise_Dados`). Semestre 2026.2 mantido, compatível com a data da atividade em novembro de 2026; o calendário específico da turma não foi consultado.

## Bibliografia e termos dos dados

- Cursino e Martinez (2021): autoria, título, data, páginas 21–30 e DOI conferidos nos metadados da página editorial da SBC: https://sol.sbc.org.br/index.php/wit/article/view/15838 — DOI 10.5753/wit.2021.15838.
- Saraiva et al. (2023): autoria, título, data, páginas 443–453 e DOI conferidos na SBC: https://sol.sbc.org.br/index.php/wei/article/view/24924 — DOI 10.5753/wei.2023.229974.
- NumPy, Matplotlib e FAIR: existência, autoria e metadados conferidos via Crossref nos DOIs citados. pandas: conferido nos anais oficiais SciPy, https://proceedings.scipy.org/articles/Majora-92bf1922-00a.
- A referência genérica do Plotly foi substituída pela documentação oficial da biblioteca Python: https://plotly.com/python/.
- Página oficial de microdados consultada, com as seis edições: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior.
- Política de dados abertos consultada: https://download.inep.gov.br/publicacoes/institucionais/gestao_e_governanca/politica_e_plano_de_dados_abertos.pdf. Não foi atribuída licença MIT aos dados do INEP; a licença específica dos seis pacotes permanece não confirmada. O artigo inclui essa ressalva e a atribuição da fonte.

## Limites da conferência

Os ZIPs brutos não acompanham o clone. O ETL e os 12 MD5 não foram reexecutados nesta integração: foi inspecionado o relatório `data/processed/audit/integrity.csv`, com 12 registros OK e hashes esperado/calculado coincidentes. Também não houve reconciliação externa integral das estatísticas, nem auditoria de chaves e reclassificações em nível de curso. A execução confirma a análise sobre o Parquet recebido, sem substituir essas auditorias.

Os gráficos interativos dependem da CDN Plotly; os PNGs oferecem alternativa estática. As práticas FAIR foram descritas sem afirmar certificação ou avaliação formal.

## Arquivos da entrega

- `docs/index.html`: artigo revisado; manter a pasta `assets/` ao lado.
- `notebooks/analise_exploratoria.ipynb`: notebook executado.
- `data/processed/agregado_anual.parquet` e metadados: base real recebida da branch de engenharia.
- `data/processed/audit/comparacao_csvs.json` e `verificacao_integracao.json`: registros das verificações desta integração.
- `README.md`: comandos para execução, fonte, limitações e condições de reutilização.

O pacote ZIP contém o projeto completo sem o ambiente virtual e sem a pasta `.git`. O patch separado registra o commit local, com autoria técnica `Codex <codex@localhost>`. Para aplicar o patch em outro clone, atualize a branch com `origin/feat/engenharia-dados`, crie uma branch de integração e execute `git am caminho/para/integracao-analise-artigo.patch`. A publicação posterior no GitHub está registrada abaixo.

## Publicação solicitada posteriormente — 19/11/2026

Conta confirmada por autenticação: `whitte77` (Alessandro Davi). Repositório: https://github.com/whitte77/censo-superior-tic. A versão integrada é disponibilizada em `main` e em `feat/analise-artigo`; a branch de origem do ETL é preservada em `feat/engenharia-dados`. O histórico original e a licença MIT foram preservados. Artigo: https://whitte77.github.io/censo-superior-tic/. A publicação não altera as limitações estatísticas e de validação externa descritas acima.

## Revisão do guia e das branches — 19/11/2026

A verificação posterior foi executada em Python 3.12.14, em ambiente virtual isolado, com instalação integral de `requirements.txt`, `pip check` sem conflitos e nove células do notebook executadas sem erros. Os CSVs exportados continuam iguais aos do ZIP recebido. A versão 3.14.7 registrada acima corresponde à etapa inicial; o notebook e a versão Python de referência desta entrega foram agora atualizados para 3.12.14.

A ancestralidade Git e a igualdade dos módulos do ETL/Parquet em relação à branch original foram verificadas. A documentação passou a distinguir a execução da análise (base já incluída) da reconstrução opcional do ETL (exige os ZIPs brutos). Consulte [a conferência completa](AUDITORIA_GUIA.md), com cada item do guia, as responsabilidades de cada branch e o fluxo entre os módulos. As limitações externas anteriores permanecem válidas.
