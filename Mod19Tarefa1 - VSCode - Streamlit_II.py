import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Configuração inicial do Streamlit
st.title("Análise do Campeonato Brasileiro 2023 🏆⚽")

# Função para carregar e processar o CSV
@st.cache_data
def carregar_processar_csv(uploaded_file):
    # Lendo o arquivo CSV
    df = pd.read_csv(uploaded_file)

    # Verificar se há valores nulos antes da limpeza
    if df.isnull().sum().sum() > 0:
        st.warning("⚠️ O dataset contém valores nulos! Eles serão removidos automaticamente.")
        df = df.dropna()  # Remove linhas com valores nulos

    # Convertendo data para datetime
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')

    # Filtrando apenas os jogos de 2023
    br_23 = df[df['data'].dt.year == 2023].copy()

    # Removendo a coluna ID, se existir
    if 'ID' in br_23.columns:
        br_23.drop(columns=['ID'], inplace=True)

    # Convertendo a coluna 'hora' para formato de hora
    br_23['hora'] = pd.to_datetime(br_23['hora'], format='%H:%M').dt.time

    # Definir categorias de horário
    limites = [
        ('09:00', '13:00', 'Manhã'),
        ('13:01', '17:59', 'Tarde'),
        ('18:00', '22:35', 'Noite'),
    ]

    # Criar lista de condições e valores
    condicoes = []
    valores = []

    for inicio, fim, categoria in limites:
        inicio_time = datetime.strptime(inicio, '%H:%M').time()
        fim_time = datetime.strptime(fim, '%H:%M').time()
        condicoes.append((br_23['hora'] >= inicio_time) & (br_23['hora'] <= fim_time))
        valores.append(categoria)

    # Aplicar categorização
    br_23['categoria_hora'] = np.select(condicoes, valores, default=-1)

    # Remover as linhas onde 'vencedor' é '-'
    br_23 = br_23[br_23['vencedor'] != '-']

    return br_23

# Sidebar para configurar os parâmetros
st.sidebar.title("Configurações de Análise")
uploaded_file = st.sidebar.file_uploader("Faça o upload do arquivo CSV", type=["csv"])

# Se o arquivo for carregado e o botão "Aplicar" for pressionado
if uploaded_file is not None:
    # Seletor para escolher a categoria de horário
    categoria_selecionada = st.sidebar.selectbox("Selecione uma categoria de horário para ver os maiores vencedores:", ['Manhã', 'Tarde', 'Noite'])

    # Botão "Aplicar" para carregar e processar os dados
    if st.sidebar.button("Aplicar"):
        # Carregar e processar o CSV
        br_23 = carregar_processar_csv(uploaded_file)

        # Mostrar os dados processados
        st.write("📊 **Dados Processados:**")
        st.dataframe(br_23.head(10))

        # Contar a frequência de cada categoria
        categoria_counts = br_23['categoria_hora'].value_counts().sort_index()

        # Criar gráfico de barras
        st.write("📊 **Distribuição dos Jogos por Horário**")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=categoria_counts.index, y=categoria_counts.values, hue=categoria_counts.index, palette='Blues', legend=False, ax=ax)
        ax.set_xlabel("Categoria Hora")
        ax.set_ylabel("Frequência")
        ax.set_title("Distribuição de Categoria Hora")
        st.pyplot(fig)

        # Filtrar pelo horário escolhido
        br_filtrado = br_23[br_23['categoria_hora'] == categoria_selecionada]

        # Obter os top 5 vencedores
        top_5_vencedores = br_filtrado['vencedor'].value_counts().head(5)

        # Exibir os vencedores
        st.write(f"🏆 **Top 5 vencedores na categoria {categoria_selecionada}**")
        st.dataframe(top_5_vencedores)

        # Exibir gráfico dos vencedores
        st.write("📊 **Gráfico dos Top 5 Vencedores**")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=top_5_vencedores.index, y=top_5_vencedores.values, palette='viridis', ax=ax)
        ax.set_xlabel("Clube")
        ax.set_ylabel("Número de Vitórias")
        ax.set_title(f"Top 5 Vencedores na Categoria {categoria_selecionada}")
        st.pyplot(fig)

else:
    st.sidebar.warning("🚨 Faça o upload de um arquivo CSV para continuar.")




