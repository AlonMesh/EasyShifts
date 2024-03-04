import Shift from './Shift';
import '../../css/ScheduleBoard.css';


function ScheduleBoard({partsCount, closedDays, startDate, allWorkers, assignedShifts}) {

    const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    const shiftNames = ['morning', 'evening', 'noon'];

    function getWorkers(date, part) {
        return assignedShifts.filter(worker => {
            return worker.shifts.some(shift => {
                const shiftDate = new Date(shift.shiftDate);
                const dayOfWeek = getDayName(shiftDate);

                console.log('known-shift:', shift);
                console.log('date:', dayOfWeek);
                console.log('part:', part);

                return dayOfWeek === date && shift.shiftPart === part;
            });
        }).map(worker => worker.name);
    }

    function getDayName(date) {
        const options = {weekday: 'long'};
        return date.toLocaleDateString('en-US', options).toLowerCase();
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
                                    date={day}
                                    part={shiftNames[i]}
                                    workers={getWorkers(day, shiftNames[i])}
                                    allWorkers={allWorkers}
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
