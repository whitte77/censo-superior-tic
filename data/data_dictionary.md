# Dicionário de dados

**Fonte:** INEP — Censo da Educação Superior, 2019–2024. [Microdados oficiais](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior).

## Entrada: cadastro de cursos

CSV separado por `;`, lido com codificação Latin-1 e inicialmente como texto, preservando códigos e valores vazios. Definições baseadas nos dicionários oficiais distribuídos nos ZIPs.

| Variável | Tipo lógico | Definição e domínio |
|---|---|---|
| NU_ANO_CENSO | Inteiro | Ano de referência do Censo (2019 a 2024). |
| TP_DIMENSAO | Categórico | 1: presencial no Brasil; 2: EaD no Brasil; 3: EaD com dados somente no nível Brasil; 4: EaD no exterior. |
| TP_NIVEL_ACADEMICO | Categórico | 1: graduação; 2: sequencial de formação específica. |
| TP_MODALIDADE_ENSINO | Categórico | 1: presencial; 2: a distância. |
| CO_CINE_AREA_GERAL | Texto (2 caracteres) | Código da área geral da Cine Brasil; 06 identifica Computação e TIC. |
| NO_CINE_AREA_GERAL | Texto | Nome da área geral correspondente. |
| QT_MAT | Inteiro não negativo | Matrículas: vínculos com situação cursando ou formado. |
| QT_MAT_FEM | Inteiro não negativo | Matrículas do sexo feminino. |
| QT_MAT_MASC | Inteiro não negativo | Matrículas do sexo masculino. |
| QT_ING | Inteiro não negativo | Quantidade de ingressantes no ano de referência. |

## Saída: agregado_anual.parquet

Granularidade: ano × escopo × modalidade. Chave composta: `ano`, `escopo`, `modalidade`. São 24 linhas esperadas, sem índice persistido.

| Variável | Tipo | Definição |
|---|---|---|
| ano | int64 | Ano do Censo. |
| escopo | string | `total_graduacao` (todas as áreas) ou `computacao_tic` (área 06, subconjunto do total). |
| modalidade | string | `presencial` ou `ead`. |
| qt_mat | int64 | Soma das matrículas no grupo. |
| qt_mat_fem | int64 | Soma das matrículas femininas no grupo. |
| qt_mat_masc | int64 | Soma das matrículas masculinas no grupo. |
| qt_ing | int64 | Soma dos ingressantes no grupo. |

## Regras e limitações

- Apenas graduação e ofertas no Brasil (dimensões 1 e 2).
- Dimensão 3 excluída: métricas de matrícula e ingresso vazias em 2019 e iguais a zero nos demais anos, conforme validação do ETL. Dimensão 4 excluída pelo recorte geográfico.
- Quantidades retidas devem ser inteiras não negativas e `qt_mat_fem + qt_mat_masc = qt_mat`.
- Os escopos se sobrepõem: não somar `total_graduacao` e `computacao_tic`.
- Matrículas representam vínculos, não pessoas únicas. Não se deduplicam registros por código de curso; a auditoria de chaves e reclassificações individuais ainda não foi concluída.
- Sexo segundo as categorias do INEP, não uma medida abrangente de identidade de gênero.
- Indicadores de participação usam razões entre somas; denominador zero implica indicador indefinido.
- O relatório versionado registra 12/12 MD5 correspondentes aos manifestos internos dos ZIPs. A reconciliação externa integral permanece pendente; consultar os relatórios de auditoria e metadados.
