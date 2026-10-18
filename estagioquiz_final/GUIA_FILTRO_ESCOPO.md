# Filtro de assuntos do chatbot SAVOT

O filtro está em `chatbot/escopo.py` e é aplicado em `chatbot/views.py` **antes** de Tavily e Gemini. Perguntas fora do escopo recebem uma resposta orientativa sem gastar créditos.

Aceita perguntas explícitas sobre CEFET-MG, SAVOT, cursos técnicos, campus, editais, inscrições, provas, matrículas e áreas correlatas, além de perguntas curtas de continuidade quando o histórico do usuário contém contexto relevante.

Recusa perguntas gerais como cálculos, listas de filmes, receitas, futebol e pedidos de programação sem relação com o CEFET.

**Limitação:** este filtro é determinístico, por palavras-chave e contexto. Pode recusar perguntas legítimas muito vagas e aceitar algumas perguntas não relacionadas que contenham termos permitidos. Para uma moderação semântica mais robusta, poderá ser complementado posteriormente por classificador local sem custo de API, ou por um modelo de classificação com custo. O filtro não substitui os limites de taxa existentes.
