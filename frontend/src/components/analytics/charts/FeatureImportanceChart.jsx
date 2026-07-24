import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip
} from "recharts";

export default function FeatureImportanceChart({ data }) {

    if(!data) return <p>Loading Feature Importance...</p>

    console.log(data);

    return (

        <ResponsiveContainer
            width = "100%"
            height = {450}
        >

            <BarChart
                data = {data}
                layout = "vertical"
                margin = {{
                    top: 20,
                    right: 30,
                    left: 120,
                    bottom: 20
                }}
            >

                <CartesianGrid strokeDasharray= "3 3"/>

                <XAxis type = "number"/>

                <YAxis
                    type = "category"
                    dataKey = "feature"
                    width = {180}
                />

                <Tooltip/>

                <Bar
                    dataKey = "importance"
                    fill = "#2563EB"
                />
            </BarChart>

        </ResponsiveContainer>
    );
}