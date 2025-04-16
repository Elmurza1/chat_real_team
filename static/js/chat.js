let socket;

function connectWebSocket() {
    if (socket) {
        socket.close();
    }

    const chatMessages = document.getElementById("chat_messages");
    const chatForm = document.getElementById("chat_message_form");
    const chatInput = chatForm.querySelector("input[name='content']");

    // Получаем ID собеседника из URL (можно передавать через шаблон Django)
    console.log("🔍 Receiver ID:", receiverId);
    console.log(`🔗 WebSocket URL: ws://${window.location.host}/ws/chat/${receiverId}/`);

    // Проверяем, что receiverId не пустой
    if (!receiverId) {
        console.error("❌ Ошибка: receiverId пустой! Проверь URL.");
        return; // Останавливаем выполнение функции
    }

    // Создаём WebSocket соединение с user_id
    socket = new WebSocket(`ws://${window.location.host}/ws/chat/${receiverId}/`);

    socket.onopen = function () {
        console.log("✅ WebSocket соединение установлено.");
    };

    socket.onclose = function (event) {
        console.warn(`⚠️ WebSocket закрыт (код ${event.code}, причина: ${event.reason})`);
        socket = null;

        // Если соединение закрыто по ошибке (не код 1000), пытаемся переподключиться
        if (event.code !== 1000) {
            console.log("🔄 Переподключение через 5 секунд...");
            setTimeout(connectWebSocket, 5000);
        }
    };

    socket.onerror = function (error) {
        console.error("❌ Ошибка WebSocket:", error);
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log("📩 Получено сообщение от сервера:", data);

        // 📦 Обработка непрочитанных сообщений от конкретного пользователя
        // 📦 Обработка непрочитанных сообщений от конкретного пользователя
        if (data.type === "unread_count") {
            updateUnreadBadge(data.sender_id, data.count); // Обновим бейдж
        }



        if (data.message) {
            addMessageToChat(data.sender, data.message);
        }
    };

    function sendMessage(message) {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            console.log("❌ WebSocket соединение закрыто. Сообщение не отправлено.");
            return;
        }

        socket.send(JSON.stringify({ "message": message }));
        addMessageToChat("Вы", message);
        chatInput.value = "";
    }

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const message = chatInput.value.trim();
        if (message.length > 0) {
            sendMessage(message);
        }
    });

    // 📌 Обновляем счетчик рядом с именем юзера
    function updateUnreadBadge(senderId, count) {
        const badge = document.getElementById(`badge-${senderId}`);
        if (badge) {
            badge.innerText = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }


    function addMessageToChat(sender, message) {
        const messageElement = document.createElement("li");
        messageElement.classList.add("flex", "justify-end", "mb-4");

        messageElement.innerHTML = `
            <div class="message ${sender === "Вы" ? "sender" : "receiver"}">
                <strong>${sender}:</strong> ${message}
            </div>
        `;

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function loadUnreadCounts() {
    fetch('/get-unread-counts/')
        .then(response => response.json())
        .then(data => {
            for (let user in data) {
                const badge = document.getElementById(`badge-${user}`);
                if (badge) {
                    badge.innerText = data[user];
                    badge.style.display = data[user] > 0 ? 'inline-block' : 'none';
                }
            }
        });
}

// вызывать при загрузке
loadUnreadCounts();

// вызывать при открытии чата
function markMessagesAsRead(username) {
    fetch(`/mark-as-read/${username}/`)
        .then(() => loadUnreadCounts());
}


// Запускаем WebSocket при загрузке страницы
window.onload = () => {
    connectWebSocket();
};
