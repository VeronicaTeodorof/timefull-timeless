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
     - [Gallery page (GP)](#gallery-page-gp)
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

#### Tdd pass for gallery views
- To add pass for gallery views permission enforcement automated tests needed for each new staff-only view, mirroring the existing add-sculpture pattern (anonymous -> 302, non-staff -> 403, staff ->200):

- [ ] edit_sculpture view
- [ ] delete_sculpture view
- [ ] edit_theme view
- [ ] change representative image view


#### TDD pass for Create and Edit Theme

- [ ] AC1 - new theme created on valid submission
- [ ] AC2 - new theme created and attached to the sculpture
- [ ] AC3 - duplicate name (case-insensitive) reuses existing theme, no duplicate created - Exact-match test passing; different-case test exposed a genuine `IntegrityError` (duplicate slug), not just a clean assertion failure, since `get_or_create` only matches exact names while slug uniqueness is case-insensitive.
- [ ] AC4 - form rejects submission when both theme fields are empty
- [ ] AC6 - selecting multiple existing themes attaches all of them
- [ ] AC7 - existing-theme selection and new-theme submission combine correctly
- [ ] AC9 - multiple `new_theme` values (cloned fields) each create and attach a theme
- [ ] AC11 - theme survives sculpture deletion; card falls back to remaining sculpture (blocked on story 31)
- [ ] AC12 - empty theme hidden from gallery queryset; still included in form queryset
- [ ] AC13 - edit-theme view rejects non-staff/anonymous requests (302/403/200)
- [ ] AC15 - representative image override takes precedence over fallback, even when it wouldn't coincidentally match
- [ ] AC16 - representative-image dropdown scoped to only this theme's sculptures, includes all of them
- [ ] AC17 - rename validation excludes self (no false duplicate on unchanged save), rejects name matching a different theme
- [ ] AC19 - untagging a sculpture from a theme clears a stale representative-image override (blocked on story 31)
- [ ] AC21 - view calls `messages.success(...)` on theme-related success paths


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
| MGM-10 | Title field present on create and edit sculpture forms; submit with title blank | Field is shown on both forms; blank submission is rejected with a validation error | As expected on create | Pass on create | |
| MGM-11 | Title translation field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission succeeds (nullable/optional) | As expected on create | Pass on create | |
| MGM-12 | View a sculpture's detail page | URL shows the sculpture's slug (e.g. `/gallery/sculpture/whispering-bronze/`) | | | |
| MGM-13 | Dimensions field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission succeeds (nullable/optional) | As expected on crate | Pass on create | |
| MGM-14 | Material field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission is rejected with a validation error | As expected on create | Pass on create | |
| MGM-15 | Price field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission is rejected with a validation error | As expected on create | Pass on create | |
| MGM-16 | Enter non-digit characters (excluding "e" and "-", which the number input allows by default) into the price field | Form does not submit; validation error shown | Pass on create | Pass | |
| MGM-17 | Enter 0.01 in the price field | Form submits successfully (minimum allowed value) | As expected on create | Pass on create | |
| MGM-18 | Enter 0 in the price field | Form does not submit; validation error shown | As expected on create | Pass on create | |
| MGM-19 | Enter a negative number in the price field | Form does not submit; validation error shown | As expected on create | Pass on create | |
| MGM-20 | Weight field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission succeeds (nullable/optional) | Does not apply/inconsistent artist records | | |
| MGM-21 | Enter 0.10 in the weight field | Form submits successfully (minimum allowed value) | Does not apply | | |
| MGM-22 | Enter 0.09 in the weight field | Form does not submit; validation error shown | Does not apply | | |
| MGM-23 | Year field present on create and edit sculpture forms; submit with field blank | Field is shown on both forms; blank submission is rejected with a validation error | As expected on creatte | Pass on create | |
| MGM-24 | Enter 1990 in the year field | Form submits successfully (minimum allowed value) | As expected on create | Pass on create | |
| MGM-25 | Enter 1989 in the year field | Form does not submit; validation error shown | As expected on create | Pass on create | |
| MGM-26 | Enter 2026 in the year field | Form submits successfully (current year, maximum allowed) | As expected on create | Pass on create | |
| MGM-27 | Enter 2027 in the year field | Form does not submit; validation error shown | As expected  on create | Pass on create | |
| MGM-28 | Enter a negative number in the year field | Form does not submit; validation error shown (PositiveIntegerField) | As expected on create | Pass on create | |
| MGM-29 | Image upload option present on create form; image change option present on edit form; submit with no image | Upload/change control shown appropriately on each form; blank submission is rejected with a validation error | As expected on create | Pass on create | |
| MGM-30 | View a sculpture's detail/edit page in sculptor's controls | reserved_at timestamp is displayed (read-only) when the sculpture is reserved | Does not apply for this MVP| | |
| MGM-31 | View a sculpture's detail/edit page in sculptor's controls | is_manually_reserved value is displayed (read-only), for verifying reservation logic behaves correctly | Does not apply for this MVP | | |
| MGM-32 | New sculpture created, no reservation activity yet | is_manually_reserved displays as False (default) | Does not apply for this MVP | | |
| MGM-33 | Artist manually reserves a sculpture from the edit page | is_manually_reserved displays as True | Does not apply for this MVP | | |
| MGM-34 | Sculpture is reserved automatically (added to a buyer's selection) | is_manually_reserved displays as False | Does not apply for this MVP | | |
| MGM-35 | View a sculpture's detail/edit page in sculptor's controls | is_visible field is present, displays True by default | Save as draft vs Save buttons present | Pass | |
| MGM-36 | Sculptor sets is_visible to False | Sculpture no longer appears in the public gallery | | | |
| MGM-37 | Sculptor resets is_visible back to True | Sculpture reappears in the public gallery | | | |
| MGM-38 | Insurance rate override field present on create/edit sculpture forms; sculptor can fill in or change value | Field shown and editable on both forms | Doesn't apply for this MVP | | |
| MGM-39 | Submit with insurance_rate_override left blank | Submission succeeds (nullable/optional) | Does not apply for this MVP | | |
| MGM-40 | Enter 0 in insurance_rate_override | Form submits successfully | Does not apply for this MVP  | | |
| MGM-41 | Enter -1 in insurance_rate_override | Form does not submit; validation error shown | Does not apply for this MVP| | |
| MGM-42 | Enter 50 in insurance_rate_override | Form submits successfully (maximum allowed value) | Does not apply for this MVP | | |
| MGM-43 | Enter 50.01 in insurance_rate_override | Form does not submit; validation error shown | Does not apply for this MVP | | |
| MGM-44 | Themes field present on create/edit sculpture forms | Field is shown and themes are selectable (multi-select) | As expected on create | Pass on create | |
| MGM-45 | Submit a sculpture form with a title exactly matching an existing sculpture's title (same casing) | Form rejects submission; validation error shown | | | |
| MGM-46 | Submit a sculpture form with a title matching an existing sculpture's title but in different casing | Form rejects submission; validation error shown | | | |
| MGM-47 | Submit a sculpture form with a title matching an existing sculpture's title, but with leading/trailing whitespace | Form rejects submission; validation error shown | | | |
| MGM-48 | Submit sculpture form with material entered in lowercase (e.g. "bronze wire") | After saving, material displays as title case (e.g. "Bronze Wire") on the sculpture's detail/edit page | | | |


##### forms.py

**SculptureForm**

| Test ID | Test | Expected | Actual | Local | Deployment |
|---|---|---|---|---|---|
| MGF-01 | New theme field |  Present on the form | As expected | | |
| MGF-02 | Submit with blank 'new theme' field | Form submits successfully | | | |
| MGF-03 | 'title', 'title_translation', 'dimensions', 'year', 'material', 'price', 'themes', 'image', 'status'  fields | Present | | | |
| MGF-04 | placeholders | Correct placeholders on each input | | | |



---

## Pass 2 — User-Perspective Testing

### Repeating categories

---

### Per-feature tests

#### Authentication (AUTH)


| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|-------|-------|------------|
| AUTH-01 | Sign up with valid data | Loads Confirm Emai page | As expected | Pass | Pass |
| AUTH-02 | Paste confirmation link url in browser (obtained via console backend) | Loads "Confirm Email Address" page showing correct email/username | As expected | Pass | |
| AUTH-03 | Click Confirm button on that page | Email is marked verified; redirects to Sign in page  | As expected | Pass | Pass |
| AUTH-04 | Submit signup with honeypot field (`phone_number`) filled in (simulating a bot) | Signup appears to succeed (fake success page shown) but no user account is actually created | Does not apply for this MVP | | |
| AUTH-05 | Attempt login before confirming email | Login blocked; redirected to Confirm Email page rather than logged in | As expected - redirected to Confirm Email page, login refused | Pass | Pass|
| AUTH-06 | Login with valid credentials (username) from a verified account | Logs in and redirects to home page | As expected | Pass | Pass |
| AUTH-07 | Login with valid credentials (email) from a verified account | Logs in and redirects to home page | As expected | Pass | Pass |
| AUTH-08 | Request password reset with a registered email | Loads "password reset sent" confirmation page | As expected | Pass | Pass |
| AUTH-08 | Click reset link from console output typed into browser | Loads "set new password" form | As expected | Pass | |
| AUTH-09 | Submit new password on that form | Password updated; redirected to reset-complete page | As expected | Pass | Pass |
| AUTH-09 | Log in with the new password | Login succeeds | As expected | Pass | Pass |
| AUTH-10 | Attempt to reuse the same reset link a second time | Link rejected | As expected | Pass | Pass |
| AUTH-11 | Sign up with mismatched email and email confirmation fields | Form rejected with validation error; no account created | As expected | Pass | Pass |
| AUTH-12 | Sign up with mismatched password and password confirmation fields | Form rejected with validation error; no account created | As expected | Pass | Pass |
| AUTH-13 | Sign up with a username shorter than the minimum length | Form rejected with validation error; no account created | As expected | Pass | Pass |
| AUTH-14 | Sign up with an email already registered to an existing account | Form rejected with validation error; no account created | As expected | Pass | Pass |
| AUTH-15 | Sign up with a username already taken by an existing account | Form rejected with validation error; no account created | As expected | Pass | Pass |
| AUTH-16 | Sign up with valid data using a real, accessible inbox, check that inbox | Confirmation email arrives in the real inbox, addressed to the exact email entered, with a working confirmation link | As expected | | Pass |
| AUTH-17 | Click confirmation link from a real email client | Link opens and loads the Confirm Email Address page correctly, showing the right email/username | As expected | | Pass |
| AUTH-18 | Submit login with valid username but wrong password | Login rejected; clear error shown; user remains logged out | As expected | Pass | Pass |
| AUTH-20 | Submit login with a username/email that doesn't exist | Login rejected; clear error shown; user remains logged out | As expected | Pass | Pass |


#### Responsiveness (RES)

**Navbar**

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

**Gallery Page**

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| GP-04 | Column count at desktop width | Theme cards arrange into 3 columns for tablet and disktop | As expected | Pass | |
| GP-05 | Column count at mobile width | Theme cards arrange into one column for mobile | As expected | Pass | |

**Sculpture Detail Page**

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| RES-06 | Layout at mobile width | Image and details stack in a single column | As expected | Pass | |
| RES-07 | Layout at desktop width (≥768px) | Image and details render in two columns (image left, details right) | As expected | Pass | |
| RES-08 | Layout transition across breakpoint | Resizing across 768px switches cleanly between stacked and two-column, no overlap or broken spacing | As expected | Pass | |


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

#### Empty states (EMPTY)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| EMPTY-01 | Gallery page empty state content | Quote and empty message for regular users, plus Add Sculpture button for staff controls | As expected | Pass | |
| EMPTY-02 | Gallery page non-empty state content | Quote, filter row, and theme card grid render when at least one sculpture exists | | | |

#### Permissions (PERM)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| PERM-01 | Gallery page anonymous user | Doesn't see 'Add sculpture' button | As expected | Pass | |
| PERM-02 | Gallery page authenticated non-staff user | Doesn't see 'Add sculpture' button | As expected | Pass | |
| PERM-03 | Gallery page staff | Sees 'Add sculpture' button | As expected | Pass | |
| PERM-04 | Change representative image icon visibility | Visible to staff only, on theme cards in non-empty state | | | |
| PERM-05 | Anonymous user tries to access '/gallery/add_sculpture/' | Redirects to login page | As expected | Pass | |
| PERM-06 | Authenticated non-staff user tries to access '/gallery/add_sculpture/' | Gets 403 response | As expected | Pass | |
| PERM-07 | Staff user tries to access '/gallery/add_sculpture/' from url browser | Page loads successfully | As expected | Pass | |
| PERM-XX | Anonymous user tries to access edit sculpture page | Redirects to login page | | | |
| PERM-XX | Authenticated non-staff user tries to access edit sculpture page | Gets 403 response  | | | |
| PERM-XX | Staff user tries to access edit sculpture page | Page loads successfully | | | |
| PERM-XX | Anonymous user tries to see edit/delete buttons on sculpture detail | Buttons not visible/rendered | | | |
| PERM-XX | Non-staff user tries to see edit/delete buttons on sculpture detail | Buttons not visible/rendered | | | |
| PERM-XX | Staff user tries to see edit/delete buttons on sculpture detail | Buttons visible | | | |
| PERM-XX | Staff user clicks delete button modal trigger on sculpture detail | Can trigger delete modal | | | |
| PERM-XX | Anonymous user tries to access edit theme controls / change representative image (gallery) | Controls not visible/accessible | | | |
| PERM-XX | Non-staff user tries to  edit theme / change representative image (gallery) | Controls not visible/accessible | | | |
| PERM-XX | Staff user tries to edit theme / change representative image (gallery) | Controls visible/accessible | | | |

#### Gallery page (GP)

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| GP-01 | Theme card display per theme | Theme card displays when the theme has one or more sculptures; does not display when the theme has none | | | |
| GP-02 | Click a theme card | Loads a carousel of sculpture detail pages belonging to that theme | | | |
| GP-03 | Theme cards render at uniform height | All theme cards display at a consistent fixed height regardless of source image aspect ratio | As expected | Pass | |
| GP-04 | Image crop, no distortion | Source image fills the fixed card height via crop | As exptected | Pass | |
| GP-05 | Card link hover state | Hovering the card shows a visible affordance indicating it's clickable | Zoom on hover | Pass | |
| GP-06 | Theme name renders in footer| Theme name text appears in a solid-background footer strip below the image| As expected - hardcoded | Pass | |
| GP-07 | Footer text contrast | Theme name text is legible against the footer's solid background, regardless of the image above it | As expected | Pass | |
| GP-08 | Footer height consistency | Footer strip height is consistent across cards regardless of image height (masonry) or theme name length | As expected | Pass | |
| GP-09 | Click 'Add sculpture' button on gallery page | Navigates to add sculpture page | As expected | Pass | |


#### Sculpture Detail

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| SDP-01 | Mobile layout matches wireframe | Field order and grouping (image, identifiers, details, actions) match the mobile wireframe | As expected | Pass | |
| SDP-02 | Desktop layout matches wireframe | Field order and grouping match the desktop wireframe, with image and details in separate columns | As expected | Pass | |
| SD-03 | Click "Acquire Now"  | Navigates to the terms page | | | |
| SD-04 | Click "Enquire about this piece" | Navigates to the contact page | | | |

#### Forms
##### Add Sculpture Form
| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| ASF-01 | All form fields present | Title, title translation, dimensions, year, material, price, status, theme (dropdown + new-theme text), image upload all render | As expected | Pass | Pass |
| ASF-02 | Save buttons present | "Save" and "Save as draft" buttons both render | As expected | Pass | Pass |
| ASF-03 | Required fields | Clearly marked as such | Consistent marking | Pass | |
| ASF-04 | Click the status dropdown on create/edit form | Dropdown opens showing tow choices (Available, Sold); hovering over an option shows a visible hover state; clicking an option selects it and closes the dropdown, showing the selected value in the field | As expected | Pass | Pass |
| ASF-05 | Click the image upload box/button on create form | File picker dialog opens, allowing the user to select an image from their device | As exptected | Pass | Pass |
| ASF-06 | Select an image file in the file picker | File picker closes; a visual indicator or message confirms the file was selected/attached | File name shown | Pass | |
| ASF-07 | Hover over form buttons (Save/Save as Draft) | Each button shows a visible hover state (color/shadow/cursor change) indicating it's interactive | As expected | Pass | |
| ASF-08 | Submit form with all valid data | Form saves; a success message/confirmation is shown to the user (not just a redirect with no feedback) | As expected | Pass | |
| ASF-09 | Submit form with invalid/missing data | Form does not save; relevant, clear error message(s) shown next to the failing field(s) | Nothing happens | Fail | |
| ASF-10 | Save a valid sculpture as staff/sculptor, then view the gallery logged in as (or logged out from) a non-staff account | Newly saved sculpture appears in the public gallery | Nothing happens | Fail | |
| ASF-11 | Save a sculpture as draft then view the gallery as a non-staff account | Sculpture does NOT appear in the public gallery | Nothing happens | Fail | |
| ASF-12 | Save a sculpture as draft then view it via sculptor's controls (staff account) | Sculpture DOES appear in sculptor's controls | Nothing happens | Fail | |



#### Add Sculpture Page

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| ASP-01 | Page title | "Add sculpture" heading renders | As expected | Pass | |
| ASP-02 | Back link presence | Back-to-gallery affordance renders at top of form | As expected | Pass | |
| ASP-03 | Back link destination | Clicking back link navigates to gallery page | As expected | Pass | |
| ASP-04 | Unsaved changes warning | Navigating away with unsaved input shows confirmation | | | |

#### Create and Edit Theme

| Test ID | Test | Expected | Actual | Local | Deployment |
|---------|------|----------|--------|-------|------------|
| CT-01 | New theme appears in multi-select after creation | Creating a sculpture with a new theme name; visiting edit-sculpture afterward shows the new theme as an option in the multi-select | As expected | Pass | |
| CT-02 | New theme correctly associated with its sculpture | Creating a sculpture with a new theme name; sculpture detail/gallery shows the new theme correctly associated | | | |
| CT-03 | Duplicate new theme name (exact match) | Submitting a new theme name exactly matching an existing theme; no error shown, no duplicate choice, submission succeeds normally | As expected | Pass | |
| CT-04 | Duplicate new theme name (different casing) | Submitting a new theme name matching an existing theme with different casing; no error shown, submission succeeds normally | As expected | Pass | |
| CT-05 | Both theme fields left empty | Submitting the add-sculpture form with both theme fields empty; clear validation error shown near the right place, other entered fields preserved | | | |
| CT-06 | Success/error feedback messages | Adding a new theme shows a success message; a theme-related validation error shows a clear error message; editing an existing theme shows a success message on save | | | |
| CT-07 | Select multiple existing themes | Physically selecting two or more themes in the multi-select; interaction feels right, selected state is visually clear | | | |
| CT-08 | Combine existing theme selection with a new theme | Selecting an existing theme and typing a new theme name in the same submission; both end up visible together on the sculpture and gallery | | | |
| CT-09 | Zero themes - form state | With zero themes in the database, the themes multi-select is not displayed on the add-sculpture form, and the "new theme" field's placeholder reflects this is the first theme(s) | As expected | Pass | |
| CT-10 | "+" button clones new theme field | Clicking the "+" button adds an additional "new theme" field in the browser (one theme name per field) | | | |
| CT-11 | New theme(s) appear as gallery cards | After adding a sculpture with one or more new themes, the gallery page shows each as its own card, displaying the sculpture's image | | | |
| CT-12 | Edit menu visible only to staff | Staff user sees the edit menu (both labeled options) on each theme card; anonymous/non-staff users do not see it | | | |
| CT-13 | Edit menu links navigate correctly | Clicking either "Change theme name" or "Change representative image" navigates to the correct theme's edit page | | | |
| CT-14 | Representative image override reflected in gallery | Selecting a different sculpture as the theme's representative image and saving; gallery card shows the selected sculpture's image | | | |
| CT-15 | Theme name field pre-populated | Theme-edit page's name field exists and is pre-populated with the current name on load | | | |
| CT-16 | Renamed theme reflected in gallery | Renaming a theme and saving; gallery card displays the new name | | | |
| CT-17 | Cancel link returns to gallery without saving | Theme-edit page has a "Cancel" link; following it returns to the gallery page, nothing is saved | | | |
| CT-18 | Themes casing | Consistent casing for themes in multiselect fields and theme cards | | | |
| CT-19 | Themes displayed in multiselect fields | All themes are displayed in multiselect fields regardless of whether there are any sculptures with that theme or not | as expected | Pass | |
| CT-20 | Non-empty themes gallery cards | Gallery displays one card per theme when this is not empty | | | |
| CT-21 | Representative image default | The image of the latest added sculpture in a theme is displayed as representative image for that theme when no other is manually selected | As expected | Pass | |

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


### DecimalField MinValueValidator Silently Rejecting Its Own Minimum

#### The Problem

Submitting `price = 0.01` — exactly the field's stated minimum — was rejected with "Ensure this value is greater than or equal to 0.01."

#### Why It Happened

`MinValueValidator(0.01)` used a Python `float`. Floats can't represent `0.01` exactly; the stored value was actually slightly above true `0.01`. Since `price` is a `DecimalField`, the submitted value cleaned to an exact `Decimal('0.01')` — which compared as *less than* the imprecise float, so the validator rejected its own limit.

A first attempt, `Decimal(0.01)`, didn't fix it — passing a float into `Decimal()` just carries the same imprecision.

#### The Solution

```python
validators=[MinValueValidator(Decimal('0.01'))]
```

Pass the limit as a **string**, not a float — `Decimal('0.01')` parses the digits exactly, with no float detour.

#### Key Takeaways

- Never pass a bare float (or `Decimal(float)`) into a validator on a `DecimalField` — wrap the literal as `Decimal('0.01')` (string).
- Bugs like this only surface at the exact boundary value — testing the literal minimum/maximum catches what a "typical" value won't.


### New theme submission rejected when multi-select is empty

#### The Problem

Manually testing the add-sculpture form with zero existing themes and only a new_theme value filled in resulted in 'This field is required.' error message.

Although the intention from the start was for the "at least one theme" requirement to accept either themes, new_theme, or both, the part that explicitly allows new_theme alone (with themes empty) was never actually written in code. Every earlier passing test happened to include a pre-existing theme selection in its data (from setUp()), so the gap was never exposed until manually testing the "new_theme only" scenario for real - at which point Django's own default form-level requirement on themes rejected the submission.

Adding a clean() method in SculptureForm didn't solve the issue, identical error messages displayed for both automated and manual tests.

#### Why clean() didn't fix the bug

Form validation happens in this order:
1. Field-level validation - each field's own validators, including the automatic `required` check (this is where the error was
   coming from).
2. Form-level validation - the form's own `clean()` method, which only runs after all fields have already passed step 1.
3. Model-level / database validation — separate again, happening later still (e.g. UniqueConstraints, at the actual database write).

Since the `themes` field's own required check (step 1) rejected the submission first, the form's `clean()` method (step 2) never got a
chance to run at all.

#### The Solution

Explicitly override themes field as not required at the form level, so that a custom cross-field check instead could run. So the solution was custom `clean()` `+` themes required override with `required=False`.

#### Key Takeaways
Given that a field's default validation runs before custom clean() logic, when the two disagree, field level validation wins unless explicitly overwritten.

---

## Known Bugs / Limitations

- Custom 403 error page -  not yet built; Django's default 403 page is currently shown to non-staff authenticated users blocked from staff-only controls. Functionally correct, for consistency only.

---

## Validation

---
