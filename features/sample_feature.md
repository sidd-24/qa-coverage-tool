# Feature: User Authentication

## Description
Users can register, log in, and log out of the application.

## Acceptance Criteria
- User can register with email and password
- Password must be at least 8 characters
- User receives error on duplicate email
- User can log in with valid credentials
- User gets 401 on invalid credentials
- Session token expires after 24 hours
- User can log out and token is invalidated