import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const SignInShifts = ({ socket }) => {
  
    const [shiftsString, setShiftsString] = useState('')
    const [sent, setSent] = useState(false)

    const onSubmit = () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 40,
                data: {shiftsString},
            };
        socket.send(JSON.stringify(request));
        setSent(true)
        console.log("sent:", sent)
        }
    }



    return (
        <div>
        <h1>What is your availability next week?</h1>
        <textarea cols={65} rows={5} onChange={(e)=>{setShiftsString(e.currentTarget.textContent)}}/>
        <br/>
        <button onClick={() => onSubmit()}>submit</button>
        {sent&&<h1>Request for shifts has been submitted</h1>}
        {/* Link back to home page */}
        <Link to="/">Go back to home page</Link>
        </div>
    );
};

export default SignInShifts;

/*
<table id='table'>
        <thead>
            <tr>
                <th></th>
                <th>Sunday</th>
                <th>Monday</th>
                <th>Tuesday</th>
                <th>Wednesday</th>
                <th>Thursday</th>
                <th>Friday</th>
                <th>Saturday</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Morning</td>
                <td><input type="checkbox" id="1m"/></td>
                <td><input type="checkbox" id="2m"/></td>
                <td><input type="checkbox" id="3m"/></td>
                <td><input type="checkbox" id="4m"/></td>
                <td><input type="checkbox" id="5m"/></td>
                <td><input type="checkbox" id="6m"/></td>
                <td><input type="checkbox" id="7m"/></td>
            </tr>
            <tr>
                <td>Noon</td>
                <td><input type="checkbox" id="1n"/></td>
                <td><input type="checkbox" id="2n"/></td>
                <td><input type="checkbox" id="3n"/></td>
                <td><input type="checkbox" id="4n"/></td>
                <td><input type="checkbox" id="5n"/></td>
                <td><input type="checkbox" id="6n"/></td>
                <td><input type="checkbox" id="7n"/></td>
            </tr>
            <tr>
                <td>Evening</td>
                <td><input type="checkbox" id="1e"/></td>
                <td><input type="checkbox" id="2e"/></td>
                <td><input type="checkbox" id="3e"/></td>
                <td><input type="checkbox" id="4e"/></td>
                <td><input type="checkbox" id="5e"/></td>
                <td><input type="checkbox" id="6e"/></td>
                <td><input type="checkbox" id="7e"/></td>
            </tr>
        </tbody>
    </table>
*/
