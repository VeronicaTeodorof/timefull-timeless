# TESTING.md — timefull-timeless
# Table of Contents

1. [Pass 1 - Code Audit](#pass-1--code-audit)
   - [Automated tests](#automated-tests)
   - [Manual tests - code reflection in UI](#manual-tests--code-reflection-in-ui)

2. [Pass 2 - User-Perspective Testing](#pass-2--user-perspective-testing)
   - [Repeating categories](#repeating-categories)
   - [Per-feature tests](#per-feature-tests)
     - [Authentication (AUTH)](#authentication-auth)
3. [Story-to-Test Mapping](#story-to-test-mapping)
4. [Solved Bugs](#solved-bugs)
5. [Known Bugs / Limitations](#known-bugs--limitations)
6. [Validation](#validation)
---


## Pass 1 — Code Audit

### Automated tests

---

### Manual tests — code reflection in UI

---

## Pass 2 — User-Perspective Testing

### Repeating categories

---

### Per-feature tests

#### Authentication (AUTH)


| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|-------|-------|------------|
| AUTH-01 | Sign up with valid data | Loads Confirm Emai page | As expected | Pass | |
| AUTH-02 | Paste confirmation link url in browser (obtained via console backend) | Loads "Confirm Email Address" page showing correct email/username | As expected | Pass | |
| AUTH-03 | Click Confirm button on that page | Email is marked verified; redirects to Sign in page  | As expected | Pass | |
| AUTH-04 | Submit signup with honeypot field (`phone_number`) filled in (simulating a bot) | Signup appears to succeed (fake success page shown) but no user account is actually created | As expected — no user created, confirmed via shell query | Pass | |
| AUTH-05 | Attempt login before confirming email | Login blocked; redirected to Confirm Email page rather than logged in | As expected — redirected to Confirm Email page, login refused | Pass | |
| AUTH-06 | Login with valid credentials (username) from a verified account | Logs in and redirects to home page | As expected | Pass | |
| AUTH-07 | Login with valid credentials (email) from a verified account | Logs in and redirects to home page | As expected | Pass | |
| AUTH-08 | Request password reset with a registered email | Loads "password reset sent" confirmation page; reset email printed to console | As expected | Pass | |
| AUTH-08 | Click reset link from console output typed into browser | Loads "set new password" form | As expected | Pass | |
| AUTH-09 | Submit new password on that form | Password updated; redirected to reset-complete page | As expected | Pass | |
| AUTH-09 | Log in with the new password | Login succeeds | As expected | Pass | |
| AUTH-10 | Attempt to reuse the same reset link a second time | Link rejected | As expected | Pass | |
| AUTH-11 | Sign up with mismatched email and email confirmation fields | Form rejected with validation error; no account created | As expected | Pass | |
| AUTH-12 | Sign up with mismatched password and password confirmation fields | Form rejected with validation error; no account created | As expected | Pass | |
| AUTH-13 | Sign up with a username shorter than the minimum length | Form rejected with validation error; no account created | As expected | Pass | |
| AUTH-14 | Sign up with an email already registered to an existing account | Form rejected with validation error; no account created | As expected | Pass | |
| AUTH-15 | Sign up with a username already taken by an existing account | Form rejected with validation error; no account created | As expected | Pass | |
---

## Story-to-Test Mapping

---

## Solved Bugs

---

## Known Bugs / Limitations

---

## Validation

---
