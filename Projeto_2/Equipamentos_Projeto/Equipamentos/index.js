let route = "http://127.0.0.1:5000/";

let action = "insert";
let currentId = 1;
let equipmentList = [];
let equipmentShowList = equipmentList;


const itemsContainer = document.getElementById("items-container");
const overlay = document.getElementById("overlay");
overlay.style.display = "none";

const inputText = document.getElementById("input-text");
const inputDate = document.getElementById("input-date");
const inputNumber = document.getElementById("input-number");
const inputMaker = document.getElementById("input-maker");
const inputPrice = document.getElementById("input-price");

const okButton = document.getElementById("ok-button");
const closeButton = document.getElementById("close-button");
const searchBar = document.getElementById("search");

const createEquipmentButton = document.getElementById("create-item-button");

startlist();

createEquipmentButton.addEventListener("click", () => {
    action = "insert";
    overlay.style.display = "flex";
});

searchBar.addEventListener("keyup", () => {
    updateEquipmentSearch(searchBar.value);
});

okButton.addEventListener("click", () => {
    if (!validateInput()) {
        return;
    }
    let equipment = {};
    if (action === "insert") {
        equipment = {};
        equipment.nome = inputText.value;
        equipment.data_fabricacao = inputDate.value;
        equipment.preco_aquisicao = inputPrice.value;
        equipment.fabricante = inputMaker.value;
        equipment.numero_serie = inputNumber.value;

        let executable = (data) => {
            console.log(data);
            startlist();
        };

        postJson("equipamentos/insert", equipment, executable);

    }
    else if (action === "update") {
        equipment = equipmentList.find(equipment => equipment.id === currentId);
        equipment.nome = inputText.value;
        equipment.data_fabricacao = inputDate.value;
        equipment.preco_aquisicao = inputPrice.value;
        equipment.fabricante = inputMaker.value;
        equipment.numero_serie = inputNumber.value;
        let executable = (data) => {
            console.log(data);
            startlist();
        };

        postJson("equipamentos/update", equipment, executable);

    }
    inputText.value = "";
    inputDate.value = "";
    inputPrice.value = "";
    inputMaker.value = "";
    inputNumber.value = "";
    overlay.style.display = "none";
});

function validateInput() {

    if (inputText.value.length < 6) {
        alert("O nome deve ter no mínimo 6 characteres");
        return false;
    }
    if (inputText.value &&
        inputDate.value &&
        inputPrice.value &&
        inputMaker.value &&
        inputNumber.value) {
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
    inputPrice.value = "";
    inputMaker.value = "";
    inputNumber.value = "";
    overlay.style.display = "none";
});

function updateEquipmentSearch(search) {
    search = search.trim().toLowerCase();
    equipmentShowList = [];
    for (let i = 0; i < equipmentList.length; i++) {
        if (equipmentList[i].nome.toLowerCase().includes(search) ||
            equipmentList[i].numero_serie.toLowerCase().includes(search) ||
            equipmentList[i].fabricante.toLowerCase().includes(search)) {
            equipmentShowList.push(equipmentList[i]);
        }
    }
    renderEquipment();
}

function updateEquipmentShowed() {
    equipmentShowList = [];
    for (let i = 0; i < equipmentList.length; i++) {
        equipmentShowList.push(equipmentList[i]);
    }
    renderEquipment();
}

function renderEquipment() {
    let equipmentHtml = "";
    for (let i = 0; i < equipmentShowList.length; i++) {
        equipmentHtml += `<div class="item-sub">
       <div>
       <button class="edit-button" id="${equipmentShowList[i].id}" onClick="editButtonClick(this.id)">Editar</button>
       <button id="${equipmentShowList[i].id}" onClick="removeButtonClick(this.id)">Remover</button>
       </div>
       <div  class="item" id="${equipmentShowList[i].id}">
       <p class="main-text">EQUIPAMENTO: ${equipmentShowList[i].nome}</p>
       <p class="main-text">NÚMERO_SÉRIE: ${equipmentShowList[i].numero_serie}</p>
       <p class="main-text">FABRICANTE: ${equipmentShowList[i].fabricante}</p>
       </div>
       </div>`
            ;

    }
    itemsContainer.innerHTML = equipmentHtml;
}

function editButtonClick(id) {
    currentId = id;
    action = "update";
    let equipment = equipmentList.find(equipment => equipment.id === id);
    inputText.value = equipment.nome;
    inputDate.value = equipment.data_fabricacao;
    inputPrice.value = equipment.preco_aquisicao;
    inputMaker.value = equipment.fabricante;
    inputNumber.value = equipment.numero_serie;
    overlay.style.display = "flex";
}

function removeButtonClick(id) {
    let isCertain = confirm("Você deseja remover este equipamento?\n(Deve remover chamados com esse equipamento antes.)");
    if (isCertain) {
        let executable = (data) => {
            console.log(data)
            startlist();
        };

        getJson(`equipamentos/remove/${id}`, executable);
    }
}

function getJson(header, executable) {
    try {
        fetch(route + header)
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
            body: JSON.stringify(object)
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
        equipmentList = data;
        updateEquipmentShowed();
    }
    getJson("equipamentos", executable);
}