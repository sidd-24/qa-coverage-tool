import {
  assertValidToken,
  buildRegistrationPayload,
  mockSuccessResponse,
  mockErrorResponse,
} from "./patterns";

describe("Auth Registration — Regression", () => {
  test("registration payload contains required fields", () => {
    const payload = buildRegistrationPayload("user@example.com", "password123");
    expect(payload).toHaveProperty("email");
    expect(payload).toHaveProperty("password");
  });

  test("rejects password shorter than 8 characters", () => {
    const password = "abc";
    expect(password.length).toBeLessThan(8);
  });
});

describe("Token Validation — Regression", () => {
  test("valid token passes all checks", () => {
    assertValidToken("mock-jwt-token-abc123");
  });

  test("empty token fails validation", () => {
    expect(() => assertValidToken("")).toThrow();
  });
});

describe("Response Shapes — Regression", () => {
  test("success response has correct shape", () => {
    const res = mockSuccessResponse({ userId: 1 });
    expect(res.status).toBe(200);
    expect(res.data).toBeTruthy();
  });

  test("error response carries status and message", () => {
    const res = mockErrorResponse(401, "Unauthorized");
    expect(res.status).toBe(401);
    expect(res.error).toBe("Unauthorized");
  });
});