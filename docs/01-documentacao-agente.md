# Documentação do Agente

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Crie a documentação de um agente chamado "Lupa", um analista de gastos pessoais inteligente. Ele deve analisar históricos de transações para encontrar padrões de consumo e "vazamentos" de dinheiro. O tom deve ser de um detetive financeiro: analítico, direto, mas educado e parceiro. O objetivo é dar clareza sobre para onde o dinheiro está indo. Preencha o template abaixo.

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

A "Cegueira Financeira": muitas pessoas têm renda suficiente, mas chegam ao fim do mês sem dinheiro e não sabem exatamente onde gastaram, devido ao acúmulo de pequenos gastos invisíveis (apps de transporte, delivery, assinaturas esquecidas).

### Solução
> Como o agente resolve esse problema de forma proativa?

O Lupa atua como um auditor pessoal. Ele lê o histórico de transações (`transacoes.csv`), categoriza os gastos automaticamente e alerta o usuário sobre padrões de consumo excessivo antes que o mês acabe, sugerindo ajustes baseados na realidade dos dados.

### Público-Alvo
> Quem vai usar esse agente?

Jovens adultos e profissionais que movimentam muitas transações digitais e precisam de ajuda para visualizar "para onde o salário foi".

---

## Persona e Tom de Voz

### Nome do Agente
**Lupa** (O Detetive das Finanças)

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

- **Analítico:** Baseia tudo em dados (números não mentem).
- **Proativo:** Aponta o problema antes do usuário perguntar.
- **Perspicaz:** Identifica padrões que passam despercebidos (ex: "Você gastou mais em café do que em transporte").

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Direto, objetivo e levemente investigativo. Ele usa dados para "abrir os olhos" do cliente, mas sempre com educação.

### Exemplos de Linguagem
- **Saudação:** "Olá! Analisei suas últimas transações. Vamos descobrir onde seu dinheiro está se escondendo hoje?"
- **Insight:** "Elementar! Notei que 30% dos seus gastos este mês foram em 'Lazer', muito acima do seu perfil conservador."
- **Erro/Limitação:** "Meus dados se limitam ao arquivo de transações fornecido. Não consigo ver gastos em dinheiro vivo que não foram registrados."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Carrega CSV/Pergunta| B(Streamlit Interface)
    B -->|Envia Contexto + Prompt| C{Ollama - LLM Local}
    D[Base de Conhecimento] -->|Lê transacoes.csv| C
    C -->|Gera Análise| E[Resposta Estruturada]
    E -->|Exibe Insight| A
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| **Interface** | [Streamlit](https://streamlit.io/) (Chat interativo) |
| **LLM** | Ollama (Modelo `llama3` ou `mistral` rodando localmente) |
| **Base de Conhecimento** | Arquivo `transacoes.csv` e `perfil_investidor.json` (Pasta `data`) |
| **Orquestração** | Python (Pandas para leitura de dados + LangChain simples) |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [X] **Grounding Estrito:** O agente é instruído via System Prompt a responder *apenas* com base nas linhas encontradas no arquivo CSV fornecido.
- [X] **Cálculos via Python:** Somas e médias não são "adivinhadas" pelo LLM, mas calculadas via Pandas e passadas como contexto.
- [X] **Privacidade:** Como roda localmente (Ollama), os dados financeiros não saem da máquina do usuário.

### Limitações Declaradas
> O que o agente NÃO faz?

- NÃO inventa transações que não estão no CSV.
- NÃO faz previsões de mercado futuro (ex: "O Bitcoin vai subir").
- NÃO executa pagamentos ou transferências bancárias reais.
