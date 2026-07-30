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
                        key = {dataset}
                        value = {dataset}
                    >
                        {dataset.replaceAll("_", " ")}
                    </option>

                ))}

            </select>

        </div>
    );
}