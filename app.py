from datetime import datetime

from flask import Flask, abort, redirect, render_template, request, url_for


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


def buscar_doacao(doacao_id):
    return next((item for item in DOACOES if item["id"] == doacao_id), None)


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", doacoes=DOACOES[:3])

    @app.route("/doacoes")
    def listar_doacoes():
        return render_template("doacoes.html", doacoes=DOACOES)

    @app.route("/doacoes/nova", methods=["GET", "POST"])
    def cadastrar_doacao():
        dados = {
            "categoria": request.form.get("categoria", "").strip(),
            "titulo": request.form.get("titulo", "").strip(),
            "descricao": request.form.get("descricao", "").strip(),
            "quantidade": request.form.get("quantidade", "").strip(),
            "bairro": request.form.get("bairro", "").strip(),
            "nome_doador": request.form.get("nome_doador", "").strip(),
            "contato": request.form.get("contato", "").strip(),
        }

        if request.method == "POST":
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
                return render_template(
                    "cadastrar_doacao.html",
                    dados=dados,
                    erro="Selecione uma categoria válida.",
                )

            if campos_vazios:
                return render_template(
                    "cadastrar_doacao.html",
                    dados=dados,
                    erro="Preencha os campos obrigatórios: " + ", ".join(campos_vazios) + ".",
                )

            novo_id = max((doacao["id"] for doacao in DOACOES), default=0) + 1
            nova_doacao = {
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
            DOACOES.append(nova_doacao)
            return redirect(url_for("detalhe_doacao", doacao_id=novo_id))

        return render_template("cadastrar_doacao.html", dados=dados, erro=None)

    @app.route("/doacoes/<int:doacao_id>")
    def detalhe_doacao(doacao_id):
        doacao = buscar_doacao(doacao_id)
        if doacao is None:
            abort(404)
        return render_template("detalhe_doacao.html", doacao=doacao)

    @app.route("/doacoes/<int:doacao_id>/interesse", methods=["GET", "POST"])
    def demonstrar_interesse(doacao_id):
        doacao = buscar_doacao(doacao_id)
        if doacao is None:
            abort(404)

        dados = {
            "nome": request.form.get("nome", "").strip(),
            "contato": request.form.get("contato", "").strip(),
            "mensagem": request.form.get("mensagem", "").strip(),
        }

        if request.method == "POST":
            campos_vazios = []
            if not dados["nome"]:
                campos_vazios.append("Nome")
            if not dados["contato"]:
                campos_vazios.append("Contato")

            if campos_vazios:
                return render_template(
                    "demonstrar_interesse.html",
                    doacao=doacao,
                    dados=dados,
                    erro="Preencha os campos obrigatórios: " + ", ".join(campos_vazios) + ".",
                )

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
            return redirect(url_for("confirmar_interesse", interesse_id=novo_id))

        return render_template(
            "demonstrar_interesse.html",
            doacao=doacao,
            dados=dados,
            erro=None,
        )

    @app.route("/interesses/<int:interesse_id>/confirmacao")
    def confirmar_interesse(interesse_id):
        interesse = next((item for item in INTERESSES if item["id"] == interesse_id), None)
        if interesse is None:
            abort(404)
        return render_template("confirmacao_interesse.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
