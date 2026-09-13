import { describe, it, expect, vi, beforeEach } from "vitest";

// Mock axios BEFORE importing the api module, since api.js calls
// axios.create() at module load time.
const mockGet = vi.fn();
const mockPost = vi.fn();

vi.mock("axios", () => ({
  default: {
    create: () => ({
      get: mockGet,
      post: mockPost,
      interceptors: { request: { use: vi.fn() } },
    }),
  },
}));

describe("api.js token storage", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("getToken returns null when nothing is stored", async () => {
    const { getToken } = await import("../../lib/api");
    expect(getToken()).toBeNull();
  });

  it("setToken stores and getToken retrieves it", async () => {
    const { getToken, setToken } = await import("../../lib/api");
    setToken("abc123");
    expect(getToken()).toBe("abc123");
  });

  it("setToken(null) clears a stored token", async () => {
    const { getToken, setToken } = await import("../../lib/api");
    setToken("abc123");
    setToken(null);
    expect(getToken()).toBeNull();
  });
});

describe("api.js error normalization (unwrap)", () => {
  beforeEach(() => {
    mockGet.mockReset();
    mockPost.mockReset();
  });

  it("resolves with response data on success", async () => {
    mockGet.mockResolvedValue({ data: { status: "ok" } });
    const { checkHealth } = await import("../../lib/api");
    const result = await checkHealth();
    expect(result).toEqual({ status: "ok" });
  });

  it("surfaces a plain string `detail` as the error message", async () => {
    mockGet.mockRejectedValue({ response: { data: { detail: "Dataset not found." } } });
    const { checkHealth } = await import("../../lib/api");
    await expect(checkHealth()).rejects.toThrow("Dataset not found.");
  });

  it("joins FastAPI/Pydantic validation error arrays into one readable message", async () => {
    mockGet.mockRejectedValue({
      response: {
        data: {
          detail: [
            { msg: "Value error, Password must be at least 8 characters long." },
            { msg: "field required" },
          ],
        },
      },
    });
    const { checkHealth } = await import("../../lib/api");
    await expect(checkHealth()).rejects.toThrow(
      "Value error, Password must be at least 8 characters long. field required"
    );
  });

  it("falls back to a generic message when there is no response at all (network error)", async () => {
    mockGet.mockRejectedValue({ message: "Network Error" });
    const { checkHealth } = await import("../../lib/api");
    await expect(checkHealth()).rejects.toThrow("Network Error");
  });

  it("falls back to a generic message when the error has neither detail nor message", async () => {
    mockGet.mockRejectedValue({});
    const { checkHealth } = await import("../../lib/api");
    await expect(checkHealth()).rejects.toThrow("Something went wrong talking to the MLForge server.");
  });
});
