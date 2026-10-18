(() => {
  const form = document.getElementById('chatbot-form');
  if (!form) return;
  const entrada = document.getElementById('chatbot-input');
  const enviar = document.getElementById('chatbot-enviar');
  const mensagens = document.getElementById('chatbot-mensagens');
  const endpoint = form.parentElement.dataset.endpoint;
  const csrf = form.querySelector('[name=csrfmiddlewaretoken]').value;
  const historico = [];
  function mensagem(texto, papel, fontes = []) {
    const bloco = document.createElement('div');
    bloco.className = 'chatbot-mensagem chatbot-mensagem--' + (papel === 'usuario' ? 'usuario' : 'bot');
    const corpo = document.createElement('div');
    corpo.textContent = texto;
    bloco.appendChild(corpo);
    if (fontes.length) {
      const lista = document.createElement('ul');
      lista.className = 'chatbot-fontes';
      fontes.forEach(fonte => {
        try {
          const url = new URL(fonte.url, window.location.origin);
          if (fonte.interno) {
            if (url.origin !== window.location.origin) return;
          } else if (url.protocol !== 'https:') return;
          const item = document.createElement('li');
          const link = document.createElement('a');
          link.href = url.href;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          link.textContent = (fonte.interno ? 'No SAVOT: ' : fonte.oficial ? 'Fonte oficial: ' : 'Fonte externa: ') + (fonte.titulo || url.hostname);
          item.appendChild(link);
          lista.appendChild(item);
        } catch (_) { /* URL inválida */ }
      });
      bloco.appendChild(lista);
    }
    mensagens.appendChild(bloco);
    mensagens.scrollTop = mensagens.scrollHeight;
    return bloco;
  }
  form.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    const pergunta = entrada.value.trim();
    if (!pergunta || enviar.disabled) return;
    const contexto = historico.slice(-6);
    mensagem(pergunta, 'usuario');
    entrada.value = '';
    enviar.disabled = true;
    entrada.disabled = true;
    const aguardando = mensagem('Pesquisando informações...', 'assistente');
    try {
      const resposta = await fetch(endpoint, {
        method: 'POST', credentials: 'same-origin',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf},
        body: JSON.stringify({mensagem: pergunta, historico: contexto})
      });
      const dados = await resposta.json();
      aguardando.remove();
      if (!resposta.ok) throw new Error(dados.erro || 'Erro na consulta.');
      mensagem(dados.resposta, 'assistente', dados.fontes || []);
      historico.push({papel: 'usuario', texto: pergunta.slice(0, 400)});
      historico.push({papel: 'assistente', texto: dados.resposta.slice(0, 400)});
      if (historico.length > 6) historico.splice(0, historico.length - 6);
    } catch (erro) {
      aguardando.remove();
      mensagem(erro.message || 'Não foi possível responder.', 'assistente');
    } finally {
      enviar.disabled = false;
      entrada.disabled = false;
      entrada.focus();
    }
  });
})();
