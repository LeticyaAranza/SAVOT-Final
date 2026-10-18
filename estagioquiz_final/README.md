# SAVOT — Mostra de Cursos CEFET-MG Varginha

Projeto Django com páginas de Informática, Edificações e Mecatrônica e seus quizzes.

## Assistente virtual

A implementação anterior do chatbot/RAG foi retirada. A página inicial mantém apenas um espaço visual reservado, sem JavaScript, API ou processamento de mensagens. O CSS desse espaço permanece para preservar o layout.

## Execução local

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Google Analytics

O GA4 permanece configurável pela variável `GA_MEASUREMENT_ID`, com eventos dos quizzes `quiz_iniciado` e `quiz_finalizado` e parâmetros `curso` e `resultado`.

## Render

Build: `./build.sh`

Start: `gunicorn projeto.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 --access-logfile - --error-logfile -`

Variáveis: `SECRET_KEY`, `GA_MEASUREMENT_ID` e `DEBUG` (conforme necessário). Não são necessárias chaves de IA.
