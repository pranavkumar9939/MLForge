import axios from "axios";

const API = "http://localhost:8000";


export async function getModelVersions(
    datasetName,
    modelName
) {

    const response = await axios.get(
        `${API}/registry/${datasetName}/${modelName}`
    );

    return response.data;
}


export async function setProductionModel(
    datasetName,
    modelName,
    version
) {

    const response = await axios.post(
        `${API}/registry/${datasetName}/${modelName}/${version}`
    );

    return response.data;
}