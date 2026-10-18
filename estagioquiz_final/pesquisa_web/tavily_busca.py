"""Busca fontes oficiais e, quando solicitado, resultados complementares.
Nenhuma chamada à API ocorre na importação deste módulo.
"""
import os
from urllib.parse import urlparse

DOMINIOS_OFICIAIS = ("cefetmg.br",)


def e_oficial(url):
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    return any(host == dominio or host.endswith("." + dominio)
               for dominio in DOMINIOS_OFICIAIS)


def pesquisar(pergunta, incluir_internet_geral=False, max_resultados=5):
    """Retorna resultados brutos. Cada chamada de busca consome créditos Tavily.

    Não avalia confiabilidade ou atualidade dos trechos; não gera resposta por IA.
    A busca geral só é executada quando explicitamente solicitada e quando
    a busca oficial não encontrou resultados.
    """
    pergunta = pergunta.strip()
    if not pergunta or len(pergunta) > 500:
        raise ValueError("A pergunta deve ter entre 1 e 500 caracteres.")
    chave = os.getenv("TAVILY_API_KEY", "").strip()
    if not chave:
        raise RuntimeError("TAVILY_API_KEY não configurada.")
    from tavily import TavilyClient
    cliente = TavilyClient(api_key=chave)
    limite = max(1, min(int(max_resultados), 5))
    consulta = f"{pergunta} CEFET-MG"
    dados = cliente.search(query=consulta, search_depth="basic",
                          max_results=limite, include_domains=list(DOMINIOS_OFICIAIS))
    resultados = _normalizar(dados.get("results", []), somente_oficiais=True)
    if not resultados and incluir_internet_geral:
        dados = cliente.search(query=consulta, search_depth="basic", max_results=limite)
        resultados = _normalizar(dados.get("results", []), somente_oficiais=False)
    return resultados


def _normalizar(itens, somente_oficiais):
    saida = []
    for item in itens:
        url = item.get("url", "")
        if not url.startswith("https://"):
            continue
        oficial = e_oficial(url)
        if somente_oficiais and not oficial:
            continue
        saida.append({"titulo": item.get("title", ""), "url": url,
                      "trecho": item.get("content", ""), "oficial": oficial})
    return saida
