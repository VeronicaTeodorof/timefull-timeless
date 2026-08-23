# TESTING.md — timefull-timeless
# Table of Contents

1. [Pass 1 - Code Audit](#pass-1--code-audit)
   - [Automated tests](#automated-tests)
   - [Manual tests - code reflection in UI](#manual-tests--code-reflection-in-ui)

2. [Pass 2 - User-Perspective Testing](#pass-2--user-perspective-testing)
   - [Repeating categories](#repeating-categories)
   - [Per-feature tests](#per-feature-tests)
     - [Authentication (AUTH)](#authentication-auth)
     - [Responsiveness (RES)](#responsiveness-res)
     - [Navigation links (NAV)](#navigation-links-nav)
     - [Search function (SEA)](#search-function-sea)
3. [Story-to-Test Mapping](#story-to-test-mapping)
4. [Solved Bugs](#solved-bugs)
5. [Known Bugs / Limitations](#known-bugs--limitations)
6. [Validation](#validation)
---


## Pass 1 — Code Audit

### Automated tests
#### First TDD pass for Theme and Sculpture models in gallery app

Model-level tests were written first (red), followed by the model implementation (green), following TDD. Tests are grouped by category
below rather than listed individually, given the volume of similar field-level checks.

| Category | Models Covered | Approx. Tests | Result |
|---|---|---|---|
| Field existence & type | Theme, Sculpture | ~20 | All pass |
| Nullability constraints (`null=True`/`False`) | Theme, Sculpture | ~12 | All pass |
| Uniqueness constraints (case-insensitive name/title, slug) | Theme, Sculpture | 4 | All pass |
| Validator boundaries (price, weight, year, insurance_rate_override) | Sculpture | 8 | All pass |
| Default values (status, is_visible, is_manually_reserved) | Sculpture | 3 | All pass |
| Slug auto-generation from name/title | Theme, Sculpture | 2 | All pass |
| Foreign key SET_NULL behaviour on delete | Theme ↔ Sculpture | 1 | All pass |
| ManyToMany relationship (themes ↔ sculptures) | Sculpture | 1 | All pass |
| Image field required-ness (CloudinaryField) | Sculpture | 2 | **Failed initially** — see note below |

### Notable finding: Sculpture.image (CloudinaryField)

I expected `Sculpture.objects.create(image=None)` to raise `IntegrityError`, since `image` is defined with `null=False`.

The test failed with no exception was raised. Investigation with Claude AI via the Django shell showed that `CloudinaryField` does not pass a true database `NULL` when given `None`; instead it substitutes an empty `CloudinaryResource` object (with `public_id=None`). Since something non-null is written to the row, the database's `NOT NULL` constraint is never violated.

Django's `null` check therefore never triggers on this field. What does catch a missing image is `full_clean()`'s **blank** check
(`image` does not have `blank=True`), since Django considers the empty `CloudinaryResource` "blank."

Two tests were written to capture this:

- One confirming `Sculpture.objects.create(image=None)` succeeds at the database level (documents the gap as expected, current
  behaviour of `CloudinaryField`).
- One confirming `full_clean()` raises `ValidationError` for a missing image (confirms required is enforced at the validation layer instead).

**Risk noted:** any code path that saves a `Sculpture` without calling `full_clean()` first (e.g. a direct `.objects.create()` or
`.save()` call outside a `ModelForm`) could silently save a sculpture with no real image, since the database itself will not reject it.

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


#### Responsiveness (RES)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| RES-01 | Burger visible on mobile (<992px) | Burger icon shown, links hidden | As expected | Pass | |
| RES-02 | Burger hidden on desktop (≥992px) | Burger hidden, links inline | As expected | Pass | |
| RES-03 | Burger drawer opens on tap | Collapse expands, links + auth block visible | As expected | Pass | |
| RES-04 | Burger drawer closes on second tap | Collapses drawer | As expected | Pass  | |
| RES-05 | Search modal opens - mobile | Fullscreen modal opens | As expected | Pass | |
| RES-06 | Search modal opens - desktop | Centred modal opens | As expected | Pass | |
| RES-07 | Username shown when authenticated (desktop) | Username replaces Sign in/Sign up | As expected | Pass | |
| RES-08 | Dropdown opens on username click/tap (mobile + desktop) | Order History / Log out appear | As expected | Pass | |
| RES-09 | Dropdown closes on second click/tap (mobile + desktop) | Dropdown closes | As expected | Pass | |

#### Navigation links (NAV)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| NAV-00 | Logo | Navigates to home page | As expected | Pass | |
| NAV-01 | Home link | Navigates to home page | As expected | Pass | |
| NAV-02 | Gallery link | Navigates to gallery page | As expected | Pass | |
| NAV-03 | About link | Navigates to about page | As expected | Pass | |
| NAV-04 | Enquiries link | Navigates to enquiries page | As expected | Pass | |
| NAV-05 | Sign in link (guest) | Navigates to login page | As expected | Pass | |
| NAV-06 | Sign up link (guest) | Navigates to signup page | As expected | Pass | |
| NAV-07 | Order History link (authenticated) | Navigates to order history | As expected | Pass | |
| NAV-08 | Log out link (authenticated) | Logs out, redirects to home page | As expected | Pass | |
| NAV-09 | Shipping link on footer | Navigates to policies page, shipping section | | | |
| NAV-10 | Terms link on footer | Navigates to policies page, terms section | | | |


#### Search function (SEA)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| SEA-01 | Match by title | Sculpture appears in results | | | |
| SEA-02 | Match by description | Sculpture(s) appear(s) in results | | | |
| SEA-03 | Match by theme | All sculptures in that theme appear | | | |
| SEA-04 | Case insensitivity | Matches regardless of case | | | |
| SEA-05 | No results | Empty-state message + link back to gallery shown | | | |
| SEA-06 | Empty submission | Returns no results, not full catalogue | | | |
| SEA-07 | Duplicate prevention | Sculpture appears only once in results | | | |
| SEA-08 | Enter key submits | Same result as clicking submit button | | | |
---

## Story-to-Test Mapping

---

## Solved Bugs

### Desktop Navbar Dropdown Layout Shift Bug

#### The Problem

When clicking the user profile dropdown on desktop, the entire navigation bar shifted horizontally to the left. This layout shift never happened on mobile, even though both breakpoints used the same login partial and username data.

#### Why It Happened

**Desktop vs. mobile rendering:** mobile stacks items vertically in normal document flow, so opening a menu just pushes content down. Desktop places items side-by-side in a flex row, which behaves differently when a child's layout changes.
**Flexbox & position overrides:** opening the dropdown made Bootstrap recalculate the floating menu's coordinates dynamically. Inside a horizontal flex row, this recalculation forced the whole row to resize, producing a visible horizontal "snap" as sibling elements shifted to accommodate the dropdown's changing inline styles.

#### The Solution

The menu layer is strictly anchored using CSS rules targeted specifically at desktop viewports:

```css
/* Apply custom positioning only to desktop viewports (lg and up) */
@media (min-width: 992px) {
    .navbar-nav .dropdown-menu-end {
        position: absolute !important;
        right: 0 !important;
        left: auto !important;
    }
}
```

#### Key Takeaways

- `position: absolute !important;` completely detaches the floating menu from the navbar's physical layout calculations so opening it cannot push sibling elements.
- `right: 0 !important;` and `left: auto !important;` anchor the dropdown directly to the right edge of its parent container.
- Scope the CSS inside a `@media (min-width: 992px)` query to protect mobile screens, allowing the mobile drawer to collapse and expand vertically without breaking.

Note: This bug was diagnosed and fixed with the help of AI tools.
---

## Known Bugs / Limitations

---

## Validation

---
