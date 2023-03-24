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
    </div>
    `;
    messages.innerHTML = content + messages.innerHTML;
};

socketio.on('message', (data) => {
    createMessage(data.name, data.message, data.date);
})

message.addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
        sendMessage();
    }
});