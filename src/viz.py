"""Gráficos Plotly (interativos, para o artigo) e Matplotlib (estáticos). Entradas: saídas de analysis.rq1/rq2/rq3."""
from math import ceil
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter
import plotly.graph_objects as go
from plotly.subplots import make_subplots

AVISO = "DADOS SINTÉTICOS — APENAS TESTE"
COR = {"principal": "#0f5c6e", "segunda": "#b8590f", "neutra": "#6b7785"}
ROTULO_MOD = {"presencial": "Presencial", "ead": "EaD", "total": "Total"}
COR_MOD = {"presencial": COR["principal"], "ead": COR["segunda"], "total": COR["neutra"]}


def _marca_plotly(fig, sint):
    if sint:
        fig.add_annotation(text=AVISO, xref="paper", yref="paper", x=.5, y=.5, showarrow=False,
                           font=dict(size=28, color="rgba(200,0,0,.35)"), textangle=-20)
    return fig


def _marca_mpl(fig, sint):
    if sint:
        fig.text(.5, .5, AVISO, ha="center", va="center", rotation=20, fontsize=24, color="red", alpha=.3)
    return fig


def plotly_rq1(r1, sintetico=False):
    f = make_subplots(rows=1, cols=2, subplot_titles=("Matrículas em<br>Computação e TIC", "Participação na<br>graduação (%)"))
    f.add_bar(x=r1.ano, y=r1.mat_computacao, marker_color=COR["principal"], name="Matrículas", row=1, col=1)
    f.add_scatter(x=r1.ano, y=r1.participacao_pct, mode="lines+markers", line_color=COR["segunda"], name="Participação (%)", row=1, col=2)
    f.update_yaxes(rangemode="tozero")
    f.update_xaxes(dtick=1)
    f.update_layout(template="simple_white", showlegend=False, margin=dict(t=60, b=40))
    return _marca_plotly(f, sintetico)


def plotly_rq2(r2, sintetico=False):
    f = go.Figure()
    for ind, cor in (("matriculas", COR["principal"]), ("ingressantes", COR["segunda"])):
        d = r2[r2.indicador == ind]
        f.add_scatter(x=d.ano, y=d.pct_ead, mode="lines+markers", name=ind.capitalize(), line_color=cor)
    f.update_layout(template="simple_white", title="Participação do EaD (%)", yaxis=dict(range=[0, 100], title="% EaD"),
                    xaxis=dict(dtick=1, title="Ano"), legend_title_text="")
    return _marca_plotly(f, sintetico)


def _limite_rq3(r3):
    maior = r3.pct_fem.max()
    return min(100, 5 * ceil((max(20, maior) + 3) / 5))


def _rotulo_pct(valor):
    return f"{valor:.2f}%".replace(".", ",")


def plotly_rq3(r3, sintetico=False):
    f = go.Figure()
    for mod, d in r3.groupby("modalidade"):
        d = d.sort_values("ano")
        ultimo = d.iloc[-1]
        cor = COR_MOD[mod]
        f.add_scatter(x=d.ano, y=d.pct_fem, mode="lines+markers+text",
                      name=ROTULO_MOD[mod], line_color=cor,
                      text=[""] * (len(d) - 1) + [_rotulo_pct(ultimo.pct_fem)],
                      textposition="middle right", textfont=dict(color=cor),
                      hovertext=[_rotulo_pct(valor) for valor in d.pct_fem],
                      hovertemplate="%{x}: %{hovertext}")
    primeiro_ano, ultimo_ano = r3.ano.min(), r3.ano.max()
    f.update_layout(template="simple_white", title="Participação feminina nas matrículas (%)",
                    separators=",.", margin=dict(l=48, r=12, t=94, b=50),
                    yaxis=dict(range=[0, _limite_rq3(r3)], title="Participação",
                               dtick=5, ticksuffix="%"),
                    xaxis=dict(tickvals=sorted(r3.ano.unique()), title="Ano",
                               range=[primeiro_ano - .25, ultimo_ano + 1.5]),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02))
    return _marca_plotly(f, sintetico)


def mpl_rq1(r1, sintetico=False):
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4))
    a.bar(r1.ano, r1.mat_computacao, color=COR["principal"]); a.set(title="Matrículas em Computação e TIC", xlabel="Ano", ylabel="Matrículas")
    b.plot(r1.ano, r1.participacao_pct, marker="o", color=COR["segunda"]); b.set(title="Participação no total da graduação", xlabel="Ano", ylabel="%", ylim=(0, None))
    for ax in (a, b): ax.set_xticks(list(r1.ano))
    fig.tight_layout()
    return _marca_mpl(fig, sintetico)


def mpl_rq2(r2, sintetico=False):
    fig, ax = plt.subplots(figsize=(6, 4))
    for ind, cor in (("matriculas", COR["principal"]), ("ingressantes", COR["segunda"])):
        d = r2[r2.indicador == ind]; ax.plot(d.ano, d.pct_ead, marker="o", color=cor, label=ind.capitalize())
    ax.set(title="Participação do EaD (%)", xlabel="Ano", ylabel="% EaD", ylim=(0, 100)); ax.set_xticks(sorted(r2.ano.unique())); ax.legend()
    fig.tight_layout()
    return _marca_mpl(fig, sintetico)


def mpl_rq3(r3, sintetico=False):
    fig, ax = plt.subplots(figsize=(6, 4))
    for mod, d in r3.groupby("modalidade"):
        d = d.sort_values("ano")
        ultimo = d.iloc[-1]
        cor = COR_MOD[mod]
        ax.plot(d.ano, d.pct_fem, marker="o", color=cor, label=ROTULO_MOD[mod])
        ax.annotate(_rotulo_pct(ultimo.pct_fem), (ultimo.ano, ultimo.pct_fem),
                    xytext=(7, 0), textcoords="offset points", va="center", color=cor)
    ax.set(title="Participação feminina nas matrículas (%)", xlabel="Ano",
           ylabel="Participação", ylim=(0, _limite_rq3(r3)))
    ax.set_xticks(sorted(r3.ano.unique()))
    ax.set_xlim(r3.ano.min() - .25, r3.ano.max() + 1)
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.legend(loc="upper left", ncol=3)
    fig.tight_layout()
    return _marca_mpl(fig, sintetico)


def salvar(nome, fig_plotly, fig_mpl, pasta, sintetico=False):
    """HTML (Plotly, para iframe) e PNG (Matplotlib). Figuras sintéticas nunca vão para docs/."""
    pasta = Path(pasta)
    if sintetico and "docs" in pasta.parts:
        raise ValueError("figuras sintéticas não podem ser salvas em docs/")
    pasta.mkdir(parents=True, exist_ok=True)
    fig_plotly.update_layout(height=390)
    fig_plotly.write_html(pasta / f"{nome}.html", include_plotlyjs="cdn", full_html=True)
    fig_mpl.savefig(pasta / f"{nome}.png", dpi=200, bbox_inches="tight")
