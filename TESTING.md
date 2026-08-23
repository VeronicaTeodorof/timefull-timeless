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
     - [Empty states (EMPTY)](#empty-states-empty)
     - [Permissions (PERM)](#permissions-perm)
     - [Theme (THEME)](#theme-theme)
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

#### gallery app

##### models.py

| Test ID | Test | Expected | Actual | Local | Deployment |
|---|---|---|---|---|---|
| MGM-01 | Theme name appears on Bootstrap theme cards in gallery page | Each theme card displays the theme's name clearly | | | |
| MGM-02 | Select a theme card on the gallery page | URL updates to include the theme's slug (e.g. `/gallery/theme/broken-forms/`), and the page shows sculptures filtered to that theme | | | |
| MGM-03 | Sculptor's control shows a "change image" (or similar) button on each theme card | Clicking it lets the sculptor select/change which sculpture is the representative_sculpture for that theme | | | |
| MGM-04 | Delete a sculpture set as a theme's representative_sculpture | Theme card remains on the gallery page; theme is not deleted | | | |
| MGM-05 | A theme still has other sculptures after its representative_sculpture is deleted | Theme card remains displayed on the gallery page | | | |
| MGM-06 | A theme has no sculptures remaining at all | Theme card is not displayed on the gallery page | | | |
| MGM-07 | Sculptor enters an existing theme name with different case (e.g. "broken forms" vs "Broken Forms") | No new theme card is created; sculpture is linked to the existing theme | | | |
| MGM-08 | Sculptor enters an existing theme name with leading/trailing whitespace (e.g. " Broken Forms ") | No new theme card is created; sculpture is linked to the existing theme | | | |
| MGM-09 | Create and edit forms in sculptor's controls display the status field | Field shows exactly three choices: Available, Reserved, Sold | | | |
| MGM-10 | Title field present on create and edit sculpture forms; submit with title blank | Field is shown on both forms; blank submission is rejected with a validation error | | | |
| MGM-11 | Title translation field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission succeeds (nullable/optional) | | | |
| MGM-12 | View a sculpture's detail page | URL shows the sculpture's slug (e.g. `/gallery/sculpture/whispering-bronze/`) | | | |
| MGM-13 | Dimensions field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission succeeds (nullable/optional) | | | |
| MGM-14 | Material field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission is rejected with a validation error | | | |
| MGM-15 | Price field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission is rejected with a validation error | | | |
| MGM-16 | Enter non-digit characters (excluding "e" and "-", which the number input allows by default) into the price field | Form does not submit; validation error shown | | | |
| MGM-17 | Enter 0.01 in the price field | Form submits successfully (minimum allowed value) | | | |
| MGM-18 | Enter 0 in the price field | Form does not submit; validation error shown | | | |
| MGM-19 | Enter a negative number in the price field | Form does not submit; validation error shown | | | |
| MGM-20 | Weight field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission succeeds (nullable/optional) | | | |
| MGM-21 | Enter 0.10 in the weight field | Form submits successfully (minimum allowed value) | | | |
| MGM-22 | Enter 0.09 in the weight field | Form does not submit; validation error shown | | | |
| MGM-23 | Year field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission is rejected with a validation error | | | |
| MGM-24 | Enter 1990 in the year field | Form submits successfully (minimum allowed value) | | | |
| MGM-25 | Enter 1989 in the year field | Form does not submit; validation error shown | | | |
| MGM-26 | Enter 2026 in the year field | Form submits successfully (current year, maximum allowed) | | | |
| MGM-27 | Enter 2027 in the year field | Form does not submit; validation error shown | | | |
| MGM-28 | Enter a negative number in the year field | Form does not submit; validation error shown (PositiveIntegerField) | | | |
| MGM-29 | Image upload option present on create form; image change option present on edit form; submit with no image | Upload/change control shown appropriately on each form; blank submission is rejected with a validation error | | | |
| MGM-30 | View a sculpture's detail/edit page in sculptor's controls | reserved_at timestamp is displayed (read-only) when the sculpture is reserved | | | |
| MGM-31 | View a sculpture's detail/edit page in sculptor's controls | is_manually_reserved value is displayed (read-only), for verifying reservation logic behaves correctly | | | |
| MGM-32 | New sculpture created, no reservation activity yet | is_manually_reserved displays as False (default) | | | |
| MGM-33 | Artist manually reserves a sculpture from the edit page | is_manually_reserved displays as True | | | |
| MGM-34 | Sculpture is reserved automatically (added to a buyer's selection) | is_manually_reserved displays as False | | | |
| MGM-35 | View a sculpture's detail/edit page in sculptor's controls | is_visible field is present, displays True by default | | | |
| MGM-36 | Sculptor sets is_visible to False | Sculpture no longer appears in the public gallery | | | |
| MGM-37 | Sculptor resets is_visible back to True | Sculpture reappears in the public gallery | | | |
| MGM-38 | Insurance rate override field present on create/edit sculpture forms; sculptor can fill in or change value | Field shown and editable on both forms | | | |
| MGM-39 | Submit with insurance_rate_override left blank | Submission succeeds (nullable/optional) | | | |
| MGM-40 | Enter 0 in insurance_rate_override | Form submits successfully | | | |
| MGM-41 | Enter -1 in insurance_rate_override | Form does not submit; validation error shown | | | |
| MGM-42 | Enter 50 in insurance_rate_override | Form submits successfully (maximum allowed value) | | | |
| MGM-43 | Enter 50.01 in insurance_rate_override | Form does not submit; validation error shown | | | |
| MGM-44 | Themes field present on create/edit sculpture forms | Field is shown and themes are selectable (multi-select) | | | |
| MGM-45 | View a sculpture's detail/edit page in sculptor's controls | reserved_by is displayed (read-only), for verifying reservation logic behaves correctly | | | |
| MGM-46 | Delete a user (e.g. via admin) who has reserved_by set on a sculpture | Sculpture is not deleted; reserved_by reverts to None (SET_NULL) | | | |
| MGM-47 | Submit a sculpture form with a title exactly matching an existing sculpture's title (same casing) | Form rejects submission; validation error shown | | | |
| MGM-48 | Submit a sculpture form with a title matching an existing sculpture's title but in different casing | Form rejects submission; validation error shown | | | |
| MGM-49 | Submit a sculpture form with a title matching an existing sculpture's title, but with leading/trailing whitespace | Form rejects submission; validation error shown | | | |
| MGM-50 | Submit sculpture form with material entered in lowercase (e.g. "bronze wire") | After saving, material displays as title case (e.g. "Bronze Wire") on the sculpture's detail/edit page | | | |


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
| NAV-11 | Click 'Add sculpture' button on gallery page | Navigates to add sculpture page | | | |


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

#### Empty states (EMPTY)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| EMPTY-01 | Gallery page empty state content | Quote and empty message for regular users, plus Add Sculpture button for staff controls | | | |
| EMPTY-02 | Gallery page non-empty state content | Quote, filter row, and theme card grid render when at least one sculpture exists | | | |

#### Permissions (PERM)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| PERM-01 | Gallery page anonymous user | Doesn't see 'Add sculpture' button | | | |
| PERM-02 | Gallery page authenticated non-staff user | Doesn't see 'Add sculpture' button | | | |
| PERM-03 | Gallery page staff | Sees 'Add sculpture' button | | | |
| PERM-04 | Change representative image icon visibility | Visible to staff only, on theme cards in non-empty state | | | |

#### Theme (THEME)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| THEME-01 | Theme card display per theme | Theme card displays when the theme has one or more sculptures; does not display when the theme has none | | | |

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
