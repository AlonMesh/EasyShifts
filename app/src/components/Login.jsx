import React, { useState, useEffect } from 'react';
import { useSocket } from '../utils';
import ManagerProfile from './ManagerProfile';
import EmployeeProfile from './EmployeeProfile';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loggedIn, setLoggedIn] = useState(false);
    const [isManager, setIsManager] = useState(false);
    const socket = useSocket();

    const handleLogin = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 10,
                data: { username, password },
            };

            socket.send(JSON.stringify(request));
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.addEventListener('message', handleMessage);
            }
        } else {
            setError('Not connected to the server');
        }
    };

    const handleMessage = (event) => {
        if (event.data !== null && event.data !== undefined) {
            // event.data is not null or undefined, proceed with further processing
            console.log(event.data);
            const data = JSON.parse(event.data);
            const userExists = data['user_exists'];
            const isManager = data['is_manager'];

            if (userExists === false) {
                setError('Invalid Username or Password');
            } else {
                setIsManager(isManager === true);
                setLoggedIn(true);
            }
            socket.removeEventListener('message', handleMessage);
        } else {
            // Handle the case where event.data is null or undefined
            console.error('Received null or undefined data.');
        }
    };

    if (loggedIn) {
        return (
            <div>
                {isManager ? <ManagerProfile /> : <EmployeeProfile />}
            </div>
        );
    }

    return (
        <div>
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
            <br />
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <br />
            <button type="submit" onClick={handleLogin}>Log In</button>
            <div id="log">{error}</div>
        </div>
    );
}

export default Login;