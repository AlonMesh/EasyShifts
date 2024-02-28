import SettingsForm from "./SettingsForm";
import React, {useState} from "react";
import "../css/ManagerSetting.css";
import DateTime from 'react-datetime';
import 'react-datetime/css/react-datetime.css';


export default function ManagerSettings() {

    function handleSubmit(event) {
        event.preventDefault();
        alert("Start Time: " + startTime + "\nEnd Time: " + endTime);
    }

    const [startTime, setStartTime] = useState(new Date());
    const [endTime, setEndTime] = useState(new Date());

    return (
        <div>
            <div className="setting-box">
                <div className="title-box">Preferences</div>
                <div className="selects-container">
                    <SettingsForm className="settings-form"/>
                </div>

                <div className="setting-box">
                    <div className="container">
                        <div className="title-box">Schedule Window</div>
                        <form onSubmit={handleSubmit}>
                            <label style={{fontWeight: 'bold', color: "GrayText", textAlign: 'left'}}>Start Time:</label>
                            <DateTime inputProps={{className: "datetime"}}
                                value={startTime}
                                onChange={setStartTime}
                            />

                            <label style={{fontWeight: 'bold', color: "GrayText", textAlign: 'left'}}>End Time:</label>
                            <DateTime inputProps={{className: "datetime"}}
                                value={endTime}
                                onChange={setEndTime}
                            />
                            <button type="submit" className="btn btn-primary" style={{marginTop: '10px'}}>Save</button>
                        </form>
                    </div>

                </div>
            </div>
        </div>
    );
}