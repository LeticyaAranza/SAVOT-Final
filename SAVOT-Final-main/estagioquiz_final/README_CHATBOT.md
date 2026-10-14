# Chatbot corrigido

Use Python 3.12 ou superior. Na pasta do manage.py:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py runserver
```

Preencha GROQ_API_KEY no .env. No Render, configure a variável no painel.
A chave da Groq continua necessária para gerar respostas. A consulta aos sites oficiais não requer outra chave.

A base ignora LEIA-ME e exemplo_*, mantém perguntas e respostas juntas, remove palavras comuns da busca e detecta alterações nos documentos automaticamente.
A consulta web pesquisa publicações no site do campus e consulta a página da Copeve para o ingresso técnico do próximo ano quando a pergunta trata de seleção. Não é uma busca de toda a internet: não garante encontrar PDFs, páginas de cursos, graduação ou qualquer edital de outros anos. As fontes efetivamente consultadas aparecem na resposta. Cache de cinco minutos. Se houver falha, usa os documentos e avisa; não inventa uma consulta bem-sucedida.

Para desativar a consulta, defina CHATBOT_CONSULTA_WEB=false.
Os textos locais continuam sendo resumos: revise-os contra os editais oficiais e suas retificações.
