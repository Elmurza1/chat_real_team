// Функция для переподключения WebSocket
let socket;
function connectWebSocket() {
    socket = new WebSocket("ws://127.0.0.1:8000/ws/chat/");

    // Элементы DOM
    const chatMessages = document.getElementById("chat_messages");
    const chatForm = document.getElementById("chat_message_form");
    const chatInput = chatForm.querySelector("input[name='content']");

    // При успешном подключении к WebSocket
    socket.onopen = function () {
        console.log("WebSocket соединение открыто.");
    };

    // При закрытии WebSocket-соединения
    socket.onclose = function () {
        console.log("WebSocket соединение закрыто.");
        // Попробуем переподключиться через 5 секунд
        setTimeout(connectWebSocket, 5000);
    };

    // Функция для отправки сообщения
    function sendMessage(message) {
        if (socket.readyState === WebSocket.OPEN) {  // Проверка, что WebSocket открыт
            socket.send(JSON.stringify({"message": message}));
            addMessageToChat("Вы", message);  // Добавляем сообщение как "Вы"
            chatInput.value = "";  // Очищаем поле ввода
        } else {
            console.log("WebSocket не открыт или уже закрыт.");
        }
    }

    // Получение сообщения от сервера
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log("Сообщение от сервера:", data);

        if (data.message && !isDuplicateMessage(data.message)) {
            addMessageToChat("Собеседник", data.message);  // Добавляем сообщение от собеседника
        }
    };

    // Функция для проверки, дублируется ли сообщение
    function isDuplicateMessage(message) {
        const messages = chatMessages.querySelectorAll("li .message");
        for (let msg of messages) {
            if (msg.innerText.includes(message)) {
                return true;  // Сообщение найдено, оно дублируется
            }
        }
        return false;
    }

    // Обработчик отправки сообщения через форму
    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();  // Отмена стандартного отправления формы

        const message = chatInput.value.trim();
        if (message.length > 0) {
            sendMessage(message);  // Отправка сообщения через WebSocket
        }
    });

    // Функция добавления нового сообщения в чат
    function addMessageToChat(sender, message) {
        let messageElement = document.createElement("li");
        messageElement.classList.add("flex", "justify-end", "mb-4");

        messageElement.innerHTML = `
            <div class="message ${sender === "Вы" ? "sender" : "receiver"}">
                <strong>${sender}:</strong> ${message}
            </div>
        `;

        chatMessages.appendChild(messageElement);

        // Проверка, внизу ли чат, перед автоскроллом
        const isAtBottom = chatMessages.scrollHeight - chatMessages.scrollTop === chatMessages.clientHeight;
        if (isAtBottom) {
            chatMessages.scrollTop = chatMessages.scrollHeight;  // Автоскроллинг вниз
        }
    }
}

// Запуск соединения WebSocket при загрузке страницы
connectWebSocket();
