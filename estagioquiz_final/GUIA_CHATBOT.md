# Chatbot SAVOT — configuração

## Variáveis

- `TAVILY_API_KEY`: chave da pesquisa Tavily.
- `GEMINI_API_KEY`: chave da API Gemini obtida no Google AI Studio (confira se o modelo e a franquia gratuita estão disponíveis para sua conta).
- `GEMINI_MODEL`: padrão `gemini-2.5-flash`; ajuste conforme disponibilidade atual.
- `CHATBOT_LIMITE_DIARIO`: máximo de requisições globais em 24 horas por instância, padrão 100.

No Render: serviço > Environment, adicione as duas chaves. Nunca faça commit de `.env`.

## Fluxo

Interface na página inicial -> POST `/api/chatbot/conversar/` -> Tavily (busca oficial, opcional geral) -> Gemini -> resposta com fontes.

## Proteção de créditos

Limites por IP: 2/minuto, 8/24h; global: 100/24h (configurável). São limites **em memória** do processo: reiniciam no deploy, não são compartilhados entre instâncias e NÃO constituem teto de cobrança. Cada mensagem pode gerar até duas pesquisas Tavily e uma chamada Gemini. Para limites rígidos em produção, usar contador persistente/compartilhado, limite do provedor, autenticação e/ou CAPTCHA.

## Testes

Sem chaves, a rota retorna 503 sem pesquisar. Testes automatizados simulados não consomem créditos. Com chaves, cada mensagem pode consumir créditos: valide primeiro em ambiente controlado.

## Atenção

O fallback geral ocorre somente se não houver resultados oficiais; relevância, datas e retificações ainda dependem de revisão. Fontes listadas são resultados de pesquisa, não garantia de suporte literal para cada frase. Hospedagem gratuita e quotas variam por fornecedor.


## Respostas diretas e links internos

Perguntas gerais sobre cursos são respondidas diretamente com informações das páginas do SAVOT, sem chamadas a Tavily/Gemini. Os links de Informática, Edificações e Mecatrônica aparecem abaixo da resposta. Perguntas sobre datas, editais, vagas e inscrições usam pesquisa atualizada e Gemini. A IA foi orientada a responder primeiro e depois indicar as fontes.

**Importante:** não houve testes com APIs reais; as respostas sobre processos seletivos dependem da qualidade e atualidade das fontes recuperadas. As informações das páginas internas são descritivas, não substituem os editais.
