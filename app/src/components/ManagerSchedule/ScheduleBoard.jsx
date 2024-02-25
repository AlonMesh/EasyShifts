import Shift from './Shift';
import '../../css/ScheduleBoard.css';

function ScheduleBoard({parts = 2, startDate = new Date('2024-02-18')}) {

    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

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
            {[...Array(parts)].map((_, i) => (
                <tr key={i}>
                    {days.map(day => (
                        <td key={day}>
                            <Shift
                                workplaceId="123"
                                date={day}
                                part={`Part ${i + 1}`}
                                workers={["John Doe", "Jane Smith"]}
                                allWorkers = {[
                                    {name: "John Doe"},
                                    {name: "Jane Smith"},
                                    {name: "Mike Wilson"},
                                    {name: "Sarah Johnson"},
                                    {name: "Chris Brown"},
                                    {name: "Amanda Miller"}
                                ]
                            }
                            />
                        </td>
                    ))}
                </tr>
            ))}
            </tbody>
        </table>
    );

}

export default ScheduleBoard;
