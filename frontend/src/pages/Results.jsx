import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  getLeaderboard,
  getMetrics,
  getROC,
  getConfusionMatrix,
  getFeatureImportance,
  getTuningResults,
  getModelDetails,
  exportModel,
  downloadPdfReport,
  openHtmlReport,
} from "../lib/api";
import { Card, CardHeader, CardBody, Badge, EmptyState } from "../components/ui/Primitives";
import Button from "../components/ui/Button";
import RocCurveChart from "../components/charts/RocCurveChart";
import ConfusionMatrixGrid from "../components/charts/ConfusionMatrixGrid";
import FeatureImportanceBar from "../components/charts/FeatureImportanceBar";
import "./Results.css";

function fmtPct(v) {
  if (v === undefined || v === null) return "—";
  return `${v.toFixed(1)}%`;
}

export default function Results() {
  const { datasetName } = useParams();

  const [leaderboard, setLeaderboard] = useState(null);
  const [error, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState(null);

  const [metrics, setMetrics] = useState(null);
  const [roc, setRoc] = useState(null);
  const [matrix, setMatrix] = useState(null);
  const [featureImportance, setFeatureImportance] = useState(null);
  const [tuning, setTuning] = useState(null);
  const [displayName, setDisplayName] = useState(null);
  const [exporting, setExporting] = useState(false);
  const [exportError, setExportError] = useState(null);
  const [reportBusy, setReportBusy] = useState(null); // "pdf" | "html" | null
  const [reportError, setReportError] = useState(null);

  useEffect(() => {
    getLeaderboard(datasetName)
      .then((data) => {
        setLeaderboard(data);
        if (data.leaderboard.length > 0) {
          setSelectedModel(data.best_model || data.leaderboard[0].model_name);
        }
      })
      .catch((err) => setError(err.message));
  }, [datasetName]);

  useEffect(() => {
    if (!selectedModel) return;

    getMetrics(datasetName, selectedModel).then(setMetrics).catch(() => setMetrics(null));
    getROC(datasetName, selectedModel).then((d) => setRoc(d.roc_curve)).catch(() => setRoc(null));
    getConfusionMatrix(datasetName, selectedModel).then((d) => setMatrix(d.confusion_matrix)).catch(() => setMatrix(null));
    getFeatureImportance(datasetName, selectedModel).then((d) => setFeatureImportance(d.feature_importance)).catch(() => setFeatureImportance(null));
    getTuningResults(datasetName, selectedModel).then(setTuning).catch(() => setTuning(null));
    getModelDetails(datasetName, selectedModel).then((d) => setDisplayName(d.display_name)).catch(() => {});
  }, [datasetName, selectedModel]);

  if (error) {
    return (
      <main className="page shell">
        <Card padded>
          <EmptyState title="Couldn't load results" description={error} />
        </Card>
      </main>
    );
  }

  if (!leaderboard) {
    return (
      <main className="page shell">
        <Card padded><EmptyState title="Loading results…" /></Card>
      </main>
    );
  }

  const isRegression = leaderboard.problem_type === "Regression";

  async function handleExport() {
    setExporting(true);
    setExportError(null);
    try {
      await exportModel(datasetName, selectedModel);
    } catch (err) {
      setExportError(err.message);
    } finally {
      setExporting(false);
    }
  }

  async function handleDownloadPdf() {
    setReportBusy("pdf");
    setReportError(null);
    try {
      await downloadPdfReport(datasetName, selectedModel);
    } catch (err) {
      setReportError(err.message);
    } finally {
      setReportBusy(null);
    }
  }

  async function handleViewHtmlReport() {
    setReportBusy("html");
    setReportError(null);
    try {
      await openHtmlReport(datasetName, selectedModel);
    } catch (err) {
      setReportError(err.message);
    } finally {
      setReportBusy(null);
    }
  }

  return (
    <main className="page shell">
      <div className="results-head">
        <div>
          <h1>{displayName || datasetName}</h1>
          <p>{leaderboard.problem_type} &middot; {leaderboard.leaderboard.length} models trained</p>
          {(exportError || reportError) && (
            <p style={{ color: "var(--danger)", fontSize: 12.5, marginTop: 4 }}>{exportError || reportError}</p>
          )}
        </div>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <Button variant="ghost" loading={reportBusy === "html"} disabled={!selectedModel} onClick={handleViewHtmlReport}>
            View report
          </Button>
          <Button variant="secondary" loading={reportBusy === "pdf"} disabled={!selectedModel} onClick={handleDownloadPdf}>
            Download PDF
          </Button>
          <Button variant="secondary" loading={exporting} disabled={!selectedModel} onClick={handleExport}>
            Export model
          </Button>
          <Link to={`/predict/${datasetName}/${encodeURIComponent(selectedModel || "")}`}>
            <Button variant="primary" disabled={!selectedModel}>Make a prediction</Button>
          </Link>
        </div>
      </div>

      {metrics && (
        <div className="metrics-row">
          {isRegression ? (
            <>
              <Card className="metric-tile">
                <div className="metric-value">{(metrics.r2_score * 100).toFixed(1)}%</div>
                <div className="metric-label">R&sup2; Score</div>
              </Card>
              <Card className="metric-tile">
                <div className="metric-value">{metrics.mae?.toFixed(3)}</div>
                <div className="metric-label">MAE</div>
              </Card>
              <Card className="metric-tile">
                <div className="metric-value">{metrics.rmse?.toFixed(3)}</div>
                <div className="metric-label">RMSE</div>
              </Card>
              <Card className="metric-tile">
                <div className="metric-value" style={{ fontSize: 16 }}>{metrics.status}</div>
                <div className="metric-label">Status</div>
              </Card>
            </>
          ) : (
            <>
              <Card className="metric-tile">
                <div className="metric-value">{fmtPct(metrics.accuracy)}</div>
                <div className="metric-label">Accuracy</div>
              </Card>
              <Card className="metric-tile">
                <div className="metric-value">{fmtPct(metrics.precision)}</div>
                <div className="metric-label">Precision</div>
              </Card>
              <Card className="metric-tile">
                <div className="metric-value">{fmtPct(metrics.recall)}</div>
                <div className="metric-label">Recall</div>
              </Card>
              <Card className="metric-tile">
                <div className="metric-value">{fmtPct(metrics.f1_score)}</div>
                <div className="metric-label">F1 Score</div>
              </Card>
            </>
          )}
        </div>
      )}

      <Card style={{ marginBottom: 24 }}>
        <CardHeader title="Model leaderboard" subtitle="Click a row to inspect that model in detail." />
        <div style={{ overflowX: "auto" }}>
          <table className="table leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Model</th>
                {isRegression ? (
                  <>
                    <th>R&sup2;</th>
                    <th>MAE</th>
                    <th>RMSE</th>
                  </>
                ) : (
                  <>
                    <th>Accuracy</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1</th>
                  </>
                )}
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.leaderboard.map((m) => (
                <tr
                  key={m.model_name}
                  className={`${m.model_name === leaderboard.best_model ? "winner" : ""} ${m.model_name === selectedModel ? "selected" : ""}`}
                  onClick={() => setSelectedModel(m.model_name)}
                >
                  <td className="rank-cell">{m.rank}</td>
                  <td>
                    {m.model_name}
                    {m.model_name === leaderboard.best_model && <Badge tone="ember"> Best</Badge>}
                  </td>
                  {isRegression ? (
                    <>
                      <td className="score-cell">{m.r2_score?.toFixed(3)}</td>
                      <td className="score-cell">{m.mae?.toFixed(3)}</td>
                      <td className="score-cell">{m.rmse?.toFixed(3)}</td>
                    </>
                  ) : (
                    <>
                      <td className="score-cell">{fmtPct(m.accuracy)}</td>
                      <td className="score-cell">{fmtPct(m.precision)}</td>
                      <td className="score-cell">{fmtPct(m.recall)}</td>
                      <td className="score-cell">{fmtPct(m.f1_score)}</td>
                    </>
                  )}
                  <td><Badge tone="neutral">{m.status}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <div className="results-grid">
        {!isRegression && (
          <Card>
            <CardHeader title="ROC Curve" subtitle={selectedModel} />
            <CardBody><RocCurveChart rocData={roc} /></CardBody>
          </Card>
        )}
        {!isRegression && (
          <Card>
            <CardHeader title="Confusion Matrix" subtitle={selectedModel} />
            <CardBody><ConfusionMatrixGrid matrix={matrix} /></CardBody>
          </Card>
        )}
        <Card style={isRegression ? { gridColumn: "1 / -1" } : {}}>
          <CardHeader title="Feature Importance" subtitle={selectedModel} />
          <CardBody><FeatureImportanceBar data={featureImportance} /></CardBody>
        </Card>
        <Card>
          <CardHeader title="Hyperparameter Tuning" subtitle={selectedModel} />
          <CardBody>
            {tuning && tuning.tuned ? (
              <>
                <div className="metric-tile" style={{ padding: 0, marginBottom: 14 }}>
                  <div className="metric-value">
                    {tuning.best_cv_score !== null ? `${(tuning.best_cv_score * 100).toFixed(2)}%` : "N/A"}
                  </div>
                  <div className="metric-label">Best cross-validated score</div>
                </div>
                <div className="params-list">
                  {Object.entries(tuning.best_params || {}).map(([k, v]) => (
                    <div className="params-row" key={k}>
                      <span className="key">{k}</span>
                      <span className="val">{String(v)}</span>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <EmptyState title="Not tuned" description="This model was trained with default parameters (no search grid defined)." />
            )}
          </CardBody>
        </Card>
      </div>
    </main>
  );
}
