import React, {useEffect} from 'react';
import '../css/ManagerProfile.css';
import {SolarSettingsBoldDuotone} from "./Icons/SolarSettingsBoldDuotone";
import {UimSchedule} from "./Icons/UimSchedule";
import {FluentPeopleTeam20Filled} from "./Icons/Team";

const ManagerProfile = ({name = "Joe's Caffe", socket}) => {

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
        </div>
    );
};

export default ManagerProfile;
