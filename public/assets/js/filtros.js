const botoesDeFiltro = document.querySelectorAll("[data-filter]");
const cardsDeDoacao = document.querySelectorAll("[data-categoria]");
const mensagemVazia = document.querySelector("#sem-resultados");

botoesDeFiltro.forEach((botao) => {
    botao.addEventListener("click", () => {
        const categoria = botao.dataset.filter;
        let totalVisivel = 0;

        botoesDeFiltro.forEach((item) => item.classList.remove("active"));
        botao.classList.add("active");

        cardsDeDoacao.forEach((card) => {
            const deveExibir = categoria === "todas" || card.dataset.categoria === categoria;
            card.hidden = !deveExibir;
            if (deveExibir) totalVisivel += 1;
        });

        mensagemVazia.hidden = totalVisivel !== 0;
    });
});
