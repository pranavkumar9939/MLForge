import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ZAxis } from "recharts";
import { EmptyState } from "../ui/Primitives";

const SERIES_COLORS = [
  "var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)",
  "var(--series-5)", "var(--series-6)", "var(--series-7)", "var(--series-8)",
];
const NOISE_COLOR = "var(--text-tertiary)";

/**
 * points: [[x, y], ...]
 * labels: optional array of cluster ids (same length as points). -1 = noise.
 * If labels is omitted, every point is drawn in a single color.
 */
export default function ClusterScatterChart({ points, labels }) {
  if (!points || points.length === 0) {
    return <EmptyState title="No points to plot" />;
  }

  const groups = new Map();
  points.forEach((p, i) => {
    const label = labels ? labels[i] : 0;
    if (!groups.has(label)) groups.set(label, []);
    groups.get(label).push({ x: p[0], y: p[1] });
  });

  const sortedLabels = [...groups.keys()].sort((a, b) => a - b);

  return (
    <ResponsiveContainer width="100%" height={380}>
      <ScatterChart margin={{ top: 8, right: 20, left: 0, bottom: 8 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis type="number" dataKey="x" tick={{ fontSize: 11, fill: "var(--text-tertiary)" }} name="Component 1" />
        <YAxis type="number" dataKey="y" tick={{ fontSize: 11, fill: "var(--text-tertiary)" }} name="Component 2" />
        <ZAxis range={[45, 45]} />
        <Tooltip cursor={{ strokeDasharray: "3 3" }} contentStyle={{ fontSize: 12.5, borderRadius: 6, border: "1px solid var(--border)" }} />
        {sortedLabels.map((label) => (
          <Scatter
            key={label}
            name={label === -1 ? "Noise" : `Cluster ${label}`}
            data={groups.get(label)}
            fill={label === -1 ? NOISE_COLOR : SERIES_COLORS[label % SERIES_COLORS.length]}
            fillOpacity={label === -1 ? 0.4 : 0.75}
          />
        ))}
      </ScatterChart>
    </ResponsiveContainer>
  );
}
