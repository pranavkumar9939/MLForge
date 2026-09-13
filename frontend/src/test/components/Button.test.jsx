import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Button from "../../components/ui/Button";

describe("Button", () => {
  it("renders its children", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: "Click me" })).toBeInTheDocument();
  });

  it("applies the requested variant class", () => {
    render(<Button variant="danger">Delete</Button>);
    expect(screen.getByRole("button")).toHaveClass("btn-danger");
  });

  it("defaults to the primary variant", () => {
    render(<Button>Default</Button>);
    expect(screen.getByRole("button")).toHaveClass("btn-primary");
  });

  it("calls onClick when clicked", async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Go</Button>);

    await user.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("is disabled and shows a spinner while loading", () => {
    render(<Button loading>Saving</Button>);
    const button = screen.getByRole("button");
    expect(button).toBeDisabled();
    expect(button.querySelector(".spinner")).toBeInTheDocument();
  });

  it("does not fire onClick when disabled", async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    render(<Button disabled onClick={handleClick}>Blocked</Button>);

    await user.click(screen.getByRole("button"));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it("applies the block class for full-width buttons", () => {
    render(<Button block>Wide</Button>);
    expect(screen.getByRole("button")).toHaveClass("btn-block");
  });
});
