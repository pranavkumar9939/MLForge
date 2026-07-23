import axios from "axios";

const API = "http://localhost:8000";

export const getROC = async (dataset, model) => {
    const response = await axios.get(
        `${API}/roc/${dataset}/${encodeURIComponent(model)}`
    );

    console.log(response.data);

    console.log(response.data.roc_curve);

    console.log(response.data.roc_curve.curves);

    return response.data;
};

export const getFeatureImportance = async (
    dataset,
    model,
    top_n = 10
) => {
    const response = await axios.get(
        `${API}/feature-importance/${dataset}/${encodeURIComponent(model)}?top_n=${top_n}`
    );

    return response.data;
};