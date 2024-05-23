var socketio = io();
const messages = document.getElementById('messages');


function sendMessage() {
    const message = document.getElementById('message');
    if (message.value == "") return;
    socketio.emit("message", {data: message.value});
    message.value = "";
}


function createMessage(name, msg) {
    var content = "";

    if (name === username) {
        content = `
    
        <div class="message own-message">
            <div>
                ${msg}
            </div>
        </div>
        `;

    } else {
        content = `
        <div class="message">
            <div><small class="message-name">${name}</small></div>
            <div>
                ${msg}
            </div>
        </div>
        `;
    }



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