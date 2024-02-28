import Shift from './Shift';
import '../../css/ScheduleBoard.css';


function ScheduleBoard({partsCount, closedDays, startDate, allWorkers, assignedShifts}) {

    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    function getWorkers(date, part) {
        return assignedShifts.filter(worker => {
            return worker.shifts.some(shift => {
                return shift.date === date && shift.part === part;
            });
        }).map(worker => worker.name);
    }

    function getDate(i) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        return date.getDate() + '-' + (date.getMonth() + 1) + '-' + date.getFullYear();
    }


    return (
        <table className="schedule-board">
            <thead>
            <tr>
                {days.map((day, i) => (
                    <th key={day}>{day}
                        <span> {getDate(i)} </span>
                    </th>
                ))}
            </tr>
            </thead>
            <tbody>
            {[...Array(partsCount)].map((_, i) => (
                <tr key={i}>
                    {days.map(day => (
                        <td key={day}>
                            {closedDays.includes(day) ? (
                                    <div className="closed-day">Closed</div>
                                ) :
                                <Shift
                                    workplaceId="123"
                                    date={day}
                                    part={`Part ${i + 1}`}
                                    workers={getWorkers(day, `Part ${i + 1}`)}
                                    allWorkers={[
                                        {name: "John Doe"},
                                        {name: "Jane Smith"},
                                        {name: "Mike Wilson"},
                                        {name: "Sarah Johnson"},
                                        {name: "Chris Brown"},
                                        {name: "Amanda Miller"}
                                    ]
                                    }
                                    workersShifts={assignedShifts}
                                />
                            }

                        </td>
                    ))}
                </tr>
            ))}
            </tbody>
        </table>
    );
}

export default ScheduleBoard;
