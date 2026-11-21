import streamlit as st
import pandas as pd
import altair as alt


# 1. CONFIGURACAO DA PAGINA


st.set_page_config(
    page_title="SUS Data Insights",
    page_icon="🏥",
    layout="wide"
)

# Paleta (baseada na imagem de referencia)
ROXO = "#5B4DA6"
ROXO_ESCURO = "#5A2A7A"
FUNDO = "#BBB3CC"


# 2. ESTILO VISUAL


st.markdown(f"""
<style>
    .stApp {{ background-color: {FUNDO}; }}

    /* Remove barra superior e ajusta margens */
    header[data-testid="stHeader"] {{ display: none; }}
    .block-container {{
        padding-top: 0 !important;
        padding-bottom: 2rem;
        max-width: 100%;
    }}

    [data-testid="stSidebar"] {{ background-color: #E4DFEE; }}

    /* Cabecalho branco */
    .st-key-cabecalho {{
        background-color: #FFFFFF;
        border-bottom: 1px solid #CFCFCF;
        margin: 0 -5rem 1.5rem -5rem;
        padding: 1.2rem 5rem 0.8rem 5rem;
    }}
    .titulo {{
        color: #1A1A1A;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.3px;
        margin: 0 0 14px 0;
        text-transform: uppercase;
    }}
    .rotulo-periodo {{
        font-size: 13px;
        font-weight: 700;
        padding-top: 8px;
    }}
    .st-key-cabecalho [data-testid="stDateInput"] label {{ display: none; }}
    .st-key-cabecalho [data-baseweb="input"] {{
        border-radius: 6px;
        background: #FFFFFF;
    }}

    /* Cartoes de KPI */
    [data-testid="stMetric"] {{
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }}
    [data-testid="stMetricLabel"] {{ color: #333333; }}
    [data-testid="stMetricValue"] {{
        color: #1A1A1A;
        font-weight: 800;
    }}

    /* Cartoes dos graficos */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #FFFFFF;
        border: none;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }}
    .titulo-card {{
        font-size: 14px;
        color: #222222;
        border-bottom: 1px solid #CCCCCC;
        padding-bottom: 8px;
        margin-bottom: 8px;
    }}
</style>
""", unsafe_allow_html=True)



# 3. LEITURA DA BASE DE DADOS


@st.cache_data
def carregar_dados():
    dados = pd.read_csv(
        "Analise_Internacoes_SUS_Simulacao.csv",
        sep=";",
        encoding="latin1"
    )
    dados.columns = dados.columns.str.strip()

    dados["data_internacao"] = pd.to_datetime(
        dados["data_internacao"], errors="coerce"
    )

    dados["custo_total"] = (
        dados["custo_total"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    dados["custo_total"] = pd.to_numeric(dados["custo_total"], errors="coerce")
    dados["dias_permanencia"] = pd.to_numeric(
        dados["dias_permanencia"], errors="coerce"
    )
    return dados


dados = carregar_dados()

# Coluna com o codigo da internacao (INT001, INT002...).
# Ajuste o nome abaixo se a sua coluna for diferente.
COL_ID = "id_internacao" if "id_internacao" in dados.columns else dados.columns[0]


def formatar_reais(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X").replace(".", ",").replace("X", ".")
    )


EIXO_REAIS = alt.Axis(
    labelExpr="'R$ ' + format(datum.value, ',.0f')",
    gridColor="#EEEEEE",
    domain=False,
    title=None,
)


def card(titulo):
    """Abre um cartao branco com titulo."""
    c = st.container(border=True)
    c.markdown(f'<div class="titulo-card">{titulo}</div>', unsafe_allow_html=True)
    return c


# 4. CABECALHO + FILTRO DE PERIODO


data_min = dados["data_internacao"].min().date()
data_max = dados["data_internacao"].max().date()

with st.container(key="cabecalho"):
    st.markdown(
        '<p class="titulo">SUS Data Insights: Análise Inteligente '
        'de Internações Hospitalares</p>',
        unsafe_allow_html=True,
    )
    c0, c1, c2, _ = st.columns([0.7, 1.5, 1.5, 8])
    c0.markdown('<div class="rotulo-periodo">Período:</div>',
                unsafe_allow_html=True)
    inicio = c1.date_input("De", value=data_min, min_value=data_min,
                           max_value=data_max, format="DD/MM/YYYY")
    fim = c2.date_input("Até", value=data_max, min_value=data_min,
                        max_value=data_max, format="DD/MM/YYYY")



# 5. FILTROS LATERAIS (opcionais)


st.sidebar.title("Filtros de análise")

regioes = sorted(dados["regiao"].dropna().unique())
sexos = sorted(dados["sexo"].dropna().unique())
faixas = sorted(dados["faixa_etaria"].dropna().unique())

regiao_sel = st.sidebar.multiselect("Região:", regioes, default=regioes)
sexo_sel = st.sidebar.multiselect("Sexo:", sexos, default=sexos)
faixa_sel = st.sidebar.multiselect("Faixa etária:", faixas, default=faixas)

filtrados = dados[
    dados["regiao"].isin(regiao_sel)
    & dados["sexo"].isin(sexo_sel)
    & dados["faixa_etaria"].isin(faixa_sel)
    & (dados["data_internacao"].dt.date >= inicio)
    & (dados["data_internacao"].dt.date <= fim)
].copy()



# 6. KPIs


if filtrados.empty:
    st.warning("Nenhum registro encontrado. Altere os filtros.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)

k1.metric("Custo Total do SUS", formatar_reais(filtrados["custo_total"].sum()))
k2.metric("Média de Dias de Internação",
          f"{filtrados['dias_permanencia'].mean():.2f}".replace(".", ","))
k3.metric("Causa mais comum de Internação",
          filtrados["causa_internacao"].mode().iloc[0])
k4.metric("Total de Internações", f"{len(filtrados)}")

st.write("")



# 7. LINHA 1: DISTRIBUICAO + SAZONALIDADE

g1, g2 = st.columns([1, 1.15])

# --- Distribuicao (custo por faixa etaria) ---
with g1:
    with card("Distribuição regional"):
        df = (filtrados.groupby("faixa_etaria", as_index=False)["custo_total"]
              .sum().sort_values("custo_total", ascending=False))
        graf = (
            alt.Chart(df)
            .mark_bar(color=ROXO, cornerRadiusTopLeft=10, cornerRadiusTopRight=10)
            .encode(
                x=alt.X("faixa_etaria:N", sort=None, title=None,
                        axis=alt.Axis(labelAngle=0)),
                y=alt.Y("custo_total:Q", axis=EIXO_REAIS),
                tooltip=["faixa_etaria",
                         alt.Tooltip("custo_total:Q", format=",.2f")],
            )
            .properties(height=300)
        )
        st.altair_chart(graf, use_container_width=True)

# --- Sazonalidade ---
with g2:
    with card("Sazonalidade e Variações Temporais"):
        df = (filtrados.dropna(subset=["data_internacao"])
              .groupby("data_internacao", as_index=False)["custo_total"].sum())
        graf = (
            alt.Chart(df)
            .mark_line(color=ROXO_ESCURO, point=alt.OverlayMarkDef(
                color=ROXO_ESCURO, size=25))
            .encode(
                x=alt.X("data_internacao:T", title=None,
                        axis=alt.Axis(format="%b %d", grid=False)),
                y=alt.Y("custo_total:Q", axis=EIXO_REAIS),
                tooltip=[alt.Tooltip("data_internacao:T", format="%d/%m/%Y"),
                         alt.Tooltip("custo_total:Q", format=",.2f")],
            )
            .properties(height=300)
        )
        st.altair_chart(graf, use_container_width=True)


# 8. LINHA 2: CAUSAS + ROSCA DE CUSTOS


g3, g4 = st.columns([1.5, 1])

# --- Causas de internacao (barras horizontais) ---
with g3:
    with card("Causas de Internação"):
        df = (filtrados["causa_internacao"].value_counts()
              .rename_axis("causa").reset_index(name="qtd"))
        graf = (
            alt.Chart(df)
            .mark_bar(color=ROXO, cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
            .encode(
                y=alt.Y("causa:N", sort="-x", title=None,
                        axis=alt.Axis(labelLimit=200)),
                x=alt.X("qtd:Q", title=None,
                        axis=alt.Axis(tickMinStep=1, gridColor="#EEEEEE")),
                tooltip=["causa", "qtd"],
            )
            .properties(height=300)
        )
        st.altair_chart(graf, use_container_width=True)

# --- Rosca: custo por internacao ---
with g4:
    with card("Distribuição de Custos por Internação"):
        df = filtrados[[COL_ID, "custo_total"]].dropna().copy()
        df["pct"] = df["custo_total"] / df["custo_total"].sum()
        df["rotulo"] = df[COL_ID].astype(str) + "\n" + (
            (df["pct"] * 100).round(1).astype(str) + "%")

        base = alt.Chart(df).encode(
            theta=alt.Theta("custo_total:Q", stack=True),
            order=alt.Order(f"{COL_ID}:N"),
        )
        rosca = base.mark_arc(innerRadius=45, outerRadius=100).encode(
            color=alt.Color(f"{COL_ID}:N", legend=None,
                            scale=alt.Scale(scheme="purples")),
            tooltip=[COL_ID, alt.Tooltip("custo_total:Q", format=",.2f"),
                     alt.Tooltip("pct:Q", format=".1%")],
        )
        texto = base.mark_text(radius=125, fontSize=10, color="#555555").encode(
            text="rotulo:N"
        )
        st.altair_chart((rosca + texto).properties(height=300),
                        use_container_width=True)


# 9. TABELA E DOWNLOAD


with st.expander("Ver base de dados"):
    st.dataframe(filtrados, use_container_width=True, hide_index=True,
                 height=300)
    csv = filtrados.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
    st.download_button("📥 Baixar dados filtrados", csv,
                       "internacoes_sus_filtradas.csv", "text/csv")

st.caption("Projeto Integrador | Análise e Desenvolvimento de Sistemas | "
           "Senac EAD | Base de dados simulada para fins acadêmicos.")

# 12. RODAPE

st.divider()

st.caption(
    "Projeto Integrador | Análise e Desenvolvimento de Sistemas | "
    "Senac EAD | Base de dados simulada para fins acadêmicos."
)

