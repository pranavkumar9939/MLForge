import axios from "axios";

export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_URL,
});

const TOKEN_KEY = "mlforge_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

client.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Surface a clean, human error message everywhere instead of raw axios errors.
function unwrap(promise) {
  return promise
    .then((res) => res.data)
    .catch((err) => {
      const rawDetail = err?.response?.data?.detail;
      let detail;
      if (Array.isArray(rawDetail)) {
        // FastAPI/Pydantic validation errors come back as a list of {msg, loc, ...}
        detail = rawDetail.map((d) => d.msg || JSON.stringify(d)).join(" ");
      } else {
        detail = rawDetail || err?.message || "Something went wrong talking to the MLForge server.";
      }
      throw new Error(detail);
    });
}

/* ---------------- Auth ---------------- */

export function signup({ name, email, password }) {
  return unwrap(client.post("/auth/signup", { name, email, password }));
}

export function login({ email, password }) {
  return unwrap(client.post("/auth/login", { email, password }));
}

export function getMe() {
  return unwrap(client.get("/auth/me"));
}

/* ---------------- Upload / Analysis / Training ---------------- */

export function uploadDataset(file, onUploadProgress) {
  const form = new FormData();
  form.append("file", file);
  return unwrap(
    client.post("/upload/", form, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress,
    })
  );
}

export function startTraining({ filename, targetColumn, trainingMode }) {
  return unwrap(
    client.post("/upload/train/start", {
      filename,
      target_column: targetColumn,
      training_mode: trainingMode,
    })
  );
}

export function getJobStatus(jobId) {
  return unwrap(client.get(`/jobs/${jobId}`));
}

/* ---------------- Unsupervised (clustering / dimensionality reduction) ---------------- */

export function startUnsupervisedTraining({ filename, mode, nClusters, nComponents }) {
  return unwrap(
    client.post("/unsupervised/train/start", {
      filename,
      mode,
      n_clusters: nClusters ?? null,
      n_components: nComponents ?? 2,
    })
  );
}

export function getClusteringResults(dataset) {
  return unwrap(client.get(`/unsupervised/clustering/${dataset}`));
}

export function getDimensionalityReductionResults(dataset) {
  return unwrap(client.get(`/unsupervised/dimensionality-reduction/${dataset}`));
}

/* ---------------- Datasets / Models registry ---------------- */

export function getSavedModels() {
  return unwrap(client.get("/models/"));
}

export function getDatasets() {
  return unwrap(client.get("/datasets"));
}

export function getModelDetails(dataset, model) {
  return unwrap(client.get(`/models/${dataset}/${encodeURIComponent(model)}`));
}

export function getMetrics(dataset, model) {
  return unwrap(client.get(`/metrics/${dataset}/${encodeURIComponent(model)}`));
}

export function getLeaderboard(dataset) {
  return unwrap(client.get(`/leaderboard/${dataset}`));
}

export function getROC(dataset, model) {
  return unwrap(client.get(`/roc/${dataset}/${encodeURIComponent(model)}`));
}

export function getConfusionMatrix(dataset, model) {
  return unwrap(client.get(`/confusion-matrix/${dataset}/${encodeURIComponent(model)}`));
}

export function getFeatureImportance(dataset, model, topN = 10) {
  return unwrap(
    client.get(`/feature-importance/${dataset}/${encodeURIComponent(model)}?top_n=${topN}`)
  );
}

export function getTuningResults(dataset, model) {
  return unwrap(client.get(`/tuning/${dataset}/${encodeURIComponent(model)}`));
}

export function getModelVersions(dataset, model) {
  return unwrap(client.get(`/registry/${dataset}/${encodeURIComponent(model)}`));
}

export function setProductionModel(dataset, model, version) {
  return unwrap(client.post(`/registry/${dataset}/${encodeURIComponent(model)}/${version}`));
}

/* ---------------- Prediction ---------------- */

export function predictSingle(dataset, model, features) {
  return unwrap(
    client.post(`/predict/${dataset}/${encodeURIComponent(model)}`, { features })
  );
}

export function getPredictionHistory(dataset, model, version, { limit = 20, offset = 0 } = {}) {
  return unwrap(
    client.get(
      `/prediction-history/${dataset}/${encodeURIComponent(model)}/${version}?limit=${limit}&offset=${offset}`
    )
  );
}

/* ---------------- Reports ---------------- */

export async function downloadPdfReport(dataset, modelName) {
  const params = modelName ? { model_name: modelName } : {};
  const res = await client.get(`/report/${dataset}/pdf`, { params, responseType: "blob" });
  const filename = filenameFromDisposition(res.headers["content-disposition"], `${dataset}_report.pdf`);
  triggerBlobDownload(res.data, filename);
}

// Opens the HTML report in a new tab. Since it needs the auth header (not
// just a URL), fetch it as a blob and open that instead of navigating
// directly to the API URL.
export async function openHtmlReport(dataset, modelName) {
  const params = modelName ? { model_name: modelName } : {};
  const res = await client.get(`/report/${dataset}/html`, { params, responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([res.data], { type: "text/html" }));
  window.open(url, "_blank");
}

/* ---------------- Export / Batch prediction ---------------- */

function filenameFromDisposition(disposition, fallback) {
  const match = /filename="?([^";]+)"?/.exec(disposition || "");
  return match ? match[1] : fallback;
}

function triggerBlobDownload(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

// Downloads the exported model zip directly (model + pipeline + metadata + README).
export async function exportModel(dataset, model) {
  const res = await client.get(`/export/${dataset}/${encodeURIComponent(model)}`, {
    responseType: "blob",
  });
  const filename = filenameFromDisposition(res.headers["content-disposition"], `${dataset}_${model}.zip`);
  triggerBlobDownload(res.data, filename);
}

// Uploads a CSV/Excel of rows and downloads the predictions CSV directly.
export async function batchPredict(dataset, model, file) {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await client.post(
      `/predict/${dataset}/${encodeURIComponent(model)}/batch`,
      formData,
      { responseType: "blob" }
    );
    const filename = filenameFromDisposition(res.headers["content-disposition"], `${dataset}_${model}_predictions.csv`);
    triggerBlobDownload(res.data, filename);
  } catch (err) {
    // The error body is a blob too when responseType is "blob" - parse it back to JSON.
    if (err?.response?.data instanceof Blob) {
      const text = await err.response.data.text();
      let message = "Batch prediction failed.";
      try {
        const parsed = JSON.parse(text);
        message = parsed.detail || message;
      } catch {
        // response wasn't JSON - keep the generic message
      }
      throw new Error(message, { cause: err });
    }
    throw new Error(err.message || "Batch prediction failed.", { cause: err });
  }
}

/* ---------------- System ---------------- */

export function checkHealth() {
  return unwrap(client.get("/health"));
}

export default client;
