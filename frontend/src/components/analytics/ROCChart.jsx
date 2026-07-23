import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
} from "recharts";

const COLORS = [
    "#2563EB",
    "#16A34A",
    "#DC2626",
    "#9333EA",
    "#F59E0B",
    "#06B6D4",
    "#EC4899",
    "#84CC16",
    "#F97316"
];

export default function ROCChart({ rocData }){

    if(!rocData) return null;

    const curves = rocData.curves;

    const maxLength = Math.max(
        ...curves.map(curve => curve.fpr.length)
    );

    const chartData = [];

    for (let i = 0; i < maxLength; i++){

        const row = {};

        curves.forEach(curve => {

            row[`${curve.class}_fpr`] = curve.fpr[i];
            row[curve.class] = curve.tpr[i];
        });

        chartData.push(row);
    }

    return (

        <ResponsiveContainer width="100%" height={500}>

            <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis 
                    dataKey={`${curves[0].class}_fpr`}
                    type="number"
                    domain={[0,1]}
                    label={{
                        value:"False Positive Rate",
                        position:"insideBottom",
                        offset:-5
                    }}
                />

                <YAxis 
                    domain={[0,1]}
                    label={{
                        value:"True Positive Rate",
                        angle:-90,
                        position:"insideLeft"
                    }}
                />

                <Tooltip />
                
                <Legend />

                {curves.map((curve,index)=>(
                    <Line
                        key={curve.class}
                        type="monotone"
                        dataKey={curve.class}
                        stroke={COLORS[index % COLORS.length]}
                        dot={false}
                        strokeWidth={3}
                        name={`${curve.class} (AUC ${curve.auc.toFixed(3)})`}
                    />
                ))}
            </LineChart>
        </ResponsiveContainer>
    );
}