import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { EmptyState } from "../ui/Primitives";

export default function FeatureImportanceBar({ data }) {
  if (!data || data.length === 0) {
    return <EmptyState title="Feature importance not available" description="This model does not expose a global importance score." />;
  }

  const sorted = [...data].sort((a, b) => b.importance - a.importance).slice(0, 12);

  return (
    <ResponsiveContainer width="100%" height={Math.max(260, sorted.length * 34)}>
      <BarChart data={sorted} layout="vertical" margin={{ top: 4, right: 24, left: 8, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
        <XAxis type="number" tick={{ fontSize: 11, fill: "var(--text-tertiary)" }} />
        <YAxis
          type="category"
          dataKey="feature"
          width={140}
          tick={{ fontSize: 12, fill: "var(--text-secondary)" }}
        />
        <Tooltip contentStyle={{ fontSize: 12.5, borderRadius: 6, border: "1px solid var(--border)" }} />
        <Bar dataKey="importance" fill="var(--series-1)" radius={[0, 3, 3, 0]} maxBarSize={16} />
      </BarChart>
    </ResponsiveContainer>
  );
}
