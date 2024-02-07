let socket;

document.addEventListener('DOMContentLoaded', function() {
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
    window.location.href = "pages/login.html";
}

function redirectToSignUp() {
    window.location.href = "pages/sign_up.html";
}

function redirectToManagerSignUp() {
    window.location.replace("../pages/manager_sign_up.html");
}

function redirectToEmployeeSignUp() {
    window.location.replace("../pages/employee_sign_up.html");
}

function redirectToSignInShifts() {
    window.location.replace("../pages/sign_in_shifts.html");
}

function sendLoginRequest() { // ORI Ekshtein
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 10,
            data: {username, password},
        };
        socket.send(JSON.stringify(request));
    } else {
        logMessage('Not connected to the server');
    }

    // ori, you need to get from server here a response that tells if this user is manager or employee
    // if manager, use  -  window.location.replace("../pages/manager_page.html");
    // if employee, use - window.location.replace("../pages/employee_page.html");

    // and if user doesn't exist, use - logMessage('invalid Username or Password'); you can copy it..
}

function sendManagerSignUpRequest() { // ALON
    const username = document.getElementById('managerUsername').value;
    const password = document.getElementById('managerPassword').value;
    const email = document.getElementById('managerEmail').value;
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 30,
            data: {username, password, email},
        };
        socket.send(JSON.stringify(request));
    } else {
        logMessage('Not connected to the server');
    }
    // alon - you need to add here all of the details in manager signup and add it to the request struct
    window.location.replace("../pages/manager_page.html");
}

function sendEmployeeSignUpRequest() { // SHOVAL
    const username = document.getElementById('employeeUsername').value;
    const password = document.getElementById('employeePassword').value;
    const email = document.getElementById('employeeEmail').value;
    const businessNumber = document.getElementById('businessNumber').value;
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 20,
            data: {username, password, email, businessNumber},
        };
        socket.send(JSON.stringify(request));
    } else {
        logMessage('Not connected to the server');
    }
    window.location.replace("../pages/employee_page.html");
}

function getProfileRequest() { // WHO ENDS HERE/HIS PART FIRST
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 70,
        };
        socket.send(JSON.stringify(request));
    } else {
        logMessage('Not connected to the server');
    }
}

function getEmployeesList() { // ORI
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 60,
        };
        socket.send(JSON.stringify(request));
    } else {
        logMessage('Not connected to the server');
    }

    // ori - you need to get from server an html file with employees list in it.
    // then, use - window.location.replace("..."); to show it to user
}

function sendShiftRequest() { // NETA
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 40,
            // neta you need to add here the shifts in format that will be comfortable for you to read in the server.
        };
        socket.send(JSON.stringify(request));
    } else {
        logMessage('Not connected to the server');
    }
}

function getEmployeesShiftsRequest() { // HALEL
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 50,
        };
        socket.send(JSON.stringify(request));
    } else {
        logMessage('Not connected to the server');
    }
}

function logMessage(message) {
    const logDiv = document.getElementById('log');
    const logEntry = document.createElement('div');
    logEntry.textContent = message;
    logDiv.appendChild(logEntry);
}
