import { useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadDataset, startTraining, startUnsupervisedTraining } from "../lib/api";
import { Card, Badge } from "../components/ui/Primitives";
import Button from "../components/ui/Button";
import "./Upload.css";

const TRAINING_MODES = [
  { id: "fast", label: "Fast", desc: "Fewer tuning iterations, 3-fold CV. Best for a quick first look." },
  { id: "balanced", label: "Balanced", desc: "A sensible default tuning budget. Recommended for most datasets." },
  { id: "thorough", label: "Thorough", desc: "Wider hyperparameter search, 5-fold CV. Slower, more accurate." },
];

const LEARNING_TYPES = [
  { id: "supervised", label: "Predict a column", desc: "Train models to predict a target column (classification or regression)." },
  { id: "clustering", label: "Find groups", desc: "Discover natural groupings in the data — no target column needed." },
  { id: "dimensionality_reduction", label: "Reduce dimensions", desc: "Project the data down to 2D to visualize its structure." },
];

function StepsBar({ step }) {
  const steps = ["Upload", "Review & confirm", "Train"];
  return (
    <div className="steps-bar">
      {steps.map((label, i) => (
        <>
          <div key={label} className={`step-chip ${i < step ? "done" : ""} ${i === step ? "current" : ""}`}>
            <span className="num">{i < step ? "✓" : i + 1}</span>
            <span>{label}</span>
          </div>
          {i < steps.length - 1 && <div className="step-sep" key={`${label}-sep`} />}
        </>
      ))}
    </div>
  );
}

export default function Upload() {
  const navigate = useNavigate();
  const fileInput = useRef(null);

  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const [uploadResult, setUploadResult] = useState(null); // { filename, analysis, rows, columns }
  const [learningType, setLearningType] = useState("supervised");
  const [targetColumn, setTargetColumn] = useState(null);
  const [trainingMode, setTrainingMode] = useState("balanced");
  const [nClusters, setNClusters] = useState(""); // blank = auto-detect
  const [starting, setStarting] = useState(false);

  const step = uploadResult ? 1 : 0;

  async function handleFile(file) {
    if (!file) return;
    setError(null);
    setUploading(true);
    try {
      const result = await uploadDataset(file);
      setUploadResult(result);
      setTargetColumn(result.analysis.target_recommendation.recommended_column);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  function onDrop(e) {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files?.[0];
    handleFile(file);
  }

  const candidates = useMemo(
    () => (uploadResult ? [...uploadResult.analysis.target_recommendation.candidates].sort((a, b) => b.score - a.score) : []),
    [uploadResult]
  );

  const selectedCandidate = candidates.find((c) => c.column === targetColumn);
  const recommendation = uploadResult?.analysis.target_recommendation;
  const isRecommended = targetColumn === recommendation?.recommended_column;

  async function handleStartTraining() {
    setStarting(true);
    setError(null);
    try {
      let job_id;
      if (learningType === "supervised") {
        ({ job_id } = await startTraining({
          filename: uploadResult.filename,
          targetColumn,
          trainingMode,
        }));
      } else {
        ({ job_id } = await startUnsupervisedTraining({
          filename: uploadResult.filename,
          mode: learningType,
          nClusters: nClusters ? parseInt(nClusters, 10) : null,
          nComponents: 2,
        }));
      }
      navigate(`/training/${job_id}`, { state: { filename: uploadResult.filename } });
    } catch (err) {
      setError(err.message);
      setStarting(false);
    }
  }

  return (
    <main className="page shell">
      <div className="upload-head">
        <h1>New experiment</h1>
        <p>Upload a dataset, confirm the target column MLForge should predict, then start training.</p>
      </div>

      <StepsBar step={step} />

      {error && (
        <Card padded style={{ marginBottom: 20, borderColor: "var(--danger)" }}>
          <strong style={{ color: "var(--danger)" }}>Something went wrong</strong>
          <p style={{ marginTop: 6, fontSize: 13.5, color: "var(--text-secondary)" }}>{error}</p>
        </Card>
      )}

      {!uploadResult && (
        <div
          className={`dropzone ${dragging ? "dragging" : ""}`}
          onClick={() => fileInput.current?.click()}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
        >
          <svg className="dropzone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M12 16V4m0 0-4 4m4-4 4 4" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <h3>{uploading ? "Uploading…" : "Drop a CSV or Excel file here"}</h3>
          <p>or click to browse &middot; .csv, .xlsx, .xls</p>
          <input
            ref={fileInput}
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={(e) => handleFile(e.target.files?.[0])}
          />
        </div>
      )}

      {uploadResult && (
        <>
          <div className="stat-strip">
            <Card>
              <div className="value">{uploadResult.analysis.rows.toLocaleString()}</div>
              <div className="label">Rows</div>
            </Card>
            <Card>
              <div className="value">{uploadResult.analysis.columns}</div>
              <div className="label">Columns</div>
            </Card>
            <Card>
              <div className="value">{uploadResult.analysis.missing_values.toLocaleString()}</div>
              <div className="label">Missing values</div>
            </Card>
            <Card>
              <div className="value">{uploadResult.analysis.duplicate_rows.toLocaleString()}</div>
              <div className="label">Duplicate rows</div>
            </Card>
          </div>

          <Card style={{ marginBottom: 20 }} padded>
            <h3 style={{ marginBottom: 4 }}>What do you want to do?</h3>
            <p style={{ fontSize: 13, color: "var(--text-tertiary)", marginBottom: 4 }}>
              This decides the whole workflow — supervised needs a target column, the others don't.
            </p>
            <div className="mode-grid">
              {LEARNING_TYPES.map((t) => (
                <div
                  key={t.id}
                  className={`mode-option ${learningType === t.id ? "selected" : ""}`}
                  onClick={() => setLearningType(t.id)}
                >
                  <h5>{t.label}</h5>
                  <p>{t.desc}</p>
                </div>
              ))}
            </div>
          </Card>

          {learningType === "supervised" && (
            <Card style={{ marginBottom: 20 }}>
            <div className="card-header">
              <h3>Target column</h3>
              <Badge tone={recommendation.confidence === "high" ? "success" : "warning"}>
                <span className="confidence-tag">{recommendation.confidence} confidence</span>
              </Badge>
            </div>
            <div className="card-body">
              <div className="target-callout">
                <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v4m0 4h.01" strokeLinecap="round" />
                </svg>
                <div>
                  <h4>
                    MLForge recommends <span className="mono-tag">{recommendation.recommended_column}</span>
                    {isRecommended && " — currently selected"}
                  </h4>
                  <p>This is a suggestion only — nothing trains until you confirm a target below.</p>
                  {selectedCandidate && (
                    <ul className="reasons">
                      {selectedCandidate.reasons.map((r) => <li key={r}>{r}</li>)}
                    </ul>
                  )}
                </div>
              </div>

              <div className="field">
                <label htmlFor="target-select">Confirm the target column to predict</label>
                <select
                  id="target-select"
                  className="select"
                  value={targetColumn || ""}
                  onChange={(e) => setTargetColumn(e.target.value)}
                >
                  {candidates.map((c) => (
                    <option key={c.column} value={c.column}>
                      {c.column} {c.column === recommendation.recommended_column ? "(recommended)" : ""}
                    </option>
                  ))}
                </select>
                <span className="hint">
                  Problem type will be re-detected from whichever column you confirm.
                </span>
              </div>
            </div>
          </Card>
          )}

          <Card style={{ marginBottom: 20 }} padded>
            <div className="card-header" style={{ padding: 0, border: "none", marginBottom: 14 }}>
              <h3>Column analysis</h3>
            </div>
            <div style={{ overflowX: "auto" }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>Column</th>
                    <th>Type</th>
                    <th>Missing</th>
                    <th>Unique</th>
                    <th>Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(uploadResult.analysis.column_analysis).map(([name, info]) => (
                    <tr key={name}>
                      <td style={{ fontWeight: name === targetColumn ? 700 : 500 }}>
                        {name}
                        {learningType === "supervised" && name === targetColumn && <Badge tone="ember"> target</Badge>}
                      </td>
                      <td><span className="col-type-badge">{info.type}</span></td>
                      <td>{info.Missing_percentage}%</td>
                      <td>{info.unique}</td>
                      <td>
                        {info.is_identifier && <Badge tone="neutral">identifier — excluded</Badge>}
                        {info.is_constant && <Badge tone="neutral">constant — excluded</Badge>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          {learningType === "supervised" && (
            <Card style={{ marginBottom: 20 }} padded>
              <h3 style={{ marginBottom: 4 }}>Training mode</h3>
              <p style={{ fontSize: 13, color: "var(--text-tertiary)", marginBottom: 4 }}>
                Controls the hyperparameter search budget for every candidate model.
              </p>
              <div className="mode-grid">
                {TRAINING_MODES.map((m) => (
                  <div
                    key={m.id}
                    className={`mode-option ${trainingMode === m.id ? "selected" : ""}`}
                    onClick={() => setTrainingMode(m.id)}
                  >
                    <h5>{m.label}</h5>
                    <p>{m.desc}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {learningType === "clustering" && (
            <Card style={{ marginBottom: 20 }} padded>
              <h3 style={{ marginBottom: 4 }}>Number of clusters</h3>
              <p style={{ fontSize: 13, color: "var(--text-tertiary)", marginBottom: 12 }}>
                Leave blank to let MLForge pick the number of clusters automatically using silhouette score.
              </p>
              <div className="field" style={{ maxWidth: 220 }}>
                <input
                  className="input"
                  type="number"
                  min={2}
                  max={20}
                  placeholder="Auto-detect"
                  value={nClusters}
                  onChange={(e) => setNClusters(e.target.value)}
                />
              </div>
            </Card>
          )}

          <div className="action-bar">
            <Button variant="secondary" onClick={() => { setUploadResult(null); setError(null); }}>
              Upload a different file
            </Button>
            <Button variant="primary" size="lg" loading={starting} onClick={handleStartTraining}>
              {learningType === "supervised" ? "Start training" : learningType === "clustering" ? "Find clusters" : "Reduce dimensions"}
            </Button>
          </div>
        </>
      )}
    </main>
  );
}
