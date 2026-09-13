import { Link } from "react-router-dom";
import { Card } from "../components/ui/Primitives";
import Button from "../components/ui/Button";
import "./Landing.css";

const PIPELINE_STEPS = [
  { title: "Upload", desc: "Drop in a CSV or Excel file. No cleanup required first." },
  { title: "Analyze", desc: "MLForge profiles every column — types, missing values, cardinality, outliers." },
  { title: "Confirm target", desc: "MLForge recommends a target column with reasons. You confirm or override it." },
  { title: "Train", desc: "A dozen candidate algorithms train in parallel with cross-validation and tuning." },
  { title: "Evaluate", desc: "Every model is scored, ranked on a leaderboard, and explained." },
  { title: "Predict", desc: "Use the best model on new data — one row at a time or in bulk." },
];

const FEATURES = [
  {
    title: "Real problem detection",
    body: "MLForge inspects your target column's type and cardinality to pick binary, multiclass, or regression — never guessed blindly.",
  },
  {
    title: "A real algorithm library",
    body: "Linear models, trees, ensembles, and gradient boosting all compete on your dataset, not just one default model.",
  },
  {
    title: "Leakage-safe preprocessing",
    body: "Scalers and encoders fit only on training data. Cross-validation runs only on the training split.",
  },
  {
    title: "Explainability built in",
    body: "SHAP-based feature attribution for every prediction, plus global feature importance for every model.",
  },
  {
    title: "No fake progress",
    body: "Training progress reflects the model that's actually running right now — not a decorative timer.",
  },
  {
    title: "Transparent by default",
    body: "Dropped columns, encoding choices, and skipped models are always shown with the reason why.",
  },
];

const ALGORITHMS = [
  "Logistic Regression", "Decision Tree", "Random Forest", "Extra Trees",
  "Gradient Boosting", "HistGradientBoosting", "AdaBoost", "Naive Bayes",
  "KNN", "SVM", "Linear / Ridge / Lasso / ElasticNet", "SVR",
];

export default function Landing() {
  return (
    <main className="page">
      <section className="hero shell">
        <div className="hero-grid">
          <div>
            <div className="hero-eyebrow">
              <span className="mono-tag">AutoML platform</span>
            </div>
            <h1>
              Upload a dataset.<br />Walk away with a <em>tuned, explained model.</em>
            </h1>
            <p className="hero-sub">
              MLForge runs the entire machine-learning workflow — analysis, preprocessing,
              algorithm selection, training, tuning, evaluation, and explainability — so you
              can focus on the questions your data raises, not the boilerplate.
            </p>
            <div className="hero-actions">
              <Link to="/upload"><Button variant="primary" size="lg">Upload a dataset</Button></Link>
              <Link to="/dashboard"><Button variant="secondary" size="lg">View past experiments</Button></Link>
            </div>
            <p className="hero-note">CSV or Excel. Works with binary, multiclass, and regression problems.</p>
          </div>

          <div className="hero-panel">
            {PIPELINE_STEPS.map((s, i) => (
              <div key={s.title} className={`hero-panel-row ${i === 3 ? "active" : ""}`}>
                <span className="step-num">{String(i + 1).padStart(2, "0")}</span>
                <span className="dot" />
                <span>{s.title}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section shell">
        <div className="section-head">
          <span className="eyebrow">Why MLForge</span>
          <h2>Built to be trusted, not just demoed.</h2>
          <p>Every number on the leaderboard comes from an actual evaluation run — nothing here is hardcoded or simulated.</p>
        </div>
        <div className="grid-3">
          {FEATURES.map((f) => (
            <Card key={f.title} className="feature-card">
              <div className="feature-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 6 9 17l-5-5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <h4>{f.title}</h4>
              <p>{f.body}</p>
            </Card>
          ))}
        </div>
      </section>

      <section className="section shell">
        <div className="section-head">
          <span className="eyebrow">The workflow</span>
          <h2>From raw file to production-ready model.</h2>
        </div>
        <div>
          {PIPELINE_STEPS.map((s, i) => (
            <div className="workflow-step" key={s.title}>
              <span className="workflow-num">{String(i + 1).padStart(2, "0")}</span>
              <div>
                <h4>{s.title}</h4>
                <p>{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="section shell" style={{ borderBottom: "none" }}>
        <div className="section-head">
          <span className="eyebrow">Algorithm library</span>
          <h2>A dozen candidate models compete on your data.</h2>
          <p>Computationally expensive models (SVM, KNN) are automatically skipped on very large datasets.</p>
        </div>
        <div className="algo-cloud">
          {ALGORITHMS.map((a) => (
            <span className="algo-pill" key={a}>{a}</span>
          ))}
        </div>
      </section>

      <section className="cta-band shell">
        <h2>Ready to forge your first model?</h2>
        <p>It takes one upload to see the whole pipeline run.</p>
        <div className="hero-actions">
          <Link to="/upload"><Button variant="primary" size="lg">Get started</Button></Link>
        </div>
      </section>
    </main>
  );
}
