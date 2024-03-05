import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useSocket } from '../utils';

const SignInShifts = () => {

    const socket = useSocket();

    const [shiftsString, setShiftsString] = useState('')
    const [requestSubmitted, setRequestSubmitted] = useState(false);

    const onSubmit = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 40,
                data: {shiftsString},
            };
            socket.send(JSON.stringify(request));
            console.log('Request for shifts has been submitted')
            setRequestSubmitted(true);
        }
    };


    return (
        <div>
        <h1>What is your availability next week?</h1>
        <textarea 
          cols={65} 
          rows={5}  
          required
          defaultValue={shiftsString} 
          onChange={(e)=>{setShiftsString(e.target.value)}} 
        />
        <br/>
        <button onClick={() => onSubmit()}>submit</button>
        {requestSubmitted && <p>Your request has been submitted</p>}
        {/* Link back to home page */}
        <Link to="/">Go back to home page</Link>
        </div>
    );
};

export default SignInShifts;
