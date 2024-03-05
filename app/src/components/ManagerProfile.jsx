import React, {useState} from 'react';
import '../css/ManagerProfile.css';
import {SolarSettingsBoldDuotone} from "./Icons/SolarSettingsBoldDuotone";
import {UimSchedule} from "./Icons/UimSchedule";
import {FluentPeopleTeam20Filled} from "./Icons/Team";
import {useSocket} from '../utils';
import ManagerSchedule from "./ManagerSchedule/ManagerSchedule";
import ManagerSettings from "./ManagerSettings";
import EmployeeListPage from "./EmployeeListPage";

const ManagerProfile = ({name = "Joe's Caffe"}) => {
    const socket = useSocket();
    const [showSettings, setShowSettings] = useState(false);
    const [showSchedule, setShowSchedule] = useState(false);
    const [showWorkers, setShowWorkers] = useState(false);

    const handleSettingsClick = () => {
        setShowSettings(!showSettings);
        setShowSchedule(false);
        setShowWorkers(false);
    };

    const handleScheduleClick = () => {
        setShowSettings(false);
        setShowSchedule(!showSchedule);
        setShowWorkers(false);
    };

    const handleWorkersClick = () => {
        setShowSettings(false);
        setShowSchedule(false);
        setShowWorkers(!showWorkers);
    };

    return (
        <div className="full-page">
            <div className="manager-profile">
                <div className="profile-header">{name}' works management</div>

                <div className="menu">
                    <div className="icon-wrapper" onClick={handleSettingsClick}>
                        {/* Replace with your Settings icon */}
                        <SolarSettingsBoldDuotone className="icon" style={{width: '5em', height: '5em'}}/>
                        <br/>
                        Settings
                    </div>

                    <div className="icon-wrapper" onClick={handleScheduleClick}>
                        {/* Replace with your Schedule icon */}
                        <UimSchedule className="icon" style={{width: '5em', height: '5em'}}/>
                        <br/>
                        Schedule
                    </div>

                    <div className="icon-wrapper" onClick={handleWorkersClick}>
                        {/* Replace with your Workers icon */}
                        <FluentPeopleTeam20Filled className="icon" style={{width: '5em', height: '5em'}}/>
                        <br/>
                        Workers
                    </div>
                </div>
            </div>

            {showSchedule && (
                <div className="submenu">
                    {/* Add submenu content for Schedule here */}
                    <ManagerSchedule socket={socket}/>
                </div>
            )}

            {showSettings && (
                <div className="submenu">
                    {/* Add submenu content for Settings here */}
                    <ManagerSettings socket={socket}/>
                </div>
            )}

            {showWorkers && (
                <div className="submenu">
                    {/* Add submenu content for Workers here */}
                    <EmployeeListPage socket={socket}/>
                </div>
            )}
        </div>
    );
};

export default ManagerProfile;