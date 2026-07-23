// import { BrowserRouter, Routes, Route  } from "react-router-dom";

// function Dashboard(){
//   return (
//     <div style={{ padding: "40px" }}>
//       <h1>🚀 MLForge Dashboard</h1>
//       <p>Your Ml platform is running successfully.</p>
//     </div>
//   );
// }

// function App() {
//   return (
//     <BrowserRouter>
//       <Routes>
//         <Route path="/" element={<Dashboard />} />
//       </Routes>
//     </BrowserRouter>
//   );
// }

// export default App;


import PerformanceDashboard from "./components/analytics/PerformanceDashboard";

function App() {
    return (
        <div>

            <PerformanceDashboard />

        </div>
    );
}

export default App;