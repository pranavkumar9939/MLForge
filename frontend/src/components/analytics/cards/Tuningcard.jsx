import "./TuningCard.css";

export default function TuningCard({
    data
}){
    if(!data){

        return (
            <div className = "tuning-card">
                Loading tuning results...
            </div>
        );
    }

    return (
        <div className = "tuning-card">

            <h3>
                ⚙ Hyperparameter Optimization
            </h3>

            <div className = "cv-score">

                Best CV Score

                <span>
                    {

                        data.best_cv_score
                        ?
                        `${(
                            data.best_cv_score * 100
                        ).toFixed(2)}%`
                        :
                        "N/A"
                    }

                </span>

            </div>
            
            <table className = "params-table">

                <tbody>

                    {
                        Object.entries(
                            data.best_params || {}
                        ).map(([key,value]) => (

                            <tr key = {key}>

                                <td>{key}</td>
                                <td>{String(value)}</td>

                            </tr>

                        ))
                    }

                </tbody>

            </table>

        </div>
    );

}