# Contrato de dados: ETL → análise

Implementação executável: `src/contract.py` (`validar`, `carregar`).
Responsável por produzir: ETL (ChatGPT). Responsável por consumir: análise e artigo (Claude).

## Entrega

| Arquivo | Conteúdo |
|---|---|
| `data/processed/agregado_anual.parquet` | tabela agregada abaixo |
| `data/processed/agregado_anual.meta.json` | metadados de proveniência |

**Grão:** uma linha por `(ano, escopo, modalidade)`. Grade completa: anos × 2 escopos × 2 modalidades (24 linhas para 2019–2024).

| Coluna | Tipo | Regra |
|---|---|---|
| `ano` | inteiro | ano do Censo |
| `escopo` | texto | `total_graduacao` ou `computacao_tic` (subconjunto do total) |
| `modalidade` | texto | `presencial` ou `ead` |
| `qt_mat` | inteiro ≥ 0 | matrículas |
| `qt_mat_fem` | inteiro ≥ 0 | matrículas, sexo feminino |
| `qt_mat_masc` | inteiro ≥ 0 | matrículas, sexo masculino |
| `qt_ing` | inteiro ≥ 0 | ingressantes |

Sem nulos, sem colunas extras, sem chave duplicada. `computacao_tic` ≤ `total_graduacao` em toda métrica.
Aviso (não bloqueante): `qt_mat_fem + qt_mat_masc ≠ qt_mat`.

## Metadados obrigatórios (`.meta.json`)

`origem` (`INEP` ou `SINTETICO`), `fonte_manifest` (caminho/hash do `manifest.json`), `gerado_em_utc`,
`regra_agregacao` (texto com a base na documentação oficial), `filtros` (nível acadêmico, área, dimensão, com contagens antes/depois).

## Responsabilidades do ETL (pontos abertos, a decidir com a auditoria)

1. Mapear códigos originais do INEP para `presencial`/`ead` e para os escopos. Registrar o mapeamento em `data/data_dictionary.md`.
2. `total_graduacao`: filtro de nível acadêmico (graduação) conforme dicionário oficial, sem sequenciais.
3. `computacao_tic`: área geral 06 da Cine Brasil, qualquer grau.
4. Regra de agregação/deduplicação (por exemplo `TP_DIMENSAO`) somente com base na documentação oficial.
5. Se `qt_ing` ou a divisão por sexo não existirem de forma confiável em algum ano, **não preencher**: sinalizar, e o contrato é revisado.

## Dados sintéticos

`src/synthetic.py` gera valores aleatórios com `origem = "SINTETICO"`. `carregar()` os recusa por padrão, as figuras levam marca d'água
e `viz.salvar` impede gravá-las em `docs/`.
