import "./MetricCard.css";

export default function MetricCard({title, value, color = "#2563EB", icon}) {
    return (
        <div className = "metric-card">
            <div 
                className = "metric-strip"
                style = {{backgroundColor: color}}
            />

            <div className="metric-content">
                <p className="metric-title">
                    {icon} {title}
                </p>

                <h2 className="metric-value">
                    {value}
                </h2>
            </div>
        </div>
    );
}