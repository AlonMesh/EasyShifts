let socket;

document.addEventListener('DOMContentLoaded', function() {
    // Connect to the server when the document is ready
    connectToServer();
});


function connectToServer() {
    const serverUrl = 'ws://localhost:8080';
    socket = new WebSocket(serverUrl);

    socket.addEventListener('message', (event) => {
        logMessage(`Received: ${event.data}`);
    });

    socket.addEventListener('close', (event) => {
        logMessage('Connection closed');
    });

    socket.addEventListener('error', (event) => {
        logMessage(`Error: ${event}`);
    });
}

function redirectToLogin() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const loginRequest = {
            request_id: 10,
            data: 'Your login data here',
        };
        socket.send(JSON.stringify(loginRequest));
        logMessage('Sent Login Request');
    } else {
        logMessage('Not connected to the server');
    }
}

function redirectToSignin() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const loginRequest = {
            request_id: 20,
            data: 'Your sign in data here',
        };
        socket.send(JSON.stringify(loginRequest));
        logMessage('Sent Sign in Request');
    } 
    else {
        logMessage('Not connected to the server');
    }
}

function logMessage(message) {
    const logDiv = document.getElementById('log');
    const logEntry = document.createElement('div');
    logEntry.textContent = message;
    logDiv.appendChild(logEntry);
}
