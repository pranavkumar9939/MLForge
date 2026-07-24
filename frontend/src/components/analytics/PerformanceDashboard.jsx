import { useEffect,useState} from "react";
import MetricsSection from "./sections/MetricsSection";
import ROCChart from "./charts/ROCChart";
import { getConfusionMatrix, getFeatureImportance, getROC } from "../../services/analyticsService";
import ConfusionMatrix from "./charts/ConfusionMatrix";
import FeatureImportanceChart from "./charts/FeatureImportanceChart";

export default function PerformanceDashboard(){

    const [roc,setROC] = useState(null);
    const [matrix, setMatrix] = useState(null);
    const [featureImportance, setFeatureImportance] = useState(null);

    useEffect(()=>{

        getROC(
            "DateFruit_Dataset",
            "Logistic Regression"
        ).then(data=>{
        
            setROC(data.roc_curve);
        });

        getConfusionMatrix(
            "DateFruit_Dataset",
            "Logistic Regression"
        ).then(data => {
            console.log(data);
            setMatrix(data.confusion_matrix)
        });

        getFeatureImportance(
            "DateFruit_Dataset",
            "Logistic Regression"
        ).then(data => {

            console.log(data);

            setFeatureImportance(
                data.feature_importance
            )
        });

    },[]);

    return (

        <div style = {{padding: "30px"}}>

            <h1>Model Performance Dashboard</h1>

            <MetricsSection />

            <h2>ROC Curve</h2>

            <ROCChart rocData={roc} />

            <h2 style = {{marginTop: 60}}>
                Confusion Matrix
            </h2>

            <ConfusionMatrix matrix={matrix} />

            <h2 style = {{marginTop : 60}}>
                Feature Importance
            </h2>

            <FeatureImportanceChart
                data = {featureImportance}
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