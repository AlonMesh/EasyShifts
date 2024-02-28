import React, {useEffect} from 'react';
import '../css/ManagerProfile.css';
import {SolarSettingsBoldDuotone} from "./Icons/SolarSettingsBoldDuotone";
import {UimSchedule} from "./Icons/UimSchedule";
import {FluentPeopleTeam20Filled} from "./Icons/Team";

const ManagerProfile = ({name = "Joe's Caffe", socket}) => {
    // Implement logic to send request for employee shifts using the existing socket
    useEffect(() => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            // Example request
            const request = {
                request_id: 50,
            };
            socket.send(JSON.stringify(request));
        } else {
            console.error('Socket connection is not available.');
        }
    }, [socket]);

    const createNewShifts = () => {
        // Implement logic to create new week shifts using the existing socket
        if (socket && socket.readyState === WebSocket.OPEN) {
            // Example request
            const request = {
                request_id: 80,
            };
            socket.send(JSON.stringify(request));
        } else {
            console.error('Socket connection is not available.');
        }
    };

    const getProfileRequest = () => {
        // Implement logic to send request to view employee profile using the existing socket
        if (socket && socket.readyState === WebSocket.OPEN) {
            // Example request
            const request = {
                request_id: 70,
            };
            socket.send(JSON.stringify(request));
        } else {
            console.error('Socket connection is not available.');
        }
    };

    const getEmployeesList = () => {
        // Implement logic to get list of employees using the existing socket
        if (socket && socket.readyState === WebSocket.OPEN) {
            // Example request
            const request = {
                request_id: 60,
            };
            socket.send(JSON.stringify(request));
        } else {
            console.error('Socket connection is not available.');
        }
    };

    return (
        <div className="manager-profile">
            <div className="profile-header">{name}' works management</div>

            <div className="menu">
                <a href="/manager-settings">
                    <SolarSettingsBoldDuotone className="icon" style={{width: '5em', height: '5em'}}/>
                    <br/>
                    Settings
                </a>

                <a href="/manager-schedule">
                    <UimSchedule className="icon" style={{width: '5em', height: '5em'}}/>
                    <br/>
                    Schedule
                </a>

                <a href="/managing-workers">
                    <FluentPeopleTeam20Filled className="icon" style={{width: '5em', height: '5em'}}/>
                    <br/>
                    Workers
                </a>
            </div>

            <div>
                <h1>Welcome!</h1>
                <h2>What would you like to do?</h2>
                <button onClick={createNewShifts}>Create new week shifts</button>
                <button onClick={getProfileRequest}>View my profile</button>
                <button onClick={getEmployeesList}>View my employees</button>
                <div id="log"></div>
                {/* Example HTML structure with a container for displaying profile information */}
                <div id="profileContainer"></div>
            </div>
        </div>
    );
};

export default ManagerProfile;
