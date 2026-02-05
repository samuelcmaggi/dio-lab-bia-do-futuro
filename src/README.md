# Passo a Passo de Execução

## Setup do Ollama

```bash
# 1. Instalar Ollama (ollama.com)
# 2. Baixar o modelo Llama 3 (usado no projeto)
ollama pull llama3

# 3. Testar se funciona
ollama run llama3 "Olá, detetive!"
```

## Código Completo

Todo o código-fonte está no arquivo `src/app.py`.

## Como Rodar

```bash
# 1. Instalar dependências
pip install streamlit pandas requests

# 2. Garantir que Ollama está rodando
ollama serve

# 3. Rodar o app
streamlit run src/app.py
```

