let notificationSocket = new WebSocket(`ws://${window.location.host}/ws/notifications/`);

notificationSocket.onopen = function () {
    console.log("🔔 WebSocket для уведомлений подключен.");
};

notificationSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.unread_count !== undefined) {
        updateUnreadCount(data.unread_count);
    }

    if (data.type === "new_message") {
        console.log(`📩 Новое сообщение от ${data.sender}: ${data.message}`);
        updateUnreadCount(data.unread_count);
    }
};

function updateUnreadCount(count) {
    const badge = document.getElementById("unread_messages_badge");
    if (count > 0) {
        badge.innerText = count;
        badge.style.display = "inline";  // Добавляем это
    } else {
        badge.innerText = "0";  // Добавляем это
        badge.style.display = "inline";  // Добавляем это
    }
}


