import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { AuthProvider } from "../../context/AuthContext";
import { useAuth } from "../../context/useAuth";

const mockLogin = vi.fn();
const mockSignup = vi.fn();
const mockGetMe = vi.fn();
let storedToken = null;

vi.mock("../../lib/api", () => ({
  getToken: () => storedToken,
  setToken: (t) => { storedToken = t; },
  login: (...args) => mockLogin(...args),
  signup: (...args) => mockSignup(...args),
  getMe: (...args) => mockGetMe(...args),
}));

function Probe() {
  const { user, isAuthenticated, login, signup, logout, loading } = useAuth();
  return (
    <div>
      <div data-testid="loading">{String(loading)}</div>
      <div data-testid="authed">{String(isAuthenticated)}</div>
      <div data-testid="user">{user ? user.email : "none"}</div>
      <button onClick={() => login({ email: "a@b.com", password: "x" })}>login</button>
      <button onClick={() => signup({ name: "A", email: "a@b.com", password: "x" })}>signup</button>
      <button onClick={logout}>logout</button>
    </div>
  );
}

describe("AuthContext", () => {
  beforeEach(() => {
    storedToken = null;
    mockLogin.mockReset();
    mockSignup.mockReset();
    mockGetMe.mockReset();
  });

  it("starts unauthenticated with no stored token", () => {
    render(<AuthProvider><Probe /></AuthProvider>);
    expect(screen.getByTestId("authed").textContent).toBe("false");
    expect(screen.getByTestId("user").textContent).toBe("none");
  });

  it("login() stores the user and flips isAuthenticated", async () => {
    mockLogin.mockResolvedValue({
      access_token: "tok123",
      user: { id: 1, name: "Alice", email: "a@b.com" },
    });
    const user = userEvent.setup();
    render(<AuthProvider><Probe /></AuthProvider>);

    await user.click(screen.getByText("login"));

    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("true"));
    expect(screen.getByTestId("user").textContent).toBe("a@b.com");
    expect(storedToken).toBe("tok123");
  });

  it("signup() stores the user the same way login does", async () => {
    mockSignup.mockResolvedValue({
      access_token: "tok456",
      user: { id: 2, name: "Bob", email: "a@b.com" },
    });
    const user = userEvent.setup();
    render(<AuthProvider><Probe /></AuthProvider>);

    await user.click(screen.getByText("signup"));

    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("true"));
    expect(storedToken).toBe("tok456");
  });

  it("logout() clears the user and token", async () => {
    mockLogin.mockResolvedValue({
      access_token: "tok123",
      user: { id: 1, name: "Alice", email: "a@b.com" },
    });
    const user = userEvent.setup();
    render(<AuthProvider><Probe /></AuthProvider>);

    await user.click(screen.getByText("login"));
    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("true"));

    await user.click(screen.getByText("logout"));
    expect(screen.getByTestId("authed").textContent).toBe("false");
    expect(storedToken).toBeNull();
  });

  it("logs the user out automatically if the stored token turns out to be invalid", async () => {
    storedToken = "stale-token";
    mockGetMe.mockRejectedValue(new Error("401"));

    render(<AuthProvider><Probe /></AuthProvider>);

    await waitFor(() => expect(screen.getByTestId("loading").textContent).toBe("false"));
    expect(storedToken).toBeNull();
  });

  it("useAuth throws when used outside an AuthProvider", () => {
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(() => render(<Probe />)).toThrow("useAuth must be used within an AuthProvider");
    consoleError.mockRestore();
  });
});
