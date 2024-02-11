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

function sendLoginRequest() { // ORI
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
    const isManager = 1;
    const isActive = 1;
    const name = document.getElementById('name').value;
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 30,
            data: {username, password, isManager, isActive, name},
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
    const name = document.getElementById('name').value;
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 20,
            data: {username, password, email, name},
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
    let shiftsString = '';
    // Go over checkboxes of each day and shift to create the shiftsString
    for (let day of ['1', '2', '3', '4', '5', '6', '7']) {
        for (let shift of ['m', 'n', 'e']) {
            const checkbox = document.getElementById(`${day}${shift}`);
            const isChecked = checkbox.checked ? 't' : 'f';
            shiftsString += `${day}${shift}-${isChecked}_`;
        }
    }
    // Remove the trailing underscore
    shiftsString = shiftsString.slice(0, -1);
    var currentDate = new Date();
    // Send time and shifts to server
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 40,
            data: {currentDate, shiftsString},
        };
        socket.send(JSON.stringify(request));
        document.getElementById('result').innerHTML = "Request for shifts has been submitted";
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
