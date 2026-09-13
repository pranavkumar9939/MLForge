import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { getDimensionalityReductionResults } from "../lib/api";
import { Card, CardHeader, CardBody, Badge, EmptyState } from "../components/ui/Primitives";
import ClusterScatterChart from "../components/charts/ClusterScatterChart";
import "./UnsupervisedResults.css";

export default function DimensionalityReductionResults() {
  const { datasetName } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [selectedAlgo, setSelectedAlgo] = useState(null);

  useEffect(() => {
    getDimensionalityReductionResults(datasetName)
      .then((d) => {
        setData(d);
        if (d.results.length > 0) setSelectedAlgo(d.results[0].algorithm);
      })
      .catch((err) => setError(err.message));
  }, [datasetName]);

  const selected = useMemo(
    () => data?.results.find((r) => r.algorithm === selectedAlgo),
    [data, selectedAlgo]
  );

  if (error) {
    return <main className="page shell"><Card padded><EmptyState title="Couldn't load results" description={error} /></Card></main>;
  }
  if (!data) {
    return <main className="page shell"><Card padded><EmptyState title="Loading…" /></Card></main>;
  }

  const displayName = data.metadata?.display_name || datasetName;

  return (
    <main className="page shell">
      <div className="unsup-head">
        <div>
          <h1>{displayName}</h1>
          <p>Dimensionality reduction &middot; {data.results.length} algorithms compared</p>
        </div>
      </div>

      {data.results.length === 0 ? (
        <Card padded><EmptyState title="No algorithm produced a projection" description="Every candidate was skipped — see details below." /></Card>
      ) : (
        <>
          <div className="algo-tab-row">
            {data.results.map((r) => (
              <button
                key={r.algorithm}
                className={`algo-tab ${r.algorithm === selectedAlgo ? "active" : ""}`}
                onClick={() => setSelectedAlgo(r.algorithm)}
              >
                {r.algorithm}
              </button>
            ))}
          </div>

          <div className="unsup-grid">
            <Card>
              <CardHeader title="2D projection" subtitle={selectedAlgo} />
              <CardBody>
                <ClusterScatterChart points={selected?.coordinates} />
              </CardBody>
            </Card>
            <Card>
              <CardHeader title="Explained variance" subtitle={selectedAlgo} />
              <CardBody>
                {selected?.explained_variance_ratio ? (
                  <>
                    <div className="cluster-size-row">
                      <span style={{ width: 110, flexShrink: 0 }}>Component 1</span>
                      <div className="cluster-size-bar-track">
                        <div className="cluster-size-bar-fill" style={{ width: `${selected.explained_variance_ratio[0] * 100}%`, background: "var(--series-1)" }} />
                      </div>
                      <span className="cluster-size-count">{(selected.explained_variance_ratio[0] * 100).toFixed(1)}%</span>
                    </div>
                    <div className="cluster-size-row">
                      <span style={{ width: 110, flexShrink: 0 }}>Component 2</span>
                      <div className="cluster-size-bar-track">
                        <div className="cluster-size-bar-fill" style={{ width: `${selected.explained_variance_ratio[1] * 100}%`, background: "var(--series-2)" }} />
                      </div>
                      <span className="cluster-size-count">{(selected.explained_variance_ratio[1] * 100).toFixed(1)}%</span>
                    </div>
                    <p style={{ fontSize: 12.5, color: "var(--text-tertiary)", marginTop: 12 }}>
                      Together these two components capture{" "}
                      <Badge tone="ember">{(selected.total_explained_variance * 100).toFixed(1)}%</Badge>{" "}
                      of the total variance in the data.
                    </p>
                  </>
                ) : (
                  <EmptyState
                    title="Not applicable"
                    description={`${selectedAlgo} doesn't expose an explained-variance metric (only PCA and Truncated SVD do).`}
                  />
                )}
              </CardBody>
            </Card>
          </div>
        </>
      )}

      {data.skipped?.length > 0 && (
        <div className="skipped-note">
          <strong>Skipped algorithms:</strong>
          <ul style={{ marginTop: 6, paddingLeft: 18 }}>
            {data.skipped.map((s) => <li key={s.algorithm}><strong>{s.algorithm}</strong>: {s.reason}</li>)}
          </ul>
        </div>
      )}
    </main>
  );
}
