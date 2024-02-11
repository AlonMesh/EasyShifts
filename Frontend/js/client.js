let socket;

/**
 * Event listener for the 'DOMContentLoaded' event.
 * Establishes a connection to the server and adds a global message event listener.
 */
document.addEventListener('DOMContentLoaded', function() {
    connectToServer();

    /**
     * Event listener for incoming messages on the WebSocket connection.
     * Parses the received JSON data and handles the corresponding response based on the request ID.
     *
     * @param {Event} event - The event object representing the incoming message.
     *
     * @example
     * // Example response object format:
     * // { request_id: 70, success: true, data: { /* profile data } } */
    socket.addEventListener('message', function(event) {
        const response = JSON.parse(event.data);

        // Check the request ID and handle the corresponding response
        switch (response.request_id) {
            case 70:
                handleProfileResponse(response);
                break;

            // Add more cases as needed
        }
    });
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

/**
 * Handles the response received for a profile request.
 *
 * @param {Object} response - The response object from the server.
     * @param {boolean} response.success - Indicates whether the request was successful.
     * @param {Object} response.data - The profile data received from the server.
 */
function handleProfileResponse(response) {
    // Check if the response object is defined
    if (response) {
        console.log('Response: ', response);
        // Check if the response indicates success or failure
        if (response.success) {
            const profileData = response.data;
            // You can now work with the profileData in your frontend
            console.log('Received profile data:', profileData);
            // Call a function to update the UI
            updateProfileUI(profileData);
        } else {
            logMessage('Failed to retrieve profile data');
        }
    } else {
        logMessage('Invalid response received');
    }
}

// Function to update the UI with profile data
// function updateProfileUI(profileData) {
//     // Debugging: Log the element IDs
//     console.log('Profile data:', profileData)
//     console.log('userName element:', profileData.username);
//     console.log('workplaceName element:', profileData.workplace_name);
//     console.log('future_shifts element:', profileData.future_shifts);
//     console.log('future_shifts   elements:', formatShifts(profileData.future_shifts));
//
//     // Update the UI with the profile data
//     document.getElementById('userName').innerText = profileData.username;
//     document.getElementById('workplaceName').innerText = profileData.workplace_name;
//     document.getElementById('Shifts').innerText = formatShifts(profileData.future_shifts);
// }

// Example function to format shifts
function formatShifts(shifts) {
    // Implement your logic to format shifts as needed
    // For example, join the shifts array into a string
    return shifts.join(', ');
}

function updateProfileUI(profileData) {
    // Update the UI with the profile data
    const profileContainer = document.getElementById('profileContainer');

    // Remove existing profile elements if any
    profileContainer.innerHTML = '';

    // Display specific fields manually
    const usernameElement = document.createElement('p');
    usernameElement.innerText = `Username: ${profileData.username}`;
    profileContainer.appendChild(usernameElement);

    const workplaceNameElement = document.createElement('p');
    workplaceNameElement.innerText = `Workplace: ${profileData.workplace_name}`;
    profileContainer.appendChild(workplaceNameElement);

    const shiftsElement = document.createElement('p');
    shiftsElement.innerText = `Future Shifts:`;
    profileContainer.appendChild(shiftsElement);

        // Display details of all shifts
    if (profileData.future_shifts.length > 0) {
        profileData.future_shifts.forEach(shift => {
            const shiftDetailsElement = document.createElement('p');
            shiftDetailsElement.innerText = `Shift ID: ${shift.id} | Shift Date: ${shift.shiftDate} | Shift Part: ${shift.shiftPart} | Workplace ID: ${shift.workPlaceID}\n \n`;

            // Display workers for the shift
            if (shift.workers && shift.workers.length > 0) {
                shiftDetailsElement.innerText += '\nWorkers:';
                shift.workers.forEach(worker => {
                    shiftDetailsElement.innerText += `\t- ${worker}`;
                });
            } else {
                shiftDetailsElement.innerText += '\nNo workers for this shift.';
            }


            // Add any additional fields you want to display for each shift

            profileContainer.appendChild(shiftDetailsElement);
        });
    } else {
        // Handle the case when there are no shifts
        const noShiftsElement = document.createElement('p');
        noShiftsElement.innerText = 'No upcoming shifts.';
        profileContainer.appendChild(noShiftsElement);
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
