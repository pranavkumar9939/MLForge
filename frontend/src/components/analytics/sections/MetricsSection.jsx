import MetricCard from "../cards/MetricCard";
import "./MetricsSection.css";

export default function MetricsSection({metrics}) {

    if(!metrics)
        return <p>Loading Metrics...</p>

    return (

        <div className="metrics-grid">

            <MetricCard
                title = "Accuracy"
                value = {`${metrics.accuracy}%`}
                color = "#2563EB"
                icon="🎯"
            />

            <MetricCard 
                title = "Precision"
                value = {`${metrics.precision}%`}
                color = "#16A34A"
                icon="📊"
            />

            <MetricCard 
                title = "Recall"
                value = {`${metrics.recall}%`}
                color = "#DC2626"
                icon="📥"
            />

            <MetricCard
                title = "F1 Score"
                value = {`${metrics.f1_score}%`}
                color = "#9333EA"
                icon="⭐"
            />
        </div>
    );
}