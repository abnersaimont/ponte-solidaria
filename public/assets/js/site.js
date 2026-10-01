const doacoes = {
    1: { categoria: "Alimentos", titulo: "Cesta básica", descricao: "Cesta básica com arroz, feijão, macarrão e óleo. Os produtos estão fechados e dentro do prazo de validade.", quantidade: "1 cesta", bairro: "Centro" },
    2: { categoria: "Roupas", titulo: "Roupas infantis", descricao: "Conjunto com roupas infantis variadas, todas limpas e em bom estado de conservação. Indicado para crianças de 4 a 6 anos.", quantidade: "10 peças", bairro: "Vila Nova" },
    3: { categoria: "Alimentos", titulo: "Pacotes de arroz", descricao: "Cinco pacotes de arroz de 1 kg, fechados e dentro do prazo de validade.", quantidade: "5 pacotes de 1 kg", bairro: "Jardim das Flores" },
    4: { categoria: "Roupas", titulo: "Agasalhos adultos", descricao: "Três agasalhos adultos em bom estado, sendo dois de tamanho M e um de tamanho G.", quantidade: "3 peças", bairro: "Santa Clara" },
    5: { categoria: "Alimentos", titulo: "Leite em pó", descricao: "Duas latas de leite em pó ainda fechadas e dentro do prazo de validade.", quantidade: "2 latas", bairro: "Boa Vista" },
    6: { categoria: "Roupas", titulo: "Calças masculinas", descricao: "Duas calças jeans masculinas tamanho 42, limpas e sem rasgos.", quantidade: "2 peças", bairro: "Parque Verde" }
};

const parametros = new URLSearchParams(window.location.search);
const id = parametros.get("id") || "1";
const doacao = doacoes[id] || doacoes[1];

if (document.body.dataset.page === "detalhe") {
    document.title = `${doacao.titulo} — Ponte Solidária`;
    document.querySelector("#detalhe-categoria").textContent = doacao.categoria;
    document.querySelector("#detalhe-titulo").textContent = doacao.titulo;
    document.querySelector("#detalhe-descricao").textContent = doacao.descricao;
    document.querySelector("#detalhe-quantidade").textContent = doacao.quantidade;
    document.querySelector("#detalhe-bairro").textContent = doacao.bairro;
    document.querySelector("#interesse-link").href = `/interesse.html?id=${id}`;
}

if (document.body.dataset.page === "interesse") {
    document.querySelector("#interesse-titulo").textContent = doacao.titulo;
    document.querySelector("#interesse-resumo").textContent = `${doacao.categoria} • ${doacao.bairro}`;
    document.querySelector("#voltar-doacao").href = `/doacao.html?id=${id}`;
}

document.querySelectorAll(".demo-form").forEach((formulario) => {
    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        if (!formulario.reportValidity()) return;
        const resultado = formulario.querySelector(".demo-result");
        resultado.textContent = formulario.dataset.demoMessage;
        resultado.hidden = false;
    });
});
