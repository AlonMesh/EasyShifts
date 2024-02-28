import {useState} from "react";
import Select from "react-select";

export default function SettingsForm() {
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
