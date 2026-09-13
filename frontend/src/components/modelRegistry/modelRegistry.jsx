import { useEffect, useState } from "react";

import {
    getModelVersions,
    setProductionModel
} from "../../services/registryService";

import { getSavedModels } from "../../services/analyticsService";

import "./ModelRegistry.css";


export default function ModelRegistry() {

    const [datasets, setDatasets] = useState([]);
    const [models, setModels] = useState([]);

    const [selectedDataset, setSelectedDataset] = useState("");
    const [selectedModel, setSelectedModel] = useState("");

    const [registry, setRegistry] = useState(null);

    const [loading, setLoading] = useState(false);
    const [updating, setUpdating] = useState(false);

    const [error, setError] = useState("");


    // Load datasets and models
    useEffect(() => {

        getSavedModels()
            .then(data => {

                const datasetList = data.datasets || [];

                setDatasets(datasetList);

                if (datasetList.length > 0) {

                    setSelectedDataset(
                        datasetList[0].dataset_name
                    );

                }

            })
            .catch(err => {

                console.error(err);

                setError(
                    "Failed to load datasets."
                );

            });

    }, []);


    // Update models when dataset changes
    useEffect(() => {

        if (!selectedDataset) return;

        const datasetInfo = datasets.find(
            dataset =>
                dataset.dataset_name === selectedDataset
        );

        if (!datasetInfo) return;

        const modelList = datasetInfo.models || [];

        const modelNames = modelList.map(
            model => model.model_name
        );

        setModels(modelNames);

        if (modelNames.length > 0) {

            setSelectedModel(
                modelNames[0]
            );

        }

    }, [selectedDataset, datasets]);


    // Load registry
    useEffect(() => {

        if (
            !selectedDataset ||
            !selectedModel
        ) return;

        loadRegistry();

    }, [
        selectedDataset,
        selectedModel
    ]);


    async function loadRegistry() {

        try {

            setLoading(true);

            setError("");

            const data =
                await getModelVersions(
                    selectedDataset,
                    selectedModel
                );

            console.log(
                "Registry:",
                data
            );

            setRegistry(data);

        }

        catch (err) {

            console.error(err);

            setError(
                "Failed to load model registry."
            );

            setRegistry(null);

        }

        finally {

            setLoading(false);

        }

    }


    async function handleSetProduction(
        version
    ) {

        try {

            setUpdating(true);

            await setProductionModel(
                selectedDataset,
                selectedModel,
                version
            );

            await loadRegistry();

        }

        catch (err) {

            console.error(err);

            alert(
                "Failed to update production model."
            );

        }

        finally {

            setUpdating(false);

        }

    }


    return (

        <div className="model-registry">

            <div className="registry-header">

                <div>

                    <h1>
                        🧠 Model Registry
                    </h1>

                    <p>
                        Manage model versions and production deployments.
                    </p>

                </div>

            </div>


            {/* CONTROLS */}

            <div className="registry-controls">

                <div className="registry-control">

                    <label>
                        Dataset
                    </label>

                    <select
                        value={selectedDataset}
                        onChange={(e) =>
                            setSelectedDataset(
                                e.target.value
                            )
                        }
                    >

                        {
                            datasets.map(
                                dataset => (

                                    <option
                                        key={
                                            dataset.dataset_name
                                        }
                                        value={
                                            dataset.dataset_name
                                        }
                                    >

                                        {
                                            dataset.dataset_name
                                        }

                                    </option>

                                )
                            )
                        }

                    </select>

                </div>


                <div className="registry-control">

                    <label>
                        Model
                    </label>

                    <select
                        value={selectedModel}
                        onChange={(e) =>
                            setSelectedModel(
                                e.target.value
                            )
                        }
                    >

                        {
                            models.map(
                                model => (

                                    <option
                                        key={model}
                                        value={model}
                                    >

                                        {model}

                                    </option>

                                )
                            )
                        }

                    </select>

                </div>


                <button
                    className="refresh-button"
                    onClick={loadRegistry}
                >

                    ↻ Refresh

                </button>

            </div>


            {/* ERROR */}

            {
                error && (

                    <div className="registry-error">

                        {error}

                    </div>

                )
            }


            {/* LOADING */}

            {
                loading && (

                    <div className="registry-loading">

                        Loading model versions...

                    </div>

                )
            }


            {/* REGISTRY TABLE */}

            {
                !loading &&
                registry &&
                registry.versions &&
                registry.versions.length > 0 && (

                    <div className="registry-table-container">

                        <table className="registry-table">

                            <thead>

                                <tr>

                                    <th>
                                        Version
                                    </th>

                                    <th>
                                        Score
                                    </th>

                                    <th>
                                        Status
                                    </th>

                                    <th>
                                        Action
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {
                                    registry.versions.map(
                                        version => {

                                            const isProduction =
                                                registry.production ===
                                                version.version;

                                            return (

                                                <tr
                                                    key={
                                                        version.version
                                                    }
                                                >

                                                    <td>

                                                        <strong>

                                                            {
                                                                version.version
                                                            }

                                                        </strong>

                                                    </td>


                                                    <td>

                                                        {
                                                            version.score !==
                                                            null

                                                                ?

                                                                `${(
                                                                    version.score *
                                                                    100
                                                                ).toFixed(
                                                                    2
                                                                )}%`

                                                                :

                                                                "N/A"
                                                        }

                                                    </td>


                                                    <td>

                                                        {
                                                            isProduction

                                                                ?

                                                                <span className="production-badge">

                                                                    🟢 Production

                                                                </span>

                                                                :

                                                                <span className="inactive-badge">

                                                                    Inactive

                                                                </span>
                                                        }

                                                    </td>


                                                    <td>

                                                        {
                                                            !isProduction && (

                                                                <button
                                                                    className="production-button"
                                                                    disabled={
                                                                        updating
                                                                    }
                                                                    onClick={() =>
                                                                        handleSetProduction(
                                                                            version.version
                                                                        )
                                                                    }
                                                                >

                                                                    {
                                                                        updating

                                                                            ?

                                                                            "Updating..."

                                                                            :

                                                                            "Set Production"
                                                                    }

                                                                </button>

                                                            )
                                                        }

                                                    </td>

                                                </tr>

                                            );

                                        }
                                    )
                                }

                            </tbody>

                        </table>

                    </div>

                )
            }


            {/* EMPTY STATE */}

            {
                !loading &&
                registry &&
                (
                    !registry.versions ||
                    registry.versions.length === 0
                ) && (

                    <div className="registry-empty">

                        No model versions found.

                    </div>

                )
            }

        </div>

    );

}