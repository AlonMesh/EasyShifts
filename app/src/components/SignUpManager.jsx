import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {useSocket} from '../utils';


function SignUpManager() {
    const navigate = useNavigate();
    const socket = useSocket();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');

    const handleSignUpManager = () => {
        const isManager = 1;
        const isActive = 1;

        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 30,
                data: {username, password, isManager, isActive, name},
            };
            socket.send(JSON.stringify(request));
            navigate('/manager-profile');
        } else {
            console.log('Not connected to the server');
        }
    };

    return (
        <div className="signup-container">
            <div className="signup-form">
                <h2>Sign Up Manager</h2>
                <form>
                    <div>
                        <label htmlFor="managerUsername">Username:</label>
                        <input
                            type="text"
                            id="managerUsername"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <label htmlFor="managerPassword">Password:</label>
                        <input
                            type="password"
                            id="managerPassword"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <div>
                        <label htmlFor="name">Name:</label>
                        <input
                            type="text"
                            id="name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                    <button type="button" onClick={handleSignUpManager}>
                        Sign Up
                    </button>
                </form>
            </div>
        </div>
    );
}

export default SignUpManager;
