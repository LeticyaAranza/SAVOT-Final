# Tavily no SAVOT — preparação sem gastar créditos

## O que foi feito
- Criado `pesquisa_web/tavily_busca.py` com `pesquisar(pergunta, incluir_internet_geral=False)`.
- Acrescentada a biblioteca `tavily-python` ao `requirements.txt`.
- Adicionada a variável `TAVILY_API_KEY` ao `render.yaml` e ao `.env.example`.
- Criado `.gitignore` para evitar publicar a chave.
- **Nenhuma rota, interface ou inicialização automática chama a Tavily.** Nenhum crédito é gasto só por instalar ou hospedar.

## Configurar localmente
1. Na pasta de `manage.py`, crie `.env` a partir de `.env.example`.
2. Coloque `TAVILY_API_KEY=sua_chave` no `.env` (não envie a chave no chat/GitHub).
3. Instale dependências com `python -m pip install -r requirements.txt` no ambiente virtual.
4. Não é necessário alterar `settings.py`: o projeto já carrega `.env`.

## Configurar no Render
1. Faça upload/push do projeto atualizado.
2. No serviço Web, abra **Environment** e crie `TAVILY_API_KEY` com a chave como valor.
3. Salve e faça deploy; o `render.yaml` também declara a variável com `sync: false` para quem usa Blueprint.
4. Confira que o diretório raiz do serviço é a pasta que contém `manage.py`, como antes.
5. Não é necessário adicionar nenhuma outra chave para esta etapa.

## Uso futuro (não executar se não quiser gastar créditos)
No Django shell, após configurar a chave:

```python
from pesquisa_web.tavily_busca import pesquisar
resultados = pesquisar("inscrições processo seletivo técnico 2027")
```

A pesquisa geral só será realizada se a busca oficial retornar vazia e você passar `incluir_internet_geral=True`. Encontrar resultados não garante que sejam atuais ou suficientes. Na etapa seguinte, implementar relevância, retificações, fontes citadas e proteção de consumo antes de expor uma rota pública.

## O que não está pronto
Ainda não há chatbot conversacional, integração com IA, pesquisa disparada pela interface, histórico, limitação de requisições ou verificação de atualidade. Não exponha esta função diretamente ao público sem controles de uso.
