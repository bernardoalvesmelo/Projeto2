let route = "http://127.0.0.1:5000/";

let action = "insert";
let currentId = 1;
let chamadoList = [];
let chamadoShowList = chamadoList;
let equipamentos = [];


const itemsContainer = document.getElementById("items-container");
const overlay = document.getElementById("overlay");
overlay.style.display = "none";

const inputText = document.getElementById("input-text");
const inputDate = document.getElementById("input-date");
const inputDescription = document.getElementById("input-description");

const selectEquip = document.getElementById("select-equipment");

const okButton = document.getElementById("ok-button");
const closeButton = document.getElementById("close-button");
const searchBar = document.getElementById("search");

const createChamadoButton = document.getElementById("create-item-button");

createChamadoButton.addEventListener("click", () => {
    startlist();
    if (equipamentos[0] != null) {
        action = "insert";
        optionsEquips();
        overlay.style.display = "flex";
    }
    else {
        alert("Cadastre ao menos um equipamento para criar um chamado");
    }
});

searchBar.addEventListener("keyup", () => {
    updateChamadoSearch(searchBar.value);
});

okButton.addEventListener("click", () => {
    if (!validateInput()) {
        return;
    }
    let chamado = {};
    if (action === "insert") {
        chamado = {};
        chamado.titulo = inputText.value;
        chamado.data_abertura = inputDate.value;
        chamado.descricao = inputDescription.value;
        chamado.Equipamentos_id = selectEquip.options[selectEquip.selectedIndex].value;

        let executable = (data) => {
            console.log(data);
            startlist();
        };

        postJson("chamados/insert", chamado, executable);

    }
    else if (action === "update") {
        chamado = chamadoList.find(chamado => chamado.id === currentId);
        chamado.titulo = inputText.value;
        chamado.data_abertura = inputDate.value;
        chamado.descricao = inputDescription.value;
        chamado.Equipamentos_id = selectEquip.options[selectEquip.selectedIndex].value;
        let executable = (data) => {
            console.log(data);
            startlist();
        };

        postJson("chamados/update", chamado, executable);

    }
    inputText.value = "";
    inputDate.value = "";
    inputDescription.value = "";
    selectEquip.value = "";
    overlay.style.display = "none";
});

function validateInput() {
    if (inputText.value &&
        inputDate.value &&
        inputDescription.value &&
        selectEquip.value) {
        return true;
    }
    else {
        alert("Não deixe nehum campo em branco");
        return false;
    }
}

closeButton.addEventListener("click", () => {
    inputText.value = "";
    inputDate.value = "";
    inputDescription.value = "";
    selectEquip.value = "";
    overlay.style.display = "none";
});

function updateChamadoSearch(search) {
    search = search.trim().toLowerCase();
    chamadoShowList = [];
    for (let i = 0; i < chamadoList.length; i++) {
        let equipamento = equipamentos.find(equipment => equipment.id === chamadoList[i].Equipamentos_id);
        let period = Date.now() - new Date(chamadoList[i].data_abertura).getTime();
        let periodDays = Math.floor(period / (3600 * 1000 * 24));
        if (chamadoList[i].titulo.toLowerCase().includes(search) ||
            `${periodDays}`.includes(search) ||
            equipamento.nome.toLowerCase().includes(search)) {
            chamadoShowList.push(chamadoList[i]);
        }
    }
    renderChamado();
}

function updateChamadoShowed() {
    chamadoShowList = [];
    for (let i = 0; i < chamadoList.length; i++) {
        chamadoShowList.push(chamadoList[i]);
    }
    renderChamado();
}

function renderChamado() {
    let chamadoHtml = "";
    for (let i = 0; i < chamadoShowList.length; i++) {
        let period = Date.now() - new Date(chamadoShowList[i].data_abertura).getTime();
        let periodDays = Math.floor(period / (3600 * 1000 * 24));
        let equipamento = equipamentos.find(equipment => equipment.id === chamadoShowList[i].Equipamentos_id);
        chamadoHtml += `<div class="item-sub">
       <div>
       <button class="edit-button" id="${chamadoShowList[i].id}" onClick="editButtonClick(this.id)">Editar</button>
       <button id="${chamadoShowList[i].id}" onClick="removeButtonClick(this.id)">Remover</button>
       </div>
       <div  class="item" id="${chamadoShowList[i].id}">
       <p class="main-text">CHAMADO: ${chamadoShowList[i].titulo}</p>
       <p class="main-text">EQUIPAMENTO: ${equipamento.nome}</p>
       <p class="main-text">DIAS_ABERTURA: ${periodDays}</p>
       </div>
       </div>`
            ;

    }
    itemsContainer.innerHTML = chamadoHtml;
}

function optionsEquips() {
    let selectHtml = "";
    for (let i = 0; i < equipamentos.length; i++) {
        selectHtml += `<option value = "${equipamentos[i].id}">${equipamentos[i].nome}</option>`;
    }
    selectEquip.innerHTML = selectHtml;
}

function editButtonClick(id) {
    currentId = id;
    action = "update";
    let chamado = chamadoList.find(chamado => chamado.id === id);
    optionsEquips();
    inputText.value = chamado.titulo;
    inputDate.value = chamado.data_abertura;
    inputDescription.value = chamado.descricao;
    selectEquip.value = chamado.Equipamentos_id;
    overlay.style.display = "flex";
}

function removeButtonClick(id) {
    let isCertain = confirm("Você deseja remover este chamado?");
    if (isCertain) {
        let executable = (data) => {
            console.log(data)
            startlist();
        };

        getJson(`chamados/remove/${id}`, executable);
    }
}

function getJson(header, executable) {
    try {
        fetch(route + header, {
            method: 'GET',
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                try {
                    if (data) {
                        executable(data);
                    }
                } catch (error) {
                    alert(`Erro: ${data}`);
                    console.log(data);
                }
            });
    } catch (error) {
        alert(`Erro: ${error}`);
    }
}

function postJson(header, object, executable) {
    for (attribute in object) {
        attribute = DOMPurify.sanitize(attribute);
    }
    try {
        fetch(route + header, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(object),
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                try {
                    executable(data);
                } catch (error) {
                    alert(`Erro: ${data}`);
                }
            });
    } catch (error) {
        alert(`Erro: ${error}`);
    }
}

function startlist() {
    let executable = (data) => {
        equipamentos = data;
        let executable2 = (data) => {
            chamadoList = data;
            updateChamadoShowed();
        }
        getJson("chamados", executable2);
    }
    getJson("equipamentos", executable);

}

function loginState() {
    const logedCookie = document.cookie.split(";").filter(n=>n.includes("session"));
    if (logedCookie != "") {
        document.getElementById("login-form").style.display = "none";
        console.log(document.cookie);
        startlist();
    } else {
        document.getElementById("login-form").style.display = "flex";
        console.log(document.cookie);
    }
}

const loginForm = document.getElementById("login-forms");

loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(loginForm);
    let executable = (data) => {
        console.log(data);
        loginState();
    }
    let header = "login";


    try {
        fetch(route + header, {
            method: 'POST',
            body: formData,
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                try {
                    executable(data);
                } catch (error) {
                    alert(`Erro: ${data}`);
                }
            });
    } catch (error) {
        alert(`Erro: ${error}`);
    }

});

const logoutButton = document.getElementById("logout-item-button");
logoutButton.addEventListener("click", () => {
    logout();
});

function logout() {
    let executable = (data) => {
        console.log(data);
        loginState();
    }
    let header = "logout";
    try {
        fetch(route + header, {
            method: 'GET',
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                try {
                    executable(data);
                } catch (error) {
                    alert(`Erro: ${data}`);
                }
            });
    } catch (error) {
        alert(`Erro: ${error}`);
    }
    window.location.reload();
}