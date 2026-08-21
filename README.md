# Ponte Solidária

Aplicação web que conecta pessoas que possuem alimentos ou roupas para doar com pessoas que precisam dessas doações.

O projeto utiliza Python, FastAPI e Jinja2 sobre o runtime Python da Cloudflare Workers. Nesta versão, as doações e manifestações de interesse são mantidas temporariamente em memória.

## Pré-requisitos

- Uma conta na Cloudflare para realizar o deploy.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado.
- Node.js instalado, exigido pelo fluxo do Pywrangler/Wrangler.

### Executando localmente

Na pasta raiz do projeto, instale as dependências e inicie o ambiente local compatível com Workers:

```powershell
uv sync
uv run pywrangler dev
```

O endereço local será informado no terminal, normalmente `http://localhost:8787`.

O comando antigo `python app.py` não é mais utilizado, pois a aplicação agora é iniciada pelo runtime local do Cloudflare Workers.

### Deploy na Cloudflare

Primeiro, autentique o Wrangler na sua conta Cloudflare:

```powershell
uv run pywrangler login
```

Depois, publique o Worker:

```powershell
uv run pywrangler deploy
```

O deploy envia o Worker Python e os arquivos estáticos configurados em `wrangler.jsonc`. Nenhum token ou credencial deve ser salvo no repositório.

## Limitação temporária dos dados

Ainda não existe banco de dados. As doações e manifestações de interesse criadas pela interface ficam apenas na memória do isolate que processou a requisição. Elas podem desaparecer a qualquer momento, não são compartilhadas de forma confiável entre isolates e sempre são perdidas em reinicializações ou novos deploys.

Essa limitação é intencional nesta etapa. A persistência será implementada posteriormente com Cloudflare D1.
