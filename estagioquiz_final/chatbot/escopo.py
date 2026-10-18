"""Filtro de assunto executado antes de qualquer chamada paga de API."""
import re
import unicodedata

RECUSA = ("Sou o assistente do SAVOT e respondo apenas dúvidas relacionadas ao "
          "CEFET-MG, seus cursos técnicos, o Campus Varginha e processos seletivos. "
          "Posso ajudar com cursos, inscrições, editais, provas e matrículas.")

TERMOS = (
    "cefet", "savot", "copeve", "varginha", "leopoldina", "araxa",
    "contagem", "curvelo", "divinopolis", "nepomuceno", "timoteo", "itabirito", "curso tecnico", "cursos tecnicos",
    "informatica", "edificacoes", "mecatronica", "ensino medio integrado",
    "ensino tecnico", "processo seletivo", "vestibular", "edital", "inscricao",
    "inscricoes", "matricula", "matriculas", "prova", "gabarito", "campus",
    "cotas", "isencao", "taxa de inscricao", "lista de espera", "resultado final",
    "nota de corte", "documentos para matricula", "quiz vocacional", "quiz",
    "areas de atuacao", "grade curricular", "disciplinas", "vagas",
)

FORA_ESCOPO = (
    "filme", "filmes", "serie", "series", "receita", "culinaria", "futebol",
    "jogo de futebol", "horoscopo", "piada", "musica", "letra de musica",
    "programa em python", "codigo python", "escreva um codigo", "crie um codigo",
    "capital da", "quanto e", "quanto eh", "calcule", "resolva a equacao",
    "conta de matematica", "previsao do tempo", "noticias do mundo",
)

CONTINUACAO = (
    "e quando", "e onde", "e quais", "e qual", "e como", "e a", "e o",
    "quando", "onde", "qual", "quais", "como", "quanto custa", "e para",
    "me explique melhor", "pode explicar", "tem mais informacoes", "e isso",
)


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in texto if not unicodedata.combining(c))


def no_escopo(pergunta, historico=None):
    texto = normalizar(pergunta).strip()
    # Rejeita pedidos explicitamente alheios, inclusive quando citam SAVOT/CEFET
    # apenas para tentar contornar a restrição.
    if re.search(r"\b\d+\s*[+*/=-]\s*\d+\b", texto):
        return False
    if any(termo in texto for termo in FORA_ESCOPO):
        return False
    if any(termo in texto for termo in TERMOS):
        return True
    # Continuação curta de uma conversa comprovadamente sobre o CEFET.
    historico = historico or []
    anteriores = [x.get("texto", "") for x in historico if x.get("papel") == "usuario"]
    if anteriores and len(texto) <= 100 and any(texto.startswith(t) for t in CONTINUACAO):
        return any(any(t in normalizar(p) for t in TERMOS) for p in anteriores[-3:])
    return False


def resposta_fora_escopo():
    return {"resposta": RECUSA, "fontes": []}
