import React from 'react';
import EmployeeShifts from './EmployeeShifts';
import ScheduleBoard from "./ScheduleBoard";
import '../../css/ManagerSchedule.css';

const allWorkers_const = [
                                        {name: "John Doe"},
                                        {name: "Jane Smith"},
                                        {name: "Mike Wilson"},
                                        {name: "Sarah Johnson"},
                                        {name: "Chris Brown"},
                                        {name: "Amanda Miller"}]


const employees_const = [
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

const assignedShifts_const = [
    {
        name: 'John Doe',
        shifts: [
            {date: 'Monday', part: 'Part 1'},
            {date: 'Tuesday', part: 'Part 2'}
        ]
    },
    {
        name: 'Jane Smith',
        shifts: [
            {date: 'Monday', part: 'Part 2'},
            {date: 'Tuesday', part: 'Part 1'}
        ]
    },
    {
        name: 'Mike Wilson',
        shifts: [
            {date: 'Monday', part: 'Part 1'},
            {date: 'Tuesday', part: 'Part 2'}
        ]
    },
    {
        name: 'Sarah Johnson',
        shifts: [
            {date: 'Monday', part: 'Part 2'},
            {date: 'Wednesday', part: 'Part 1'}
        ]
    },
    {
        name: 'Chris Brown',
        shifts: []
    },
    {
        name: 'Amanda Miller',
        shifts: []
    }
];

const startDate_const = new Date('2024-02-18')
const preferences_const = [2, ["Sunday", "Friday"]]


function ManagerSchedule({employees = employees_const, preferences = preferences_const, startDate = startDate_const}, allWorkers = allWorkers_const, assignedShifts = assignedShifts_const) {

    return (
            <div className="manager-schedule">
                <div className="board-and-requests">
                    <EmployeeShifts employees={employees}/>
                    <ScheduleBoard
                        partsCount={preferences[0]} // number of parts
                        closedDays={preferences[1]} // closed days
                        startDate={startDate}
                        allWorkers={allWorkers}
                        assignedShifts={assignedShifts}
                    />
                </div>

                <div className="buttons">
                    <button>Save</button>
                    <button>Clean</button>
                    <button>Publish</button>
                </div>
            </div>
    );
}

export default ManagerSchedule;