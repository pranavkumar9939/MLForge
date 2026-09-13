import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Badge, ProgressBar, EmptyState, Card, CardHeader } from "../../components/ui/Primitives";

describe("Badge", () => {
  it("renders its children with the requested tone class", () => {
    render(<Badge tone="success">Done</Badge>);
    const badge = screen.getByText("Done");
    expect(badge).toHaveClass("badge-success");
  });

  it("defaults to the neutral tone", () => {
    render(<Badge>Plain</Badge>);
    expect(screen.getByText("Plain")).toHaveClass("badge-neutral");
  });
});

describe("ProgressBar", () => {
  it("renders a fill width matching the given value", () => {
    const { container } = render(<ProgressBar value={42} />);
    const fill = container.querySelector(".progress-fill");
    expect(fill).toHaveStyle({ width: "42%" });
  });

  it("clamps values above 100 down to 100%", () => {
    const { container } = render(<ProgressBar value={250} />);
    expect(container.querySelector(".progress-fill")).toHaveStyle({ width: "100%" });
  });

  it("clamps negative values up to 0%", () => {
    const { container } = render(<ProgressBar value={-30} />);
    expect(container.querySelector(".progress-fill")).toHaveStyle({ width: "0%" });
  });
});

describe("EmptyState", () => {
  it("renders title and description", () => {
    render(<EmptyState title="Nothing here" description="Try uploading a file." />);
    expect(screen.getByText("Nothing here")).toBeInTheDocument();
    expect(screen.getByText("Try uploading a file.")).toBeInTheDocument();
  });

  it("renders an action node when provided", () => {
    render(<EmptyState title="Empty" action={<button>Retry</button>} />);
    expect(screen.getByRole("button", { name: "Retry" })).toBeInTheDocument();
  });
});

describe("Card / CardHeader", () => {
  it("renders a title and optional subtitle", () => {
    render(<CardHeader title="Results" subtitle="12 models compared" />);
    expect(screen.getByText("Results")).toBeInTheDocument();
    expect(screen.getByText("12 models compared")).toBeInTheDocument();
  });

  it("Card renders children inside a card wrapper", () => {
    const { container } = render(<Card>content</Card>);
    expect(container.querySelector(".card")).toBeInTheDocument();
    expect(container.querySelector(".card")).toHaveTextContent("content");
  });
});
