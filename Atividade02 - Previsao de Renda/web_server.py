import streamlit as st
import pickle  # Para carregar o modelo treinado
import pandas as pd

# Nome e icon 
st.set_page_config(
    page_title="Previsão de Renda",
    page_icon="💲", 
    layout="wide",  # Alternativas: "centered"
    initial_sidebar_state="expanded"  # Inicializa a sidebar expandida
)

# Carregar modelo salvo
with open("C:/Users/djang/OneDrive/Área de Trabalho/EBAC/Cientista de Dados/Projeto 2/input/regressor_forest.pkl", 'rb') as file:
    modelo = pickle.load(file)

# Título da aplicação
st.title("Previsão de Renda e Decisão de Crédito")

# Criando sidebar para interações com o usuario:
a = st.sidebar 

#estilo geral sidebar (CSS) 
st.markdown("""
    <style>
    /* Estilo geral da sidebar */
    [data-testid="stSidebar"] {
        background-color: #16498C; /* Cor de fundo padrão */
        color: #F2F2F2; /* Cor do texto */
    }

    /* Ajusta a cor do texto e inputs (botões, radio buttons, etc.) */
    [data-testid="stSidebar"] * {
        color: #F2F2F2; /* Cor do texto dos inputs */
        font-size: 18px !important; /* Tamanho da fonte */
    }

    /* Ajusta campos de entrada (exemplo: text_input, selectbox) */
    [data-testid="stSidebar"] input, 
    [data-testid="stSidebar"] select, 
    [data-testid="stSidebar"] textarea {
        background-color: #F2F2F2 !important; /* Fundo dos inputs */
        color: #333333 !important; /* Texto dos inputs */
        border: 1px solid #F2F2F2 !important; /* Borda */
    }

    </style>
""", unsafe_allow_html=True)

# Inputs do usuário
st.sidebar.header("Informações do Cliente")
tempo_emprego = st.sidebar.number_input("Tempo de Emprego (anos)", min_value=0.0, format="%.1f")
posse_de_veiculo = st.sidebar.checkbox("Possui Veículo?")
estado_civil_Casado = st.sidebar.checkbox("Casado?")
qt_pessoas_residencia = st.sidebar.number_input("Quantidade de Pessoas na Residência", min_value=1, step=1)
tipo_renda_Assalariado = st.sidebar.checkbox("Renda: Assalariado")
tipo_renda_Servidor_publico = st.sidebar.checkbox("Renda: Servidor Público")
idade = st.sidebar.number_input("Idade", min_value=18, max_value=100, step=1)
sexo = st.sidebar.selectbox("Sexo", ["Masculino", "Feminino"])
posse_de_imovel = st.sidebar.checkbox("Possui Imóvel?")

# Criar DataFrame com os dados inseridos
dados_cliente = pd.DataFrame({
    'tempo_emprego': [tempo_emprego],
    'posse_de_veiculo': [int(posse_de_veiculo)],
    'estado_civil_Casado': [int(estado_civil_Casado)],
    'qt_pessoas_residencia': [qt_pessoas_residencia],
    'tipo_renda_Assalariado': [int(tipo_renda_Assalariado)],
    'tipo_renda_Servidor_publico': [int(tipo_renda_Servidor_publico)],
    'idade': [idade],
    'sexo': [0 if sexo == "Masculino" else 1],
    'posse_de_imovel': [int(posse_de_imovel)]
})

# ESTILO GERAL DISPLAY

st.markdown("""
    <style>
    /* Fundo do display principal */
    [data-testid="stAppViewContainer"] {
        background-color: #F4F4F4; /* Cor de fundo do display */
        color: #333333; /* Cor do texto principal */
        padding: 10px; /* Espaçamento interno */
    }

    /* Estilo do cabeçalho e subtítulos */
    [data-testid="stAppViewContainer"] h1, 
    [data-testid="stAppViewContainer"] h2, 
    [data-testid="stAppViewContainer"] h3 {
    }

    /* Estilo de widgets (inputs, botões, etc.) no display principal */
    [data-testid="stAppViewContainer"] input, 
    [data-testid="stAppViewContainer"] select, 
    [data-testid="stAppViewContainer"] textarea {
        background-color: #F4F4F4; /* Fundo dos inputs */
        color: #333333; /* Cor do texto */
        border: 2.5px solid #333333; /* Borda */
        border-radius: 10px; /* Borda arredondada */
        padding: 8px; /* Espaçamento interno */
    }

    /* Estilo dos botões */
    [data-testid="stAppViewContainer"] button {
        background-color: #16498C; /* Fundo dos botões */
        color: #F4F4F4; /* Texto dos botões */
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }

    /* Efeito de hover nos botões */
    [data-testid="stAppViewContainer"] button:hover {
        background-color: #037F8C; /* Cor ao passar o mouse */
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Prever renda
if st.sidebar.button("Prever Renda"):
    renda_prevista = modelo.predict(dados_cliente)[0]
    st.write(f"### Renda Prevista: R$ {renda_prevista:.2f}")
    
    # Aplicar motor de decisão
    limite_credito = renda_prevista * 0.3  # Exemplo: 30% da renda prevista
    st.write(f"### Limite de Crédito Sugerido: R$ {limite_credito:.2f}")
    
    # Intervenção humana
    decisao = st.radio("Aprovar Crédito?", ("Aprovar", "Rejeitar"))
    if st.button("Confirmar Decisão"):
        st.write(f"## Decisão Final: {decisao}")
        
        # Exibir histórico das decisões
        st.write("### Histórico de Decisões")
        st.table(dados_cliente.assign(Renda_Prevista=renda_prevista, Limite_Credito=limite_credito, Decisao=decisao))