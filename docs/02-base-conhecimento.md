# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Organize a base de conhecimento do agente "Lupa" usando os 4 arquivos da pasta `data/`. Explique como cada arquivo ajuda na investigação financeira e monte um exemplo de contexto formatado que será enviado pro LLM. O foco é análise de dados e detecção de padrões.

## Dados Utilizados

O Lupa utiliza dados mockados (fictícios) armazenados localmente na pasta `data/` para garantir privacidade e rapidez na execução.

| Arquivo | Formato | Função na Investigação (Lupa) |
|---------|---------|-------------------------------|
| `transacoes.csv` | CSV | **A Lupa do Detetive.** É a fonte primária. Contém o "rastro" do dinheiro. O Lupa varre este arquivo buscando gastos excessivos, duplicados ou categorias que estouraram o orçamento. |
| `perfil_investidor.json` | JSON | **O Dossiê do Cliente.** Define quem é o suspeito (o usuário). Se o perfil diz que ele ganha R$ 5.000 e quer economizar, mas o CSV mostra R$ 6.000 de gastos, temos um caso! |
| `historico_atendimento.csv` | CSV | **O Arquivo Morto.** Mostra o que o cliente já perguntou antes, para o Lupa não investigar o mesmo caso duas vezes ou retomar conversas antigas. |
| `produtos_financeiros.json` | JSON | **Soluções.** Se o Lupa encontrar "dinheiro sobrando" (o que é raro), ele consulta essa lista para sugerir onde guardar, em vez de deixar parado na conta. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Mantivemos a estrutura original dos arquivos fornecidos pela DIO para garantir compatibilidade, mas **ajustamos o foco da interpretação**:
- O arquivo `transacoes.csv` é tratado não apenas como uma lista, mas como um dataset analítico onde calculamos **totais por categoria** antes de passar para o LLM.
- O produto **Fundo Imobiliário (FII)** foi priorizado nas explicações para perfis moderados que buscam renda passiva, substituindo recomendações genéricas de "multimercado".

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Utilizamos Python (Pandas) para carregar e pré-processar os dados. Não passamos o CSV bruto diretamente para o LLM para economizar tokens e evitar confusão. O Python faz a "pré-mastigação" dos dados.

```python
import pandas as pd
import json

# Carregamento da "Cena do Crime" (Dados)
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# Exemplo de Pré-processamento do Lupa
total_gastos = transacoes['valor'].sum()
gastos_por_categoria = transacoes.groupby('categoria')['valor'].sum()
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Adotamos a estratégia de **Injeção de Contexto Estruturada**. O Python gera um resumo textual (string) e injetamos isso no `system prompt` logo antes da pergunta do usuário.

**Exemplo de Prompt Montado (O que o LLM realmente vê):**

```text
SYSTEM: Você é o Lupa, um detetive financeiro. Use APENAS os dados abaixo para responder.

--- DOSSIÊ DO CLIENTE (Resumo) ---
Nome: João Silva | Perfil: Moderado
Meta Principal: Reserva de Emergência (Faltam R$ 5.000)

--- ANÁLISE DE GASTOS (Outubro) ---
🚨 ALERTA: Total de Saídas (R$ 2.488,90) consome 50% da Renda.
- Moradia: R$ 1.380 (Normal)
- Alimentação: R$ 570 (Atenção: inclui muitos restaurantes)
- Transporte: R$ 295
- Lazer: R$ 55,90

--- PRODUTOS DISPONÍVEIS (Caso sobre dinheiro) ---
1. Tesouro Selic (Segurança)
2. CDB Liquidez Diária
3. Fundo Imobiliário (Renda Mensal)

PERGUNTA DO USUÁRIO: "Para onde meu dinheiro foi esse mês?"
```

Dessa forma, o Lupa recebe a análise já "mastigada" e foca em **explicar e alertar** com sua personalidade detetivesca, em vez de tentar fazer contas de cabeça.
