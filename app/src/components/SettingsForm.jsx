import {useState} from "react";
import Select from "react-select";
import {useSocket} from "../utils";

export default function SettingsForm() {
    const socket = useSocket();
    const [shifts, setShifts] = useState(null);
    const [days, setDays] = useState(null);

    const shiftOptions = [
        {value: 1, label: '1'},
        {value: 2, label: '2'},
        {value: 3, label: '3'}
    ];

    const dayOptions = [
        {value: 'sunday', label: 'Sunday'},
        {value: 'monday', label: 'Monday'},
        {value: 'tuesday', label: 'Tuesday'},
        {value: 'wednesday', label: 'Wednesday'},
        {value: 'thursday', label: 'Thursday'},
        {value: 'friday', label: 'Friday'},
        {value: 'saturday', label: 'Saturday'}
    ];

    function handleSubmit(e) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            // save days to const, if days is null or empty, set to empty array
            const days = days ? days : [];
            const request = {
                request_id: 991,
                data: {
                    number_of_shifts_per_day: shifts.value,
                    closed_days: days.map(day => day.value),
                },
            };

            socket.send(JSON.stringify(request));
            console.log("Sent to server: ", request);
        } else {
            console.error("Socket not connected");
        }

        e.preventDefault();
        alert('Saved!');
    }

    return (
        <form onSubmit={handleSubmit}>
            <div style={{textAlign: 'left', marginBottom: '0px'}}>
                <label>Shifts per day</label>
            </div>
            <Select
                options={shiftOptions}
                value={shifts}
                onChange={setShifts}
                placeholder="Pick shift count"
            />

            <div style={{textAlign: 'left', marginBottom: '0 px', marginTop: '10 px'}}>
                <label>Closed days</label>
            </div>
            <Select
                options={dayOptions}
                value={days}
                onChange={setDays}
                placeholder="Pick closed days"
                isMulti
                closeMenuOnSelect={false}
            />

            <button>Save</button>
        </form>
    );
}
