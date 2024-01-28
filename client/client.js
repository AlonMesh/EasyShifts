// client.js

const net = require('net');

const client = new net.Socket();

const PORT = 8080;
const HOST = '127.0.0.1';

client.connect(PORT, HOST, () => {
    console.log('Connected to server');

    // Sending a sample request (request ID 10 and data "Hello, server!")
    sendRequest(10, 'Hello, server!');
});

// Handle data received from the server
client.on('data', (data) => {
    console.log('Received from server:', data.toString());
});

// Handle the connection being closed
client.on('close', () => {
    console.log('Connection closed');
});

// Function to send a request to the server
function sendRequest(requestId, requestData) {
    // Convert the request ID to two bytes in big-endian order
    const requestIdBytes = Buffer.alloc(2);
    requestIdBytes.writeUInt16BE(requestId, 0);

    // Combine the request ID bytes and request data
    const requestDataBuffer = Buffer.concat([requestIdBytes, Buffer.from(requestData)]);

    // Send the request to the server
    client.write(requestDataBuffer);
}

// Handle any errors during the connection
client.on('error', (err) => {
    console.error('Error:', err.message);
});


// Handles first page's buttons:

function loginAsEmployee() {
    window.location.href = "pages/loginAsEmployee.html";
}

function loginAsManager() {
    window.location.href = "pages/loginAsManager.html";
}

function signUp() {
    window.location.href = "pages/signUp.html";
}


function employeeLogin(){

}




function handleLoginResponse(data) {
    console.log('Handling Login response:', data);
    // Implement your logic for handling the login response
}

function handleEmployeeSignInResponse(data) {
    console.log('Handling Employee Sign In response:', data);
    // Implement your logic for handling the employee sign-in response
}

function handleManagerSignInResponse(data) {
    console.log('Handling Manager Sign In response:', data);
    // Implement your logic for handling the manager sign-in response
}

function handleEmployeeShiftsResponse(data) {
    console.log('Handling Employee Shifts response:', data);
    // Implement your logic for handling the employee shifts response
}

function handleManagerShiftsResponse(data) {
    console.log('Handling Manager Shifts response:', data);
    // Implement your logic for handling the manager shifts response
}

function handleEmployeeListResponse(data) {
    console.log('Handling Employee List response:', data);
    // Implement your logic for handling the employee list response
}
