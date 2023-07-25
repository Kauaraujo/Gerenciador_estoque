document.addEventListener("DOMContentLoaded", function () {
  // Lista para armazenar os itens, descrições e quantidades
  const itensList = [];

  function addItem(codigo, descricao, quantidade) {
    itensList.push({ codigo: codigo, descricao: descricao, quantidade: quantidade });
  }

  function showItensList() {
    const itensListContainer = document.getElementById("itens_list");
    itensListContainer.innerHTML = "";

    for (const item of itensList) {
      const itemDiv = document.createElement("div");
      itemDiv.textContent = `Código: ${item.codigo}, Descrição: ${item.descricao}, Quantidade: ${item.quantidade}`;
      itensListContainer.appendChild(itemDiv);
    }
  }

  document.getElementById("baixa_itens_form").addEventListener("submit", function (event) {
    event.preventDefault();

    const itemInput = document.getElementById("item");
    const quantidadeInput = document.getElementById("quantidade");
    const codigo = itemInput.value;
    const quantidade = quantidadeInput.value;

    fetch("/buscar_descricao", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ codigo: codigo })
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const descricao = data.descricao;
          itemInput.value = descricao;
          addItem(codigo, descricao, quantidade);
          showItensList();
        } else {
          itemInput.value = "";
          alert("Código não encontrado.");
        }
      })
      .catch(error => {
        console.error("Erro na solicitação AJAX:", error);
      });
  });

  document.getElementById("enviar_btn").addEventListener("click", function () {
    fetch("/gerar_csv", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ itensList: itensList })
    })
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const a = document.createElement("a");
        a.href = url;
        a.download = "itens.csv"; // O nome do arquivo que será baixado
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
      .catch(error => {
        console.error("Erro na solicitação AJAX:", error);
      });
  });
});
