import axios from "axios";

const API = "http://localhost:8000";

export async function getTuningResults(
    dataset,
    model
){

    const response = await axios.get(
        `${API}/tuning/${dataset}/${model}`
    );

    return response.data;
}