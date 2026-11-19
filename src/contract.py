"""Contrato de dados entre o ETL e a análise.

Entrega do ETL:  data/processed/agregado_anual.parquet + agregado_anual.meta.json
Grão:            1 linha por (ano, escopo, modalidade)
Escopos:         total_graduacao (toda a graduação) e computacao_tic (subconjunto do total)
Os nomes de colunas ORIGINAIS do INEP não aparecem aqui: o mapeamento original -> contrato
é responsabilidade do ETL e deve constar em data/data_dictionary.md.
"""
import json
import pandas as pd

COLUNAS = {
    "ano": "inteiro",
    "escopo": "texto: total_graduacao | computacao_tic",
    "modalidade": "texto: presencial | ead",
    "qt_mat": "inteiro >= 0 (matrículas)",
    "qt_mat_fem": "inteiro >= 0 (matrículas, sexo feminino)",
    "qt_mat_masc": "inteiro >= 0 (matrículas, sexo masculino)",
    "qt_ing": "inteiro >= 0 (ingressantes)",
}
ESCOPOS = ("total_graduacao", "computacao_tic")
MODALIDADES = ("presencial", "ead")
CHAVE = ["ano", "escopo", "modalidade"]
METRICAS = ["qt_mat", "qt_mat_fem", "qt_mat_masc", "qt_ing"]
META_OBRIGATORIA = ("origem", "fonte_manifest", "gerado_em_utc", "regra_agregacao", "filtros")
ORIGENS = ("INEP", "SINTETICO")


class ContratoError(ValueError):
    """Violação estrutural do contrato: a análise não deve prosseguir."""


def validar(df: pd.DataFrame, meta: dict | None = None) -> list[str]:
    """Levanta ContratoError em violações estruturais; devolve avisos (não bloqueantes)."""
    faltam, extras = set(COLUNAS) - set(df.columns), set(df.columns) - set(COLUNAS)
    if faltam or extras:
        raise ContratoError(f"colunas: faltam={sorted(faltam)} extras={sorted(extras)}")
    if df[list(COLUNAS)].isna().any().any():
        raise ContratoError("há valores nulos")
    for c in ["ano", *METRICAS]:
        if not pd.api.types.is_integer_dtype(df[c]):
            raise ContratoError(f"{c}: esperado inteiro")
    if (df[METRICAS] < 0).any().any():
        raise ContratoError("há contagens negativas")
    if not df.escopo.isin(ESCOPOS).all() or not df.modalidade.isin(MODALIDADES).all():
        raise ContratoError("escopo/modalidade fora do domínio")
    if df.duplicated(CHAVE).any():
        raise ContratoError("chave (ano, escopo, modalidade) duplicada")
    esperado = df.ano.nunique() * len(ESCOPOS) * len(MODALIDADES)
    if len(df) != esperado:
        raise ContratoError(f"grade incompleta: {len(df)} linhas, esperado {esperado}")
    p = df.pivot_table(index=["ano", "modalidade"], columns="escopo", values=METRICAS, aggfunc="sum")
    for m in METRICAS:
        if (p[(m, "computacao_tic")] > p[(m, "total_graduacao")]).any():
            raise ContratoError(f"{m}: computacao_tic maior que total_graduacao")
    avisos = []
    n = int((df.qt_mat_fem + df.qt_mat_masc != df.qt_mat).sum())
    if n:
        avisos.append(f"{n} linha(s) com qt_mat_fem + qt_mat_masc != qt_mat")
    if meta is not None:
        ausentes = [k for k in META_OBRIGATORIA if k not in meta]
        if ausentes:
            raise ContratoError(f"meta sem chaves obrigatórias: {ausentes}")
        if meta["origem"] not in ORIGENS:
            raise ContratoError(f"origem inválida: {meta['origem']}")
    return avisos


def carregar(parquet: str, meta_json: str, aceitar_sintetico: bool = False):
    """Lê, valida e devolve (df, meta). Dados sintéticos só entram com aceitar_sintetico=True."""
    df = pd.read_parquet(parquet)
    with open(meta_json, encoding="utf-8") as f:
        meta = json.load(f)
    avisos = validar(df, meta)
    if meta["origem"] == "SINTETICO" and not aceitar_sintetico:
        raise ContratoError("dados sintéticos recusados (aceitar_sintetico=False)")
    df.attrs.update(origem=meta["origem"], avisos=avisos)
    return df, meta
