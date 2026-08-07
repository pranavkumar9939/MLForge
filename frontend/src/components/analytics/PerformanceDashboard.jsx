import { useEffect,useState} from "react";
import MetricsSection from "./sections/MetricsSection";
import ROCChart from "./charts/ROCChart";
import { getConfusionMatrix, getFeatureImportance, getROC } from "../../services/analyticsService";
import ConfusionMatrix from "./charts/ConfusionMatrix";
import FeatureImportanceChart from "./charts/FeatureImportanceChart";
import ControlPanel from "./controls/ControlPanel";
import "./PerformanceDashboard.css";
import { getDatasets } from "../../services/analyticsService";
import { getMetrics } from "../../services/analyticsService";
import { getSavedModels } from "../../services/analyticsService";
import Leaderboard from "./leaderboard/Leaderboard";
import { getLeaderboard } from "../../services/leaderboardService";

export default function PerformanceDashboard(){

    const [roc,setROC] = useState(null);
    const [matrix, setMatrix] = useState(null);
    const [featureImportance, setFeatureImportance] = useState(null);

    const [selectedDataset, setSelectedDataset] = useState("");
    const [selectedModel, setSelectedModel] = useState("Logistic Regression");

    const [datasets, setDatasets] = useState([]);
    const [metrics, setMetrics] = useState(null);

    const [models, setModels] = useState([]);
    const [leaderboard, setLeaderboard] = useState(null);

    useEffect(() => {

        getSavedModels().then(data => {

            console.log(data);

            const datasetList = data.datasets || [];

            setDatasets(datasetList);

            if (datasetList.length > 0) {

                setSelectedDataset(
                    datasetList[0].dataset_name
                );

            }

        });

    }, []); 

    useEffect(()=>{

        if(!selectedDataset) return;

        getROC(
            selectedDataset,
            selectedModel
        ).then(data=>{
        
            setROC(data.roc_curve);
        });

        getConfusionMatrix(
            selectedDataset,
            selectedModel
        ).then(data => {
            console.log(data);
            setMatrix(data.confusion_matrix)
        });

        getFeatureImportance(
            selectedDataset,
            selectedModel
        ).then(data => {

            console.log(data);

            if (Array.isArray(data.feature_importance)) {

                setFeatureImportance(
                    data.feature_importance
                );

            } else {

                setFeatureImportance([]);
            }
        });

        getMetrics(
            selectedDataset,
            selectedModel
        )
        .then(data => {
            setMetrics(data);
        })
        .catch(err => {
            console.error(err);
        });

        console.log(
        "Dataset:",
        selectedDataset,
        "Model:",
        selectedModel
    );

    getLeaderboard(
        selectedDataset
    ).then(data => {

        setLeaderboard(data);

    });


    },[selectedDataset, selectedModel]);

    useEffect(() => {

        if (!selectedDataset) return;

        const datasetInfo = datasets.find(
            d => d.dataset_name === selectedDataset
        );

        if (!datasetInfo) return;

        const modelNames =
            datasetInfo.models.map(
                m => m.model_name
            );

        setModels(modelNames);

        if (!modelNames.includes(selectedModel)) {
            setSelectedModel(modelNames[0]);
        }

    }, [selectedDataset, datasets]);

    return (

        <div className = "dashboard">

            <h1 className = "dashboard-title">
                Model Performance Dashboard
            </h1>

            <ControlPanel 
                datasets = {datasets}
                models = {models}

                selectedDataset = {selectedDataset}
                selectedModel = {selectedModel}

                onDatasetChange = {setSelectedDataset}
                onModelChange={(model)=>{
                    console.log("SELECTED MODEL:", model);
                    setSelectedModel(model);
                }}

            />

            <MetricsSection metrics = {metrics}/>

            {metrics?.problem_type !== "Regression" && (
                <>
                    <h2 className="section-title">📈 ROC Curve</h2>

                    <div className="chart-card">
                        <ROCChart rocData={roc} />
                    </div>
                </>
            )}

            {metrics?.problem_type !== "Regression" && (
                <>
                    <h2 className="section-title">
                        📊 Confusion Matrix
                    </h2>

                    <div className="chart-card">
                        <ConfusionMatrix matrix={matrix} />
                    </div>
                </>
            )}

            <h2 className="section-title">
                ⭐ Feature Importance
            </h2>

            <div className="chart-card">

                <FeatureImportanceChart
                    data = {featureImportance}
                />
            </div>

            <h2 className="section-title">
                🏆 Model Comparison
            </h2>

            <Leaderboard
                data = {leaderboard}
            />

        </div>
    );
}


// import MetricsSection from "./sections/MetricsSection";
// import ROCChart from "./charts/ROCChart";

// export default function PerformanceDashboard() {

//     // console.log("ROC DATA:", roc);

//     return (

//         <div style = {{padding: "30px"}}>

//             <h1>Model Performance Dashboard</h1>

//             <MetricsSection />

//             <h2>ROC Curve</h2>

//             <ROCChart />

//             <h2 style = {{marginTop: 60}}>
//                 Confusion Matrix
//             </h2>

//             <div 
//                 style = {{
//                     height: 300,
//                     border: "2px dashed lightgray",
//                     borderRadius: 10
//                 }}
//             />

//             <h2 style={{marginTop: 60}}>
//                 Feature Importance
//             </h2>

//             <div 
//                 style = {{
//                     height: 300,
//                     border: "2px dashed lightgray",
//                     borderRadius: 10
//                 }}
//             />
            
//         </div>
//     );
// }