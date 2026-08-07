export default function DatasetSelector({
    datasets,
    selectedDataset,
    onChange
}) {

    return (

        <div className="control-group">

            <label className="control-label">
                Dataset
            </label>

            <select 
                className = "select-box"
                value = {selectedDataset}
                onChange = {(e) => onChange(e.target.value)}
            >

                {datasets.map(dataset => (

                    <option 
                        key = {dataset.dataset_name}
                        value = {dataset.dataset_name}
                    >
                        {dataset.dataset_name.replaceAll("_", " ")}
                    </option>

                ))}

            </select>

        </div>
    );
}