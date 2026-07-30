import DatasetSelector from "./DatasetSelector";
import ModelSelector from "./ModelSelector";
import "./ControlPanel.css";

export default function ControlPanel({

    datasets,
    models,

    selectedDataset,
    selectedModel,

    onDatasetChange,
    onModelChange

})
{

    return (

        <div className="control-panel">

            <div className="selectors">

                <DatasetSelector

                    datasets = {datasets}
                    selectedDataset = {selectedDataset}
                    onChange = {onDatasetChange}

                />

                <ModelSelector 

                    models = {models}
                    selectedModel = {selectedModel}
                    onChange = {onModelChange}

                />

                <div className="status-chip">

                    <span className="status-dot"></span>

                    Ready

                </div>

            </div>

        </div>

    );

}