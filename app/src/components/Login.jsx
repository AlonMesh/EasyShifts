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

    useEffect(() => {
        const handleMessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Received data:', data);

            if (Array.isArray(data)) {
                const [userExists, isManager] = data;
                if (!userExists) {
                    setError('Invalid Username or Password');
                } else {
                    setIsManager(isManager);
                    setLoggedIn(true);
                }
            } else if (data.request_id === 70) {
                const { success, data: profileData } = data;
                if (!success) {
                    console.error('Failed to retrieve profile data');
                } else {
                    console.log('Profile Data:', profileData);
                    // Handle profile data as needed
                }
            } else {
                // Handle other types of responses if necessary
            }
        };

        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.addEventListener('message', handleMessage);
        }

        return () => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.removeEventListener('message', handleMessage);
            }
        };
    }, [socket]);

    const handleLogin = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 10,
                data: { username, password },
            };

            socket.send(JSON.stringify(request));
        } else {
            setError('Not connected to the server');
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
