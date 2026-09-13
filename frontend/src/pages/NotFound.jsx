import { Link } from "react-router-dom";
import { EmptyState } from "../components/ui/Primitives";
import Button from "../components/ui/Button";

export default function NotFound() {
  return (
    <main className="page shell" style={{ display: "flex", justifyContent: "center" }}>
      <EmptyState
        title="Page not found"
        description="The page you're looking for doesn't exist."
        action={<Link to="/"><Button variant="primary">Back to home</Button></Link>}
      />
    </main>
  );
}
