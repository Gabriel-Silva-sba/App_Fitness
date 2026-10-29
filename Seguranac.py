import folium
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

# 1. Configuração da Página do Streamlit
st.set_page_config(
    page_title="Monitor de Segurança Pública - Ribeirão Preto",
    layout="wide",
)

st.title("🚨 Monitor de Segurança Pública - Ribeirão Preto")
st.markdown(
    "Painel de controle em tempo real para monitoramento de ocorrências nas últimas 24 horas por região/bairro."
)

# 2. Base de dados simulada com as regiões e cores fixas
@st.cache_data
def carregar_dados():
    dados = {
        "Regiao": [
            "Centro",
            "Zona Sul (Jardim Botânico / Ribeirânia)",
            "Zona Norte (Ipiranga / Campos Elíseos)",
            "Zona Leste (Jardim Irajá / Santa Cruz)",
            "Zona Oeste (Sumarezinho / Simioni)",
            "Zona Oeste (Vila Tibério)",
        ],
        "Lat": [-21.1775, -21.1950, -21.1550, -21.1800, -21.1650, -21.1700],
        "Lon": [-47.8103, -47.8000, -47.8200, -47.7850, -47.8400, -47.8250],
    }
    df = pd.DataFrame(dados)

    np.random.seed(42)
    df["Ocorrencias_24h"] = np.random.randint(0, 25, size=len(df))

    def definir_status_cor(regiao):
        if "Zona Norte" in regiao:
            return "Alto (Vermelho)", "red"
        elif "Centro" in regiao:
            return "Médio (Amarelo)", "orange"
        elif "Zona Sul" in regiao:
            return "Baixo / Zero (Verde)", "green"
        else:
            return "Baixo / Zero (Verde)", "green"

    status_cor = df["Regiao"].apply(definir_status_cor)
    df["Status"] = [item[0] for item in status_cor]
    df["Cor"] = [item[1] for item in status_cor]
    
    return df

df_regioes = carregar_dados()

# 2.1 Dados temporais (Ocorrências por Hora)
@st.cache_data
def carregar_dados_temporais():
    horas = [f"{h:02d}:00" for h in range(24)]
    np.random.seed(100)
    ocorrencias_hora = np.random.randint(1, 15, size=24)
    df_tempo = pd.DataFrame({"Hora": horas, "Ocorrencias": ocorrencias_hora})
    return df_tempo

df_tempo = carregar_dados_temporais()

# 2.2 Dados de Tipos de Ocorrência (Com a substituição realizada)
@st.cache_data
def carregar_tipos_ocorrencia():
    tipos = [
        "Furto Simples", 
        "Homicídio / Lesão Corporal", # Substituído aqui
        "Roubo a Mão Armada", 
        "Furto de Veículo", 
        "Vandalismo / Dano",
        "Tráfico de Drogas"
    ]
    np.random.seed(200)
    quantidades = np.random.randint(5, 35, size=len(tipos))
    df_tipos = pd.DataFrame({"Tipo_Ocorrencia": tipos, "Total": quantidades})
    return df_tipos

df_tipos = carregar_tipos_ocorrencia()

# 3. Sidebar com Filtros e Métricas Rápidas
st.sidebar.header("Painel de Controle")

filtro_status = st.sidebar.multiselect(
    "Filtrar por Nível de Alerta:",
    options=["Alto (Vermelho)", "Médio (Amarelo)", "Baixo / Zero (Verde)"],
    default=["Alto (Vermelho)", "Médio (Amarelo)", "Baixo / Zero (Verde)"],
)

df_filtrado = df_regioes[df_regioes["Status"].isin(filtro_status)]

# Métricas no topo
col1, col2, col3 = st.columns(3)
col1.metric("Total de Ocorrências (24h)", int(df_regioes["Ocorrencias_24h"].sum()))
col2.metric(
    "Áreas em Alerta Vermelho",
    int((df_regioes["Status"] == "Alto (Vermelho)").sum()),
)
col3.metric(
    "Áreas Estáveis (Verde)",
    int((df_regioes["Status"] == "Baixo / Zero (Verde)").sum()),
)

st.markdown("---")

# 4. Construção do Mapa Interativo com Folium
st.subheader("📍 Mapa de Calor / Status por Região em Ribeirão Preto")

mapa_rp = folium.Map(location=[-21.1775, -47.8103], zoom_start=13)

for _, row in df_filtrado.iterrows():
    folium.CircleMarker(
        location=[row["Lat"], row["Lon"]],
        radius=12 + (row["Ocorrencias_24h"] * 0.4),
        color=row["Cor"],
        fill=True,
        fill_color=row["Cor"],
        fill_opacity=0.7,
        popup=f"<b>Região:</b> {row['Regiao']}<br><b>Ocorrências (24h):</b> {row['Ocorrencias_24h']}<br><b>Status:</b> {row['Status']}",
    ).add_to(mapa_rp)

st_data = st_folium(mapa_rp, width=1200, height=450)

st.markdown("---")

# 5. Seção de Gráficos Analíticos
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📊 Ocorrências por Região")
    if not df_filtrado.empty:
        fig_bar = px.bar(
            df_filtrado, 
            x="Regiao", 
            y="Ocorrencias_24h", 
            color="Status",
            color_discrete_map={"Alto (Vermelho)": "red", "Médio (Amarelo)": "orange", "Baixo / Zero (Verde)": "green"},
            labels={"Regiao": "Região", "Ocorrencias_24h": "Ocorrências (24h)"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Sem dados para exibir no gráfico.")

with col_g2:
    st.subheader("📈 Linha do Tempo (Ocorrências por Hora)")
    fig_line = px.line(
        df_tempo, 
        x="Hora", 
        y="Ocorrencias", 
        markers=True,
        labels={"Hora": "Horário do Dia", "Ocorrencias": "Volume de Ocorrências"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Gráfico de Tipos de Ocorrência atualizado
st.subheader("🔍 Distribuição por Tipo de Ocorrência (Natureza do Delito)")
fig_tipo = px.bar(
    df_tipos, 
    x="Tipo_Ocorrencia", 
    y="Total", 
    color="Tipo_Ocorrencia",
    labels={"Tipo_Ocorrencia": "Tipo de Ocorrência", "Total": "Quantidade Registrada"}
)
st.plotly_chart(fig_tipo, use_container_width=True)

st.markdown("---")

# 6. Tabela de Dados Detalhada
st.subheader("📋 Detalhamento por Região")

df_tabela = df_filtrado[["Regiao", "Ocorrencias_24h", "Status"]].rename(
    columns={
        "Regiao": "Região / Bairro",
        "Ocorrencias_24h": "Ocorrências (24h)",
        "Status": "Nível de Alerta"
    }
).reset_index(drop=True)

st.dataframe(df_tabela, use_container_width=True)