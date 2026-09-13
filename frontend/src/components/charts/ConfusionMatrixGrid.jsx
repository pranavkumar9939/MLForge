import { EmptyState } from "../ui/Primitives";

export default function ConfusionMatrixGrid({ matrix }) {
  if (!matrix || !matrix.labels) {
    return <EmptyState title="Confusion matrix not available" description="This chart only applies to classification models." />;
  }

  const labels = matrix.labels;
  const values = matrix.matrix;
  const maxValue = Math.max(...values.flat());

  return (
    <div style={{ overflowX: "auto" }}>
      <table className="table" style={{ tableLayout: "fixed" }}>
        <thead>
          <tr>
            <th></th>
            {labels.map((label) => (
              <th key={label} style={{ textAlign: "center" }}>{label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {values.map((row, i) => (
            <tr key={i}>
              <th style={{ background: "var(--surface-2)", textTransform: "none", fontSize: 12.5 }}>
                {labels[i]}
              </th>
              {row.map((value, j) => {
                const intensity = maxValue ? value / maxValue : 0;
                const isDiagonal = i === j;
                return (
                  <td
                    key={j}
                    style={{
                      textAlign: "center",
                      fontFamily: "var(--font-mono)",
                      fontWeight: isDiagonal ? 700 : 500,
                      background: isDiagonal
                        ? `rgba(196, 80, 31, ${0.12 + intensity * 0.55})`
                        : `rgba(58, 107, 138, ${intensity * 0.35})`,
                      color: intensity > 0.55 ? "#fff" : "var(--text-primary)",
                    }}
                  >
                    {value}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
