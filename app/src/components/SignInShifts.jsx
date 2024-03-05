import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useSocket } from '../utils';

const SignInShifts = () => {

    const socket = useSocket(); // Call the useSocket hook directly

    const [shiftsString, setShiftsString] = useState('')

    const onSubmit = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 40,
                data: {shiftsString: shiftsString},
            };
            socket.send(JSON.stringify(request));
            console.log('Request for shifts has been submitted - ', request);
        }
    };


    return (
        <div>
        <h1>What is your availability next week?</h1>
        <textarea cols={65} rows={5} onChange={(e)=>{setShiftsString(e.currentTarget.textContent)}}/>
        <br/>
        <button onClick={() => onSubmit()}>submit</button>
        {/* Link back to home page */}
        <Link to="/">Go back to home page</Link>
        </div>
    );
};

export default SignInShifts;
