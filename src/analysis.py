"""Estatística descritiva e indicadores das RQs. Entrada: DataFrame no formato de contract.py."""
import numpy as np
import pandas as pd


def cagr(inicio: float, fim: float, periodos: int) -> float:
    """Taxa média anual de crescimento composta (fração). NaN se inválida."""
    if inicio <= 0 or periodos <= 0:
        return float("nan")
    return (fim / inicio) ** (1 / periodos) - 1


def resumo_descritivo(s: pd.Series) -> pd.Series:
    s = s.dropna().astype(float)
    d = s.describe()
    d["amplitude"] = s.max() - s.min()
    d["cv"] = s.std(ddof=1) / s.mean() if s.mean() else np.nan
    return d


def _serie(df, escopo, col):
    return df[df.escopo == escopo].groupby("ano")[col].sum()


def rq1(df: pd.DataFrame) -> pd.DataFrame:
    """Matrículas (absolutas), participação da área no total e variações, por ano."""
    out = pd.DataFrame({
        "mat_computacao": _serie(df, "computacao_tic", "qt_mat"),
        "mat_total_graduacao": _serie(df, "total_graduacao", "qt_mat"),
    })
    out["participacao_pct"] = 100 * out.mat_computacao / out.mat_total_graduacao
    out["delta_participacao_pp"] = out.participacao_pct.diff()
    for c in ("mat_computacao", "mat_total_graduacao"):
        out[f"var_pct_{c}"] = 100 * out[c].pct_change()
        out[f"indice_{c}"] = 100 * out[c] / out[c].iloc[0]
    return out.reset_index()


def rq2(df: pd.DataFrame, escopo: str = "computacao_tic") -> pd.DataFrame:
    """Participação do EaD (%) em matrículas e ingressantes, por ano."""
    partes = []
    for indicador, col in (("matriculas", "qt_mat"), ("ingressantes", "qt_ing")):
        p = df[df.escopo == escopo].pivot_table(index="ano", columns="modalidade", values=col, aggfunc="sum")
        partes.append(pd.DataFrame({
            "ano": p.index, "escopo": escopo, "indicador": indicador,
            "qt_ead": p["ead"].to_numpy(), "qt_total": p.sum(axis=1).to_numpy(),
            "pct_ead": 100 * p["ead"].to_numpy() / p.sum(axis=1).to_numpy(),
        }))
    out = pd.concat(partes, ignore_index=True)
    out["delta_pp"] = out.groupby("indicador").pct_ead.diff()
    return out


def rq3(df: pd.DataFrame, escopo: str = "computacao_tic") -> pd.DataFrame:
    """Participação feminina (%) = F / (F + M), por modalidade e no total do escopo."""
    d = df[df.escopo == escopo]
    mod = d.groupby(["ano", "modalidade"])[["qt_mat_fem", "qt_mat_masc"]].sum().reset_index()
    tot = d.groupby("ano")[["qt_mat_fem", "qt_mat_masc"]].sum().reset_index().assign(modalidade="total")
    out = pd.concat([mod, tot], ignore_index=True).sort_values(["modalidade", "ano"])
    out["escopo"] = escopo
    out["pct_fem"] = 100 * out.qt_mat_fem / (out.qt_mat_fem + out.qt_mat_masc)
    out["delta_pp"] = out.groupby("modalidade").pct_fem.diff()
    return out.reset_index(drop=True)
