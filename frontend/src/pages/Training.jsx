import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getJobStatus } from "../lib/api";
import { Card } from "../components/ui/Primitives";
import Button from "../components/ui/Button";
import "./Training.css";

export default function Training() {
  const { jobId } = useParams();
  const navigate = useNavigate();

  const [job, setJob] = useState(null);
  const [log, setLog] = useState([]);
  const [error, setError] = useState(null);
  const lastStage = useRef(null);

  useEffect(() => {
    let cancelled = false;
    let timer;

    async function poll() {
      try {
        const data = await getJobStatus(jobId);
        if (cancelled) return;

        setJob(data);

        if (data.stage && data.stage !== lastStage.current) {
          lastStage.current = data.stage;
          setLog((prev) => [...prev, data.stage]);
        }

        if (data.status === "completed") {
          const result = data.result;
          setTimeout(() => {
            if (cancelled || !result) return;
            if (result.mode === "clustering") {
              navigate(`/clustering/${result.dataset_name}`);
            } else if (result.mode === "dimensionality_reduction") {
              navigate(`/dimensionality-reduction/${result.dataset_name}`);
            } else if (result.dataset_name) {
              navigate(`/results/${result.dataset_name}`);
            }
          }, 900);
          return;
        }

        if (data.status === "failed") {
          setError(data.error || "Training failed for an unknown reason.");
          return;
        }

        timer = setTimeout(poll, 700);
      } catch (err) {
        if (!cancelled) setError(err.message);
      }
    }

    poll();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [jobId, navigate]);

  const progress = job?.progress ?? 0;

  return (
    <main className="page shell training-wrap">
      <div className="training-head">
        <h1>Training in progress</h1>
        <p>Every stage below reflects a model that is actually training right now.</p>
      </div>

      <Card className="training-card">
        <div className="progress-top">
          <span className="progress-pct">{progress}%</span>
          <span className="mono-tag">job {jobId.slice(0, 8)}</span>
        </div>
        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
        <p className="progress-stage">
          {job?.status === "completed" ? "Finalizing results…" : job?.stage || "Starting up…"}
        </p>

        {log.length > 0 && (
          <div className="stage-log">
            {log.map((stage, i) => (
              <div key={`${stage}-${i}`} className={`stage-log-row ${i === log.length - 1 ? "latest" : ""}`}>
                <svg className="tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="m20 6-11 11-5-5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                {stage}
              </div>
            ))}
          </div>
        )}

        {job?.status === "completed" && (
          <div className="training-success">
            <p style={{ fontSize: 13.5, color: "var(--success)", fontWeight: 600 }}>
              Training complete — opening results…
            </p>
          </div>
        )}

        {error && (
          <div className="training-error">
            <strong>Training failed.</strong> {error}
            <div style={{ marginTop: 12 }}>
              <Button variant="secondary" size="sm" onClick={() => navigate("/upload")}>
                Start over
              </Button>
            </div>
          </div>
        )}
      </Card>
    </main>
  );
}
