import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getSavedModels } from "../lib/api";
import { Card, EmptyState, Badge } from "../components/ui/Primitives";
import Button from "../components/ui/Button";
import "./Dashboard.css";

function formatScore(perf) {
  if (perf === null || perf === undefined) return "—";
  if (perf <= 1) return `${(perf * 100).toFixed(1)}%`;
  if (perf <= 100) return `${perf.toFixed(1)}%`;
  return perf.toFixed(3);
}

export default function Dashboard() {
  const [datasets, setDatasets] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getSavedModels()
      .then((data) => setDatasets(data.datasets || []))
      .catch((err) => setError(err.message));
  }, []);

  const totalModels = (datasets || []).reduce((sum, d) => sum + d.models.length, 0);

  return (
    <main className="page shell">
      <div className="dash-head">
        <div>
          <h1>Dashboard</h1>
          <p>Every dataset you've trained a model on, and how each model performed.</p>
        </div>
        <Link to="/upload"><Button variant="primary">New experiment</Button></Link>
      </div>

      {datasets && datasets.length > 0 && (
        <div className="stat-row">
          <Card className="stat-card">
            <div className="stat-value">{datasets.length}</div>
            <div className="stat-label">Datasets trained</div>
          </Card>
          <Card className="stat-card">
            <div className="stat-value">{totalModels}</div>
            <div className="stat-label">Models produced</div>
          </Card>
          <Card className="stat-card">
            <div className="stat-value">{Math.round(totalModels / Math.max(datasets.length, 1))}</div>
            <div className="stat-label">Avg. models per dataset</div>
          </Card>
        </div>
      )}

      {error && (
        <Card padded>
          <EmptyState
            title="Couldn't reach the MLForge server"
            description={error}
          />
        </Card>
      )}

      {!error && datasets === null && (
        <Card padded>
          <EmptyState title="Loading experiments…" />
        </Card>
      )}

      {!error && datasets && datasets.length === 0 && (
        <Card padded>
          <EmptyState
            title="No experiments yet"
            description="Upload your first dataset to see analysis, training, and a model leaderboard here."
            action={<Link to="/upload"><Button variant="primary">Upload a dataset</Button></Link>}
          />
        </Card>
      )}

      {datasets && datasets.filter((d) => d.models.length > 0).map((dataset) => {
        const best = [...dataset.models].sort((a, b) => (b.performance || 0) - (a.performance || 0))[0];
        return (
          <Card key={dataset.dataset_name} className="dataset-card">
            <div className="dataset-card-head">
              <h3>{dataset.models[0]?.display_name || dataset.dataset_name}</h3>
              <Link to={`/results/${dataset.dataset_name}`}>
                <Button variant="secondary" size="sm">View results</Button>
              </Link>
            </div>
            {dataset.models.slice(0, 5).map((m) => (
              <div className="model-row" key={m.model_name}>
                <div>
                  <div className="model-row-name">{m.model_name}</div>
                  <div className="model-row-meta">
                    {m.problem_type} &middot; target: {m.target_column}
                  </div>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  {best && best.model_name === m.model_name && (
                    <Badge tone="ember">Best</Badge>
                  )}
                  <span className="model-row-score">{formatScore(m.performance)}</span>
                </div>
              </div>
            ))}
          </Card>
        );
      })}
    </main>
  );
}
