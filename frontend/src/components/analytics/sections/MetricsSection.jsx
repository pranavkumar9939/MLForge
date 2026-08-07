import MetricCard from "../cards/MetricCard";
import "./MetricsSection.css";

export default function MetricsSection({ metrics }) {

    if (!metrics)
        return <p>Loading Metrics...</p>;

    const isRegression =
        metrics.problem_type === "Regression";

    return (

        <div className="metrics-grid">

            {isRegression ? (

                <>

                    <MetricCard
                        title="R² Score"
                        value={`${metrics.r2_score * 100}%`}
                        color="#2563EB"
                        icon="📈"
                    />

                    <MetricCard
                        title="MAE"
                        value={metrics.mae}
                        color="#16A34A"
                        icon="📊"
                    />

                    <MetricCard
                        title="RMSE"
                        value={metrics.rmse}
                        color="#DC2626"
                        icon="📉"
                    />

                    <MetricCard
                        title="Status"
                        value={metrics.status}
                        color="#9333EA"
                        icon="⭐"
                    />

                </>

            ) : (

                <>

                    <MetricCard
                        title="Accuracy"
                        value={`${metrics.accuracy}%`}
                        color="#2563EB"
                        icon="🎯"
                    />

                    <MetricCard
                        title="Precision"
                        value={`${metrics.precision}%`}
                        color="#16A34A"
                        icon="📊"
                    />

                    <MetricCard
                        title="Recall"
                        value={`${metrics.recall}%`}
                        color="#DC2626"
                        icon="📥"
                    />

                    <MetricCard
                        title="F1 Score"
                        value={`${metrics.f1_score}%`}
                        color="#9333EA"
                        icon="⭐"
                    />

                </>

            )}

        </div>

    );
}