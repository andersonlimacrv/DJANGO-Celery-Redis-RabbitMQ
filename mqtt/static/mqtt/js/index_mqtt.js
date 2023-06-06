// Função para adicionar uma mensagem à lista de mensagens
function addMessageToList(message) {
    const messageList = document.getElementById("message-list");
    const listItem = document.createElement("li");
    listItem.innerText = message;
    messageList.appendChild(listItem);
}

// Função para atualizar o status do MQTT
function updateMQTTStatus() {
    const statusElement = document.getElementById('mqtt_status');

    fetch('/mqtt_status/')
        .then(response => response.json())
        .then(data => {
            statusElement.innerText = data.status;
        });
}

// Função para receber as mensagens do MQTT
function receiveMQTTMessage(message) {
    addMessageToList(message);
}

// Atualiza o status do MQTT inicialmente
updateMQTTStatus();

// Atualiza o status do MQTT a cada segundo
setInterval(updateMQTTStatus, 1000);