import { useEffect, useMemo, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getModelDetails, predictSingle, batchPredict } from "../lib/api";
import { Card, CardHeader, CardBody, EmptyState, Badge } from "../components/ui/Primitives";
import Button from "../components/ui/Button";
import "./Predict.css";

function ContributionBar({ feature, value, max }) {
  const pct = max ? (Math.abs(value) / max) * 100 : 0;
  const positive = value >= 0;
  return (
    <div className="contrib-row">
      <span className="contrib-name">{feature.replace(/^numerical__|^categorical__/, "")}</span>
      <div className="contrib-bar-track">
        <div
          className="contrib-bar-fill"
          style={{
            width: `${pct}%`,
            background: positive ? "var(--ember)" : "var(--info)",
            marginLeft: positive ? "50%" : `${50 - pct}%`,
          }}
        />
      </div>
      <span className="contrib-value">{value.toFixed(3)}</span>
    </div>
  );
}

export default function Predict() {
  const { datasetName, modelName } = useParams();

  const [details, setDetails] = useState(null);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [predictError, setPredictError] = useState(null);

  const batchInput = useRef(null);
  const [batchSubmitting, setBatchSubmitting] = useState(false);
  const [batchError, setBatchError] = useState(null);
  const [batchDone, setBatchDone] = useState(false);

  useEffect(() => {
    getModelDetails(datasetName, modelName)
      .then((data) => {
        setDetails(data);
        const initial = {};
        (data.input_schema || []).forEach((field) => {
          initial[field.name] = field.example ?? "";
        });
        setForm(initial);
      })
      .catch((err) => setError(err.message));
  }, [datasetName, modelName]);

  const schema = details?.input_schema || [];

  const contributions = useMemo(() => {
    if (!result) return [];
    const shap = result.shap;
    if (Array.isArray(shap) && shap.length > 0) {
      return shap.map((s) => ({ feature: s.feature, value: s.shap_value }));
    }
    const top = result.explanation?.top_contributing_features || [];
    return top.map((s) => ({ feature: s.feature, value: s.contribution }));
  }, [result]);

  const maxAbs = Math.max(1e-9, ...contributions.map((c) => Math.abs(c.value)));

  async function handleBatchFile(file) {
    if (!file) return;
    setBatchSubmitting(true);
    setBatchError(null);
    setBatchDone(false);
    try {
      await batchPredict(datasetName, modelName, file);
      setBatchDone(true);
    } catch (err) {
      setBatchError(err.message);
    } finally {
      setBatchSubmitting(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setPredictError(null);
    setResult(null);
    try {
      const payload = {};
      schema.forEach((field) => {
        const raw = form[field.name];
        payload[field.name] = field.type === "Numerical" ? parseFloat(raw) : raw;
      });
      const res = await predictSingle(datasetName, modelName, payload);
      setResult(res);
    } catch (err) {
      setPredictError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (error) {
    return (
      <main className="page shell">
        <Card padded><EmptyState title="Couldn't load this model" description={error} /></Card>
      </main>
    );
  }

  if (!details) {
    return (
      <main className="page shell">
        <Card padded><EmptyState title="Loading model…" /></Card>
      </main>
    );
  }

  return (
    <main className="page shell">
      <div className="predict-head">
        <h1>Predict with {modelName}</h1>
        <p>
          Dataset: <span className="mono-tag">{details.display_name || datasetName}</span> &middot; target:{" "}
          <span className="mono-tag">{details.target_column}</span>
        </p>
      </div>

      <div className="predict-grid">
        <Card>
          <CardHeader title="Input" subtitle="Fill in a row of feature values" />
          <CardBody>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                {schema.map((field) => (
                  <div className="field" key={field.name}>
                    <label>{field.name}</label>

                    {field.type === "Numerical" && (
                      <>
                        <input
                          className="input"
                          type="number"
                          step="any"
                          value={form[field.name] ?? ""}
                          onChange={(e) => setForm((f) => ({ ...f, [field.name]: e.target.value }))}
                        />
                        {field.min !== undefined && field.max !== undefined && (
                          <span className="hint">range {field.min} &ndash; {field.max}</span>
                        )}
                      </>
                    )}

                    {(field.type === "Categorical" || field.type === "Boolean") && (
                      field.options && field.options.length ? (
                        <select
                          className="select"
                          value={form[field.name] ?? ""}
                          onChange={(e) => setForm((f) => ({ ...f, [field.name]: e.target.value }))}
                        >
                          {field.options.map((o) => <option key={o} value={o}>{o}</option>)}
                        </select>
                      ) : (
                        <input
                          className="input"
                          type="text"
                          value={form[field.name] ?? ""}
                          onChange={(e) => setForm((f) => ({ ...f, [field.name]: e.target.value }))}
                        />
                      )
                    )}

                    {field.type === "Datetime" && (
                      <input
                        className="input"
                        type="date"
                        value={form[field.name] ?? ""}
                        onChange={(e) => setForm((f) => ({ ...f, [field.name]: e.target.value }))}
                      />
                    )}
                  </div>
                ))}
              </div>

              {schema.length === 0 && (
                <EmptyState title="No input fields" description="This model has no recorded input schema." />
              )}

              {predictError && (
                <p style={{ color: "var(--danger)", fontSize: 13, marginTop: 16 }}>{predictError}</p>
              )}

              <div style={{ marginTop: 22 }}>
                <Button type="submit" variant="primary" loading={submitting} block disabled={schema.length === 0}>
                  Predict
                </Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="Prediction" />
          <CardBody>
            {!result && (
              <EmptyState title="No prediction yet" description="Fill in the form and submit to see a result here." />
            )}
            {result && (
              <>
                <div className="result-hero">
                  <div className="label">Predicted {details.target_column}</div>
                  <div className="value">{String(result.prediction)}</div>
                  {result.confidence !== null && result.confidence !== undefined && (
                    <div className="confidence">
                      <Badge tone="success">{(result.confidence * 100).toFixed(1)}% confidence</Badge>
                    </div>
                  )}
                </div>

                {contributions.length > 0 && (
                  <div style={{ marginTop: 8 }}>
                    <h4 style={{ fontSize: 13.5, marginBottom: 10, color: "var(--text-secondary)" }}>
                      Why MLForge predicted this
                    </h4>
                    {contributions.map((c) => (
                      <ContributionBar key={c.feature} feature={c.feature} value={c.value} max={maxAbs} />
                    ))}
                  </div>
                )}
              </>
            )}
          </CardBody>
        </Card>
      </div>

      <Card style={{ marginTop: 20 }}>
        <CardHeader
          title="Batch prediction"
          subtitle="Upload a CSV or Excel file with the same columns to get predictions for every row."
        />
        <CardBody>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <Button
              variant="secondary"
              loading={batchSubmitting}
              onClick={() => batchInput.current?.click()}
            >
              Choose file &amp; download predictions
            </Button>
            <input
              ref={batchInput}
              type="file"
              accept=".csv,.xlsx,.xls"
              style={{ display: "none" }}
              onChange={(e) => handleBatchFile(e.target.files?.[0])}
            />
            {batchDone && <Badge tone="success">Downloaded</Badge>}
          </div>
          {batchError && (
            <p style={{ color: "var(--danger)", fontSize: 13, marginTop: 12 }}>{batchError}</p>
          )}
          <p style={{ fontSize: 12.5, color: "var(--text-tertiary)", marginTop: 12 }}>
            Required columns: {schema.map((f) => f.name).join(", ") || "—"}. Up to 5,000 rows per file.
          </p>
        </CardBody>
      </Card>

      <div style={{ marginTop: 24 }}>
        <Link to={`/results/${datasetName}`}><Button variant="ghost">&larr; Back to results</Button></Link>
      </div>
    </main>
  );
}
