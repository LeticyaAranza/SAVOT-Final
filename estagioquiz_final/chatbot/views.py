import json
import logging
import os
import hashlib
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .servico import responder, resposta_local
from .escopo import no_escopo, resposta_fora_escopo

log = logging.getLogger(__name__)


def _incrementar(chave, limite, duracao):
    if cache.add(chave, 1, timeout=duracao):
        return True
    try:
        return cache.incr(chave) <= limite
    except ValueError:
        return cache.add(chave, 1, timeout=duracao)


@require_POST
def conversar(request):
    if len(request.body) > 6000:
        return JsonResponse({"erro": "Mensagem muito grande."}, status=400)
    try:
        dados = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"erro": "JSON inválido."}, status=400)
    if not isinstance(dados, dict):
        return JsonResponse({"erro": "Dados inválidos."}, status=400)
    pergunta = dados.get("mensagem", "")
    historico = dados.get("historico", [])
    if not isinstance(pergunta, str) or not 1 <= len(pergunta.strip()) <= 400:
        return JsonResponse({"erro": "Escreva uma pergunta de até 400 caracteres."}, status=400)
    if not isinstance(historico, list) or len(historico) > 6 or any(
        not isinstance(x, dict) or x.get("papel") not in ("usuario", "assistente")
        or not isinstance(x.get("texto"), str) or len(x["texto"]) > 400 for x in historico
    ):
        return JsonResponse({"erro": "Histórico inválido."}, status=400)
    # Bloqueia assuntos externos ANTES da busca e da IA: zero créditos consumidos.
    if not no_escopo(pergunta.strip(), historico):
        return JsonResponse(resposta_fora_escopo())
    local = resposta_local(pergunta.strip(), historico)
    if local is not None:
        return JsonResponse(local)
    if not os.getenv("TAVILY_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        return JsonResponse({"erro": "Chatbot aguardando configuração das APIs."}, status=503)
    # A chave por IP não usa X-Forwarded-For fornecido pelo visitante.
    ip = request.META.get("REMOTE_ADDR", "desconhecido")
    identificador = hashlib.sha256(ip.encode()).hexdigest()[:20]
    if not _incrementar(f"savot:ip:min:{identificador}", 2, 60):
        return JsonResponse({"erro": "Aguarde um minuto antes de perguntar novamente."}, status=429)
    if not _incrementar(f"savot:ip:dia:{identificador}", 8, 86400):
        return JsonResponse({"erro": "Limite diário de perguntas atingido."}, status=429)
    if not _incrementar("savot:global:dia", int(os.getenv("CHATBOT_LIMITE_DIARIO", "100")), 86400):
        return JsonResponse({"erro": "Limite diário do chatbot atingido. Volte amanhã."}, status=429)
    try:
        return JsonResponse(responder(pergunta.strip(), historico))
    except Exception as exc:
        log.exception("Falha ao responder no chatbot")
        detalhe = str(exc).lower()
        if any(x in detalhe for x in ("429", "quota", "resource_exhausted", "rate limit")):
            mensagem = "A API atingiu um limite de uso. Aguarde ou confira as cotas do Tavily e do Gemini."
        elif any(x in detalhe for x in ("401", "403", "api key", "api_key", "permission_denied", "unauthorized")):
            mensagem = "A consulta foi recusada pela API. Verifique as chaves e permissões no arquivo .env."
        elif any(x in detalhe for x in ("404", "model not found", "not_found")):
            mensagem = "O modelo Gemini configurado pode não estar disponível. Confira GEMINI_MODEL."
        elif any(x in detalhe for x in ("timeout", "timed out", "connection")):
            mensagem = "A consulta demorou demais ou houve falha de conexão. Tente novamente."
        else:
            mensagem = "Falha na consulta externa. Confira o traceback no terminal do Django (não publique suas chaves)."
        return JsonResponse({"erro": mensagem}, status=503)
