import "./ConfusionMatrix.css";

export default function ConfusionMatrix({ matrix }) {

    if (!matrix) return <p>Loading Confusion Matrix...</p>;

    const labels = matrix.labels;
    const values = matrix.matrix;

    const maxValue = Math.max(
        ...values.flat()
    );

    console.log(matrix);

    return (

        <div className="cm-container">

            <table className="cm-table">

                <thead>

                    <tr>

                        <th> </th>

                            {labels.map(label => (
                                <th key={label}>{label}</th>
                            ))}

                    </tr>

                </thead>

                <tbody>

                    {values.map((row, i) => (

                        <tr key={i}>

                            <th>{labels[i]}</th>

                            {row.map((value, j) => {

                                const intensity = value / maxValue;

                                return (

                                    <td 

                                        key = {j}

                                        style = {{
                                            backgroundColor:
                                                    `rgba(37,99,235,${intensity})`,
                                            color:
                                                intensity > 0.5
                                                    ? "white"
                                                    : "black"
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