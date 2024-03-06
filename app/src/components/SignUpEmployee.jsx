import React, {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';
import * as socket_object from '../utils'
import {useSocket} from '../utils';
import './../css/SignUpEmployee.css';

const SignUpEmployee = () => {
    const socket = useSocket(); // Call useSocket hook directly

    const [employeeUsername, setEmployeeUsername] = useState('');
    const [employeePassword, setEmployeePassword] = useState('');
    const [businessName, setBusinessName] = useState('');
    const [employeeName, setEmployeeName] = useState('');
    const [log, setLog] = useState('');

    const sendEmployeeSignUpRequest = () => {
        if (!socket) {
            console.error("Socket connection is not available.");
            return;
        }

        const requestData = {
            request_id: 20,
            data: {
                username: employeeUsername,
                password: employeePassword,
                businessName: businessName,
                employeeName: employeeName
            }
        };

        // Send sign-up request to the server using WebSocket
        socket.send(JSON.stringify(requestData));
    };

    useEffect(() => {
        if (socket) {
            // Handle response from the server
            const handleResponse = (event) => {
                const response = JSON.parse(event.data);
                const {success, message} = response.data;
                if (success) {
                    setLog(message);
                } else {
                    setLog('Sign up failed. Please try again.');
                }
            };

            socket.addEventListener('message', handleResponse);

            // Cleanup function
            return () => {
                socket.removeEventListener('message', handleResponse);
            };
        }
    }, [socket]);

    return (
        <div className="signup-employee-container">
            <div className="signup-employee-form">
                <h1>Employee Sign Up</h1>
                <label htmlFor="employeeUsername">Username:</label>
                <input
                    type="text"
                    id="employeeUsername"
                    name="employeeUsername"
                    value={employeeUsername}
                    onChange={(e) => setEmployeeUsername(e.target.value)}
                    required
                />
                <br/>
                <label htmlFor="employeePassword">Password:</label>
                <input
                    type="password"
                    id="employeePassword"
                    name="employeePassword"
                    value={employeePassword}
                    onChange={(e) => setEmployeePassword(e.target.value)}
                    required
                />
                <br/>
                <label htmlFor="businessName">Business Name:</label>
                <input
                    type="text"
                    id="businessName"
                    name="businessName"
                    value={businessName}
                    onChange={(e) => setBusinessName(e.target.value)}
                    required
                />
                <br/>
                <label htmlFor="employeeName">Name:</label>
                <input
                    type="text"
                    id="employeeName"
                    name="employeeName"
                    value={employeeName}
                    onChange={(e) => setEmployeeName(e.target.value)}
                    required
                />
                <br/>
                {/* Use Link component to navigate to employeeProfile */}
                <Link to="/employeeProfile">
                    <button type="button" onClick={sendEmployeeSignUpRequest}>Sign Up</button>
                </Link>
                <div id="log">{log}</div>
            </div>
        </div>
    );
};

export default SignUpEmployee;