"""DADOS SINTÉTICOS — exclusivamente para testar código. Não representam o Brasil nem o INEP.
Escala deliberadamente pequena e valores aleatórios, sem tendência intencional."""
import numpy as np
import pandas as pd
from .contract import ESCOPOS, MODALIDADES


def gerar(anos=range(2019, 2025), seed: int = 42):
    rng = np.random.default_rng(seed)
    linhas = []
    for ano in anos:
        for mod in MODALIDADES:
            tot = int(rng.integers(40_000, 90_000))
            comp = int(tot * rng.uniform(0.05, 0.20))
            for escopo, mat in zip(ESCOPOS, (tot, comp)):
                fem = int(mat * rng.uniform(0.15, 0.60))
                linhas.append(dict(ano=ano, escopo=escopo, modalidade=mod, qt_mat=mat,
                                   qt_mat_fem=fem, qt_mat_masc=mat - fem,
                                   qt_ing=int(mat * rng.uniform(0.2, 0.4))))
    df = pd.DataFrame(linhas)
    df.attrs["origem"] = "SINTETICO"
    meta = dict(origem="SINTETICO", fonte_manifest="n/a", gerado_em_utc="n/a",
                regra_agregacao="n/a (valores aleatórios)", filtros="n/a", seed=seed)
    return df, meta
