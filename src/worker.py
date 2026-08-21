from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs

import asgi
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from workers import WorkerEntrypoint


DOACOES = [
    {
        "id": 1,
        "categoria": "Alimentos",
        "titulo": "Cesta básica",
        "descricao_curta": "Arroz, feijão, macarrão e óleo.",
        "descricao": "Cesta básica com arroz, feijão, macarrão e óleo. Os produtos estão fechados e dentro do prazo de validade.",
        "quantidade": "1 cesta",
        "bairro": "Centro",
        "status": "Disponível",
    },
    {
        "id": 2,
        "categoria": "Roupas",
        "titulo": "Roupas infantis",
        "descricao_curta": "10 peças infantis em bom estado.",
        "descricao": "Conjunto com roupas infantis variadas, todas limpas e em bom estado de conservação. Indicado para crianças de 4 a 6 anos.",
        "quantidade": "10 peças",
        "bairro": "Vila Nova",
        "status": "Disponível",
    },
    {
        "id": 3,
        "categoria": "Alimentos",
        "titulo": "Pacotes de arroz",
        "descricao_curta": "5 pacotes disponíveis.",
        "descricao": "Cinco pacotes de arroz de 1 kg, fechados e dentro do prazo de validade. Podem ser retirados juntos.",
        "quantidade": "5 pacotes de 1 kg",
        "bairro": "Jardim das Flores",
        "status": "Disponível",
    },
    {
        "id": 4,
        "categoria": "Roupas",
        "titulo": "Agasalhos adultos",
        "descricao_curta": "Agasalhos para o período de frio.",
        "descricao": "Três agasalhos adultos em bom estado, sendo dois de tamanho M e um de tamanho G.",
        "quantidade": "3 peças",
        "bairro": "Santa Clara",
        "status": "Disponível",
    },
    {
        "id": 5,
        "categoria": "Alimentos",
        "titulo": "Leite em pó",
        "descricao_curta": "Latas fechadas e dentro da validade.",
        "descricao": "Duas latas de leite em pó ainda fechadas, armazenadas em local seco e dentro do prazo de validade.",
        "quantidade": "2 latas",
        "bairro": "Boa Vista",
        "status": "Disponível",
    },
    {
        "id": 6,
        "categoria": "Roupas",
        "titulo": "Calças masculinas",
        "descricao_curta": "Calças jeans tamanho 42.",
        "descricao": "Duas calças jeans masculinas tamanho 42. As peças são usadas, mas estão limpas e sem rasgos.",
        "quantidade": "2 peças",
        "bairro": "Parque Verde",
        "status": "Disponível",
    },
]

INTERESSES = []

templates = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def url_for(nome, **valores):
    rotas = {
        "index": "/",
        "listar_doacoes": "/doacoes",
        "cadastrar_doacao": "/doacoes/nova",
        "confirmar_interesse": "/interesse/confirmacao",
    }
    if nome == "static":
        return f"/{valores['filename']}"
    if nome == "detalhe_doacao":
        return f"/doacoes/{valores['doacao_id']}"
    if nome == "demonstrar_interesse":
        return f"/doacoes/{valores['doacao_id']}/interesse"
    return rotas[nome]


def render_template(nome, **contexto):
    contexto["url_for"] = url_for
    conteudo = templates.get_template(nome).render(**contexto)
    return HTMLResponse(conteudo)


async def ler_formulario(request: Request):
    corpo = (await request.body()).decode("utf-8")
    campos = parse_qs(corpo, keep_blank_values=True)
    return {nome: valores[-1].strip() for nome, valores in campos.items()}


def buscar_doacao(doacao_id):
    return next((item for item in DOACOES if item["id"] == doacao_id), None)


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/", response_class=HTMLResponse)
async def index():
    return render_template("index.html", doacoes=DOACOES[:3])


@app.get("/doacoes", response_class=HTMLResponse)
async def listar_doacoes():
    return render_template("doacoes.html", doacoes=DOACOES)


@app.get("/doacoes/nova", response_class=HTMLResponse)
async def formulario_doacao():
    dados = {campo: "" for campo in ("categoria", "titulo", "descricao", "quantidade", "bairro", "nome_doador", "contato")}
    return render_template("cadastrar_doacao.html", dados=dados, erro=None)


@app.post("/doacoes/nova", response_class=HTMLResponse)
async def cadastrar_doacao(request: Request):
    formulario = await ler_formulario(request)
    dados = {
        campo: formulario.get(campo, "")
        for campo in ("categoria", "titulo", "descricao", "quantidade", "bairro", "nome_doador", "contato")
    }
    campos_obrigatorios = {
        "categoria": "Categoria",
        "titulo": "Título da doação",
        "descricao": "Descrição",
        "quantidade": "Quantidade",
        "bairro": "Bairro",
        "nome_doador": "Nome do doador",
        "contato": "Contato",
    }
    campos_vazios = [nome for campo, nome in campos_obrigatorios.items() if not dados[campo]]

    if dados["categoria"] and dados["categoria"] not in {"Alimentos", "Roupas"}:
        return render_template("cadastrar_doacao.html", dados=dados, erro="Selecione uma categoria válida.")
    if campos_vazios:
        erro = "Preencha os campos obrigatórios: " + ", ".join(campos_vazios) + "."
        return render_template("cadastrar_doacao.html", dados=dados, erro=erro)

    novo_id = max((doacao["id"] for doacao in DOACOES), default=0) + 1
    DOACOES.append(
        {
            "id": novo_id,
            "categoria": dados["categoria"],
            "titulo": dados["titulo"],
            "descricao_curta": dados["descricao"],
            "descricao": dados["descricao"],
            "quantidade": dados["quantidade"],
            "bairro": dados["bairro"],
            "nome_doador": dados["nome_doador"],
            "contato": dados["contato"],
            "status": "Disponível",
        }
    )
    return RedirectResponse(url_for("detalhe_doacao", doacao_id=novo_id), status_code=303)


@app.get("/doacoes/{doacao_id}", response_class=HTMLResponse)
async def detalhe_doacao(doacao_id: int):
    doacao = buscar_doacao(doacao_id)
    if doacao is None:
        raise HTTPException(status_code=404)
    return render_template("detalhe_doacao.html", doacao=doacao)


@app.get("/doacoes/{doacao_id}/interesse", response_class=HTMLResponse)
async def formulario_interesse(doacao_id: int):
    doacao = buscar_doacao(doacao_id)
    if doacao is None:
        raise HTTPException(status_code=404)
    return render_template(
        "demonstrar_interesse.html",
        doacao=doacao,
        dados={"nome": "", "contato": "", "mensagem": ""},
        erro=None,
    )


@app.post("/doacoes/{doacao_id}/interesse", response_class=HTMLResponse)
async def demonstrar_interesse(doacao_id: int, request: Request):
    doacao = buscar_doacao(doacao_id)
    if doacao is None:
        raise HTTPException(status_code=404)

    formulario = await ler_formulario(request)
    dados = {campo: formulario.get(campo, "") for campo in ("nome", "contato", "mensagem")}
    campos_vazios = [nome for campo, nome in (("nome", "Nome"), ("contato", "Contato")) if not dados[campo]]
    if campos_vazios:
        erro = "Preencha os campos obrigatórios: " + ", ".join(campos_vazios) + "."
        return render_template("demonstrar_interesse.html", doacao=doacao, dados=dados, erro=erro)

    novo_id = max((interesse["id"] for interesse in INTERESSES), default=0) + 1
    INTERESSES.append(
        {
            "id": novo_id,
            "doacao_id": doacao_id,
            "nome": dados["nome"],
            "contato": dados["contato"],
            "mensagem": dados["mensagem"],
            "criado_em": datetime.now(),
        }
    )
    return RedirectResponse(url_for("confirmar_interesse"), status_code=303)


@app.get("/interesse/confirmacao", response_class=HTMLResponse)
async def confirmar_interesse():
    return render_template("confirmacao_interesse.html")


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request.js_object, self.env)
