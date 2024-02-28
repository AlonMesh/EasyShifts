import React from 'react';
import EmployeeShifts from './EmployeeShifts';
import ScheduleBoard from "./ScheduleBoard";
import '../../css/ManagerSchedule.css';

function ManagerSchedule() {
    const employees = [
        {
            name: 'John Doe',
            request: 'Monday off'
        },

        {
            name: 'Jane Smith',
            request: 'Thursday off please'
        },

        {
            name: 'Mike Wilson',
            request: 'Schedule me for 3-11pm on Friday'
        },

        {
            name: 'Sarah Johnson',
            request: 'I need Tuesday off'
        },

        {
            name: 'Chris Brown',
            request: 'Can I work 8am-4pm on Saturday?'
        },

        {
            name: 'Amanda Miller',
            request: 'I need Sunday off'
        }
        // other employees
    ];

    return (
        <div className="manager-schedule">
            <div className="board-and-requests">
                <EmployeeShifts employees={employees}/>
                <ScheduleBoard shiftsPerDay={3}/>
            </div>
            <div className="buttons">
                <button>Save</button>
                <button>Revert</button>
                <button>Clean</button>
                <button>Publish</button>
            </div>
        </div>
    );
}

export default ManagerSchedule;