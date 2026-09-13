import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { getClusteringResults } from "../lib/api";
import { Card, CardHeader, CardBody, Badge, EmptyState } from "../components/ui/Primitives";
import ClusterScatterChart from "../components/charts/ClusterScatterChart";
import "./UnsupervisedResults.css";

const SWATCHES = [
  "var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)",
  "var(--series-5)", "var(--series-6)", "var(--series-7)", "var(--series-8)",
];

export default function ClusteringResults() {
  const { datasetName } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [selectedAlgo, setSelectedAlgo] = useState(null);

  useEffect(() => {
    getClusteringResults(datasetName)
      .then((d) => {
        setData(d);
        if (d.results.length > 0) setSelectedAlgo(d.best_algorithm || d.results[0].algorithm);
      })
      .catch((err) => setError(err.message));
  }, [datasetName]);

  const selected = useMemo(
    () => data?.results.find((r) => r.algorithm === selectedAlgo),
    [data, selectedAlgo]
  );

  if (error) {
    return <main className="page shell"><Card padded><EmptyState title="Couldn't load clustering results" description={error} /></Card></main>;
  }
  if (!data) {
    return <main className="page shell"><Card padded><EmptyState title="Loading…" /></Card></main>;
  }

  const displayName = data.metadata?.display_name || datasetName;
  const maxClusterSize = selected ? Math.max(...Object.values(selected.cluster_sizes)) : 1;

  return (
    <main className="page shell">
      <div className="unsup-head">
        <div>
          <h1>{displayName}</h1>
          <p>Clustering &middot; recommended k = {data.recommended_k} &middot; {data.results.length} algorithms compared</p>
        </div>
      </div>

      {data.results.length === 0 ? (
        <Card padded><EmptyState title="No algorithm produced a usable clustering" description="Every candidate was skipped — see details below." /></Card>
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
                {r.algorithm === data.best_algorithm && " ★"}
              </button>
            ))}
          </div>

          <Card style={{ marginBottom: 24 }}>
            <CardHeader
              title="Algorithm comparison"
              subtitle="Ranked by silhouette score (higher is better)"
            />
            <div style={{ overflowX: "auto" }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>Algorithm</th>
                    <th>Clusters found</th>
                    <th>Silhouette</th>
                    <th>Davies-Bouldin</th>
                    <th>Calinski-Harabasz</th>
                    <th>Noise points</th>
                  </tr>
                </thead>
                <tbody>
                  {data.results.map((r) => (
                    <tr key={r.algorithm} className={r.algorithm === selectedAlgo ? "" : ""} onClick={() => setSelectedAlgo(r.algorithm)} style={{ cursor: "pointer" }}>
                      <td style={{ fontWeight: 600 }}>
                        {r.algorithm}
                        {r.algorithm === data.best_algorithm && <Badge tone="ember"> Best</Badge>}
                      </td>
                      <td className="mono">{r.n_clusters_found}</td>
                      <td className="mono">{r.silhouette_score.toFixed(3)}</td>
                      <td className="mono">{r.davies_bouldin_score.toFixed(3)}</td>
                      <td className="mono">{r.calinski_harabasz_score.toFixed(1)}</td>
                      <td className="mono">{r.noise_points || 0}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <div className="unsup-grid">
            <Card>
              <CardHeader title="Cluster visualization" subtitle={`${selectedAlgo} — projected to 2D via PCA`} />
              <CardBody>
                <ClusterScatterChart points={data.visualization.points} labels={selected?.labels} />
              </CardBody>
            </Card>
            <Card>
              <CardHeader title="Cluster sizes" subtitle={selectedAlgo} />
              <CardBody>
                {selected && Object.entries(selected.cluster_sizes)
                  .sort((a, b) => Number(a[0]) - Number(b[0]))
                  .map(([label, count]) => (
                    <div className="cluster-size-row" key={label}>
                      <span
                        className="cluster-size-swatch"
                        style={{ background: label === "-1" ? "var(--text-tertiary)" : SWATCHES[Number(label) % SWATCHES.length] }}
                      />
                      <span style={{ width: 70, flexShrink: 0 }}>{label === "-1" ? "Noise" : `Cluster ${label}`}</span>
                      <div className="cluster-size-bar-track">
                        <div
                          className="cluster-size-bar-fill"
                          style={{
                            width: `${(count / maxClusterSize) * 100}%`,
                            background: label === "-1" ? "var(--text-tertiary)" : SWATCHES[Number(label) % SWATCHES.length],
                          }}
                        />
                      </div>
                      <span className="cluster-size-count">{count}</span>
                    </div>
                  ))}
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
