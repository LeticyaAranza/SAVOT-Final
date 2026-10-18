# Correções do chatbot SAVOT

- Consultas sobre outros campi (como Leopoldina) agora seguem para Tavily/Gemini, em vez de usar a resposta fixa de Varginha.
- Perguntas gerais sobre o CEFET também consultam fontes externas; respostas locais são reservadas para perguntas explícitas sobre SAVOT/Varginha.
- O filtro aceita nomes de outros campi, mantendo bloqueio de perguntas não relacionadas.
- Erros de API retornam categorias mais informativas; o traceback completo permanece no terminal do Django.
- Continuações curtas de conversa levam a pergunta anterior como contexto da busca.

## Como testar

Na pasta de manage.py, configure `.env` com `TAVILY_API_KEY`, `GEMINI_API_KEY`, `GEMINI_MODEL` e `DEBUG=True` somente localmente. Reinicie `python manage.py runserver`. Teste primeiro uma pergunta local sobre o SAVOT; depois teste uma única pergunta sobre Leopoldina e uma sobre data de prova. Estas últimas gastam créditos.

**Importante:** este pacote não foi testado contra APIs reais. Se uma chamada falhar, veja o erro no terminal. Nunca publique chaves ou `.env`.
