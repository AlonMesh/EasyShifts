import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useSocket } from '../utils';

const SignInShifts = () => {
  
    const socket = useSocket(); // Call the useSocket hook directly
    const [checkboxes, setCheckboxes] = useState(Array(21).fill(false));

    const shifts = ['Morning', 'Noon', 'Evening'];
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    const handleCheckboxChange = (index) => {
        setCheckboxes((prevCheckboxes) => {
        const newCheckboxes = [...prevCheckboxes];
        newCheckboxes[index] = !newCheckboxes[index];
        return newCheckboxes;
        });
    };

    const handleSubmit = () => {
        let resultString = '';
        daysOfWeek.forEach((day, dayIndex) => {
            shifts.forEach((shift, shiftIndex) => {
                const checkboxIndex = dayIndex * shifts.length + shiftIndex;
                resultString += `${dayIndex + 1}${shift.charAt(0).toLowerCase()}-${checkboxes[checkboxIndex] ? 't' : 'f'}_`;
            });
        });
        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 40,
                data: {resultString},
            };
        socket.send(JSON.stringify(request));
        }
    }



    return (
        <div>
        <h1>What is your availability next week?</h1>
        <table border="1">
            <thead>
            <tr>
                <th></th>
                {daysOfWeek.map((day) => (
                <th key={day} style={{ padding: '10px' }} >{day}</th>
                ))}
            </tr>
            
            </thead>
            <tbody>
            {shifts.map((shift) => (
                <tr key={shift}>
                <td>{shift}</td>
                {Array(7)
                    .fill(0)
                    .map((_, dayIndex) => (
                    <td key={dayIndex}>
                        <input
                        type="checkbox"
                        checked={checkboxes[dayIndex * 3 + shifts.indexOf(shift)]}
                        onChange={() => handleCheckboxChange(dayIndex * 3 + shifts.indexOf(shift))}
                        />
                    </td>
                    ))}
                </tr>
            ))}
            </tbody>
        </table>
        <button onClick={handleSubmit } style={{ display: 'block', margin: '20px auto', fontSize: '16px' }} >Submit</button>

        {/* Link back to home page */}
        <Link to="/">Go back to home page</Link>
        </div>
    );
};

export default SignInShifts;
