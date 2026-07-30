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


export default function PerformanceDashboard(){

    const [roc,setROC] = useState(null);
    const [matrix, setMatrix] = useState(null);
    const [featureImportance, setFeatureImportance] = useState(null);

    const [selectedDataset, setSelectedDataset] = useState("");
    const [selectedModel, setSelectedModel] = useState("Logistic Regression");

    const [datasets, setDatasets] = useState([]);
    const [metrics, setMetrics] = useState(null);

    const [models] = useState([
        "Logistic Regression"
    ]);

    useEffect(() => {

        // console.log("Datasets: ", data);

        getDatasets().then(data => {
            setDatasets(data);

            if (data.length > 0){
                setSelectedDataset(data[0]);
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

            setFeatureImportance(
                data.feature_importance
            )
        });

        getMetrics(
            selectedDataset,
            selectedModel
        ).then(data => {
            console.log("Metrics:", data);

            setMetrics(data);

        });


    },[selectedDataset, selectedModel]);

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
                onModelChange = {setSelectedModel}

            />

            <MetricsSection metrics = {metrics}/>

            <h2 className="section-title">📈 ROC Curve</h2>

            <div className="chart-card">

                <ROCChart rocData={roc} />

            </div>

            <h2 className="section-title">
                📊 Confusion Matrix
            </h2>

            <div className="chart-card">

                <ConfusionMatrix matrix={matrix} />

            </div>

            <h2 className="section-title">
                ⭐ Feature Importance
            </h2>

            <div className="chart-card">

                <FeatureImportanceChart
                    data = {featureImportance}
                />
            </div>

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