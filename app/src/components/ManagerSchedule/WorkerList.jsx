import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import '../../css/WorkerList.css';

const animatedComponents = makeAnimated();

function WorkerList({allWorkers, selectedWorkers, onSelect}) {
    console.log("WorkerList: ", allWorkers, selectedWorkers)

    const availableWorkers = allWorkers.filter(
        worker => !selectedWorkers.includes(worker)
    );

    const handleChange = (selected) => {
        selected.forEach(option => {
            onSelect(option.value);
        });
    }

    return (
        <Select
            className={"worker-list"}
            components={animatedComponents}
            isMulti
            options={availableWorkers.map(worker => ({value: worker, label: worker}))}
            onChange={handleChange}
        />
    );

}

export default WorkerList;