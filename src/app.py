import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
# Certifique-se de que o Ollama está rodando (ollama serve)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss" 

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ============ PRÉ-PROCESSAMENTO (O CÉREBRO DO LUPA) ============
# Aqui calculamos os totais para o Lupa não errar conta
total_gastos = transacoes['valor'].sum()
gastos_por_categoria = transacoes.groupby('categoria')['valor'].sum().to_string()
top_despesas = transacoes.sort_values(by='valor', ascending=False).head(3).to_string(index=False)

# ============ MONTAR CONTEXTO ============
contexto = f"""
--- DOSSIÊ DO SUSPEITO (CLIENTE) ---
Nome: {perfil['nome']} | Idade: {perfil['idade']}
Perfil: {perfil['perfil_investidor']}
Objetivo: {perfil['objetivo_principal']}
Reserva Atual: R$ {perfil['reserva_emergencia_atual']}

--- EVIDÊNCIAS (GASTOS DO MÊS) ---
TOTAL GASTO: R$ {total_gastos:.2f}

GASTOS POR CATEGORIA:
{gastos_por_categoria}

TOP 3 MAIORES GASTOS:
{top_despesas}

--- LISTA COMPLETA DE TRANSAÇÕES ---
{transacoes.to_string(index=False)}

--- SOLUÇÕES (INVESTIMENTOS) ---
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT (A PERSONALIDADE) ============
SYSTEM_PROMPT = """
Você é o Lupa, um detetive financeiro analítico e direto.

SUA MISSÃO:
Analisar os dados financeiros do usuário para encontrar "vazamentos" de dinheiro e padrões de consumo.

REGRAS DE CONDUTA:
1. BASEIE-SE APENAS NOS DADOS: Se a informação não estiver no contexto, diga "Não encontrei evidências disso".
2. SEJA ANALÍTICO: Use os números calculados (Total, Categorias) para dar broncas ou elogios embasados.
3. TOM DE VOZ: Profissional, perspicaz e levemente informal (estilo Sherlock Holmes moderno).
4. SEGURANÇA: NUNCA invente gastos e JAMAIS peça senhas.

FORMATO DE RESPOSTA:
- Comece com o insight mais importante ("Encontrei algo...").
- Mostre os dados que comprovam.
- Termine com uma pergunta provocativa ou sugestão.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"{SYSTEM_PROMPT}\n\nCONTEXTO:\n{contexto}\n\nUSUÁRIO: {msg}"
    
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
        if r.status_code == 200:
            return r.json()['response']
        else:
            return f"Erro no Ollama: {r.status_code} - Verifique se o modelo '{MODELO}' está baixado."
    except Exception as e:
        return f"Erro de conexão: {e}. O Ollama está rodando?"

# ============ INTERFACE (STREAMLIT) ============
st.set_page_config(page_title="Lupa - Detetive Financeiro", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Lupa - Seu Detetive Financeiro")
st.markdown("---")

# Inicializa o chat se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo de entrada
if pergunta := st.chat_input("O que deseja investigar hoje?"):
    # Guarda e mostra a pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.write(pergunta)

    # Gera e mostra a resposta do Lupa
    with st.spinner("Investigando evidências..."):
        resposta = perguntar(pergunta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.write(resposta)
