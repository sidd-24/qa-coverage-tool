// Reusable TypeScript test patterns
import { expect } from "@jest/globals";

export const assertValidToken = (token: string): void => {
  expect(token).toBeDefined();
  expect(token.length).toBeGreaterThan(10);
  expect(typeof token).toBe("string");
};

export const buildRegistrationPayload = (email: string, password: string) => ({
  email,
  password,
});

export const mockSuccessResponse = (data: object) => ({
  status: 200,
  data,
  error: null,
});

export const mockErrorResponse = (status: number, error: string) => ({
  status,
  data: null,
  error,
});