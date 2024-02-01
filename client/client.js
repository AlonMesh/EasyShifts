// client.js

const WebSocket = require('ws');

const serverUrl = 'ws://localhost:8080';

const socket = new WebSocket(serverUrl);

// Connection opened
socket.addEventListener('open', (event) => {
    console.log('Connected to the server');

    // Example: Send a login request
    const loginRequest = {
        request_id: 10,
        data: 'Your login data here',
    };
    socket.send(JSON.stringify(loginRequest));
});

// Listen for messages from the server
socket.addEventListener('message', (event) => {
    console.log('Received:', event.data);
});

// Connection closed
socket.addEventListener('close', (event) => {
    console.log('Connection closed');
});

// Connection error
socket.addEventListener('error', (event) => {
    console.error('Error:', event);
});

// Example: Sending a request to the server
function sendEmployeeSigninRequest() {
    const employeeSigninRequest = {
        request_id: 20,
        data: 'Employee signin data here',
    };
    socket.send(JSON.stringify(employeeSigninRequest));
}

// Call the function to send a request when needed
// sendEmployeeSigninRequest();



// Functions for the first page's buttons:

function signUp() {
    // Moving to sign-up page
    window.location.href = "pages/signUp.html";
}


function login(){
    // send name and passwoed to server

    // if he is employee
    window.location.href = "pages/employee_page.html";
    // if he is manager
    window.location.href = "pages/manager_page.html";
}

/*
function login() {
    var username = document.getElementById("userName").value;
    var password = document.getElementById("password").value;

    // Add '10' before the name and password
}
*/