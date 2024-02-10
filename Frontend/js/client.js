let socket;

document.addEventListener('DOMContentLoaded', function() {
    connectToServer();
});

function connectToServer() {
    const serverUrl = 'ws://localhost:8080';
    socket = new WebSocket(serverUrl);

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
        socket.addEventListener ('message', (event) => {
        const userExists = event.data[1];

        if (userExists == 'f') {
            logMessage('Invalid Username or Password');
        } else {
            const isManager = event.data[7];
            if (isManager == 't') {
                window.location.replace("../pages/manager_page.html");
            } else {
                window.location.replace("../pages/employee_page.html");
            }
        }
        });
    } else {
        logMessage('Not connected to the server');
    }

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
    const businessNumber = document.getElementById('businessNumber').value;
    if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
            request_id: 20,
            data: {username, password, businessNumber},
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
        return;
    }

    socket.addEventListener('message', function(event) {
        const data = JSON.parse(event.data);
        // Assuming data is an array of tuples containing employee ID and name
        const employees = data;

        // Generate HTML content dynamically
        let htmlContent = '<h1>Employees List</h1>';
        htmlContent += '<ul>';
        employees.forEach(employee => {
            htmlContent += `<li>${employee[0]}: ${employee[1]}</li>`;
        });
        htmlContent += '</ul>';

        // Open the HTML page in a new browser window
        const newWindow = window.open();
        newWindow.document.open();
        newWindow.document.write(htmlContent);
        newWindow.document.close();
    });
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