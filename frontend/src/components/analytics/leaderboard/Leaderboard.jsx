import "./Leaderboard.css";

export default function Leaderboard({data}) {

    if (!data) return null;

    return (

        <div className = "leaderboard-container">

            <h2>
                🏆 Model Leaderboard
            </h2>

            <table className = "leaderboard-table">

                <thead>

                    <tr>

                        <th>Rank</th>
                        <th>Model</th>
                        <th>Score</th>
                        <th>Status</th>

                    </tr>

                </thead>

                <tbody>

                    {data.leaderboard.map(model => (

                        <tr
                            key = {model.model_name}
                            className = {
                                model.rank === 1
                                    ? "winner-row"
                                    : ""
                            }
                        >

                            <td>

                                {model.rank === 1 && "🥇"}
                                {model.rank === 2 && "🥈"}
                                {model.rank === 3 && "🥉"}

                                {model.rank > 3 && model.rank}

                            </td>

                            <td>

                                {model.model_name}

                            </td>

                            <td>

                                {model.overall_score}

                            </td>

                            <td>

                                {model.status}

                            </td>

                        </tr>

                    ))}
                    
                </tbody>

            </table>

        </div>
    );
}