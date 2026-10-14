document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chatbot-form");
    const input = document.getElementById("chatbot-input");
    const mensagens = document.getElementById("chatbot-mensagens");

    if (!form) {
        return;
    }

    const tokenInput = form.querySelector("[name=csrfmiddlewaretoken]");
    const csrfToken = tokenInput ? tokenInput.value : "";

    function adicionarMensagem(texto, autor) {
        const bolha = document.createElement("div");
        bolha.classList.add("chatbot-mensagem", `chatbot-mensagem--${autor}`);
        bolha.textContent = texto;
        mensagens.appendChild(bolha);
        mensagens.scrollTop = mensagens.scrollHeight;
        return bolha;
    }

    form.addEventListener("submit", async function (evento) {
        evento.preventDefault();

        const pergunta = input.value.trim();
        if (!pergunta) {
            return;
        }

        adicionarMensagem(pergunta, "usuario");
        input.value = "";
        input.disabled = true;

        const bolhaResposta = adicionarMensagem("Digitando...", "bot");

        try {
            const resposta = await fetch("/api/chatbot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ pergunta: pergunta }),
            });

            const dados = await resposta.json();

            const texto = dados.resposta || dados.erro || "Algo deu errado, tente novamente.";
            bolhaResposta.textContent = "";
            const partes = texto.split(/(https:\/\/[^\s]+)/g);
            partes.forEach(function (parte) {
                if (parte.startsWith("https://")) {
                    const link = document.createElement("a");
                    link.href = parte;
                    link.textContent = parte;
                    link.target = "_blank";
                    link.rel = "noopener noreferrer";
                    bolhaResposta.appendChild(link);
                } else {
                    bolhaResposta.appendChild(document.createTextNode(parte));
                }
            });
        } catch (erro) {
            bolhaResposta.textContent =
                "Não consegui me conectar ao assistente. Verifique sua conexão e tente novamente.";
        } finally {
            input.disabled = false;
            input.focus();
        }
    });
});
