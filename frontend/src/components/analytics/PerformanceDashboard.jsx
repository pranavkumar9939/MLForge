import { useEffect,useState} from "react";
import ROCChart from "./ROCChart";
import { getROC } from "../../services/analyticsService";

export default function PerformanceDashboard(){

    const [roc,setROC] = useState(null);

    useEffect(()=>{

        getROC(
            "DateFruit_Dataset",
            "Logistic Regression"
        ).then(data=>{
            console.log(data);

            console.log(data.roc_curve);

            setROC(data.roc_curve);
        });
    },[]);

    return (

        <div>

            <h2>ROC Curve</h2>

            <ROCChart rocData={roc}/>

        </div>
    );
}