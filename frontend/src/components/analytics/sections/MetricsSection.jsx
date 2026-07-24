import MetricCard from "../cards/MetricCard";
import "./MetricsSection.css";

export default function MetricsSection() {

    return (

        <div className="metrics-grid">

            <MetricCard
                title = "Accuracy"
                value = "98.2%"
                color = "#2563EB"
            />

            <MetricCard 
                title = "Precision"
                value = "97.8%"
                color = "#16A34A"
            />

            <MetricCard 
                title = "Recall"
                value = "97.1%"
                color = "#DC2626"
            />

            <MetricCard
                title = "F1 Score"
                value = "97.4%"
                color = "#9333EA"
            />
        </div>
    );
}