import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import '../../css/WorkerList.css';

const animatedComponents = makeAnimated();

function WorkerList({allWorkers, selectedWorkers, onSelect}) {

    const availableWorkers = allWorkers.filter(
        worker => !selectedWorkers.includes(worker.name)
    );

    const handleChange = (selected) => {
        selected.forEach(option => {
            onSelect(option.value);
        });
    }

    return (
        <Select
            className={"worker-list"}
            closeMenuOnSelect={false}
            components={animatedComponents}
            isMulti
            options={availableWorkers.map(worker => ({value: worker.name, label: worker.name}))}
            onChange={handleChange}
        />
    );

}

export default WorkerList;