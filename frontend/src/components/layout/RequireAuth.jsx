import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../../context/useAuth";
import { Card, EmptyState } from "../ui/Primitives";

export default function RequireAuth({ children }) {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <main className="page shell">
        <Card padded><EmptyState title="Loading…" /></Card>
      </main>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
