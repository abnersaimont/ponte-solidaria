# Ponte Solidária

Site demonstrativo de uma iniciativa social que conecta pessoas que possuem alimentos ou roupas para doar com pessoas que precisam dessas doações.

O projeto é totalmente estático e utiliza apenas HTML, CSS e JavaScript. Os formulários são demonstrativos: nenhum dado é enviado ou armazenado.

## Estrutura

- `public/index.html`: página inicial;
- `public/doacoes.html`: listagem e filtros visuais;
- `public/doacao.html`: detalhes das doações fictícias;
- `public/quero-doar.html`: formulário demonstrativo de doação;
- `public/interesse.html`: formulário demonstrativo de interesse;
- `public/assets/`: CSS e JavaScript.

## Executando localmente

Para testar os caminhos exatamente como serão publicados, execute um servidor HTTP local apontando para a pasta `public`. Com o Wrangler disponível:

```powershell
npx wrangler pages dev public
```

O endereço local será informado no terminal, normalmente `http://localhost:8788`.

## Deploy na Cloudflare Pages

Ao conectar este repositório pelo painel da Cloudflare Pages, utilize:

- **Framework preset:** None;
- **Production branch:** `main`;
- **Build command:** deixe vazio ou use `exit 0`;
- **Build output directory:** `public`.

Não são necessários Python, FastAPI, Jinja2, Workers, banco de dados ou variáveis de ambiente.
