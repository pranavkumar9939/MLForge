
import { Routes, Route, useLocation } from "react-router-dom";
import { useEffect } from "react";

import AppShell from "./components/layout/AppShell";
import RequireAuth from "./components/layout/RequireAuth";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Training from "./pages/Training";
import Results from "./pages/Results";
import ClusteringResults from "./pages/ClusteringResults";
import DimensionalityReductionResults from "./pages/DimensionalityReductionResults";
import Predict from "./pages/Predict";
import NotFound from "./pages/NotFound";
import { trackPageview } from "./pages/Analytics";

function App() {
  const location = useLocation();

  useEffect(() => {
    trackPageview(location.pathname);
  }, [location.pathname]);

  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />

        <Route
          path="/upload"
          element={
            <RequireAuth>
              <Upload />
            </RequireAuth>
          }
        />

        <Route
          path="/training/:jobId"
          element={
            <RequireAuth>
              <Training />
            </RequireAuth>
          }
        />

        <Route
          path="/results/:datasetName"
          element={
            <RequireAuth>
              <Results />
            </RequireAuth>
          }
        />

        <Route
          path="/clustering/:datasetName"
          element={
            <RequireAuth>
              <ClusteringResults />
            </RequireAuth>
          }
        />

        <Route
          path="/dimensionality-reduction/:datasetName"
          element={
            <RequireAuth>
              <DimensionalityReductionResults />
            </RequireAuth>
          }
        />

        <Route
          path="/predict/:datasetName/:modelName"
          element={
            <RequireAuth>
              <Predict />
            </RequireAuth>
          }
        />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </AppShell>
  );
}

export default App;

