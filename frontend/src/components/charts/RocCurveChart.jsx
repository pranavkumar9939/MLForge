import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { EmptyState } from "../ui/Primitives";

const SERIES_COLORS = [
  "var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)",
  "var(--series-5)", "var(--series-6)", "var(--series-7)", "var(--series-8)",
];

export default function RocCurveChart({ rocData }) {
  if (!rocData || !rocData.curves) {
    return <EmptyState title="ROC curve not available" description="This chart only applies to classification models." />;
  }

  const curves = rocData.curves;
  const maxLength = Math.max(...curves.map((c) => c.fpr.length));
  const chartData = [];

  for (let i = 0; i < maxLength; i++) {
    const row = {};
    curves.forEach((curve) => {
      row[`${curve.class}_fpr`] = curve.fpr[i];
      row[curve.class] = curve.tpr[i];
    });
    chartData.push(row);
  }

  return (
    <ResponsiveContainer width="100%" height={360}>
      <LineChart data={chartData} margin={{ top: 8, right: 20, left: 0, bottom: 8 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis
          dataKey={`${curves[0].class}_fpr`}
          type="number"
          domain={[0, 1]}
          tick={{ fontSize: 11, fill: "var(--text-tertiary)" }}
          label={{ value: "False Positive Rate", position: "insideBottom", offset: -4, fontSize: 12, fill: "var(--text-tertiary)" }}
        />
        <YAxis
          domain={[0, 1]}
          tick={{ fontSize: 11, fill: "var(--text-tertiary)" }}
          label={{ value: "True Positive Rate", angle: -90, position: "insideLeft", fontSize: 12, fill: "var(--text-tertiary)" }}
        />
        <Tooltip contentStyle={{ fontSize: 12.5, borderRadius: 6, border: "1px solid var(--border)" }} />
        <Legend wrapperStyle={{ fontSize: 12.5 }} />
        {curves.map((curve, index) => (
          <Line
            key={curve.class}
            type="monotone"
            dataKey={curve.class}
            stroke={SERIES_COLORS[index % SERIES_COLORS.length]}
            dot={false}
            strokeWidth={2}
            name={`${curve.class} (AUC ${curve.auc.toFixed(3)})`}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
