var socketio = io();
const messages = document.getElementById('messages');


function sendMessage() {
    const message = document.getElementById('message');
    if (message.value == "") return;
    socketio.emit("message", {data: message.value});
    message.value = "";
}


function createMessage(name, msg) {
    const content = `
    <div>
        <span>
            <strong>${name}</strong>: ${msg}
        </span>
        <span class="muted">
            ${new Date().toLocaleString()}
        </span>
    </div>
    `;
    messages.innerHTML += content;
};

socketio.on('message', (data) => {
    createMessage(data.name, data.message);
})

message.addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
        sendMessage();
    }
});