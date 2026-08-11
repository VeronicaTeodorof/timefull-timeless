# timefull-timeless
#### *—  and a race against time*
###### *Concept & Branding by Veronica Teodorof*

A bespoke, full stack Django web application designed as a digital home for a professional sculptor. This platform strives to unify an elegant fine-art portfolio with a secure e-commerce marketplace, professional resume, and interactive business card.

The project title is a deliberate paradox rooted in the sculptor's core themes of time, flight, and angels: **"timefull"** (intentionally spelled with a double 'l' firstly for visual symmetry, and secondly, to distinguish its meaning from *timeful*) - reads literally: 'full of time', while **"timeless"** represents their eternal artistic and spiritual value.


Developed under the unforgiving watch of the Academic Deadline - the cold, merciless deity that frightens the organized students and the chaotic ones alike - this project is a race to finish before the gates lock forever. Will this chronic detail-obsessed, deadline-missing developer manage to complete the challenge? Stay tuned to find out!

---

## Table of Contents
1. [Strategy Plane](#1-strategy-plane)
   - [Business goals](#business-goals)
   - [Target Audience Segmentation: User Needs and Conversion Value](#target-audience-segmentation-user-needs-and-conversion-value)
   - [Developer Goals](#developer-goals)
   - [Resources Consulted](#resources-consulted)
2. [Scope Plane](#2-scope-plane)
   - [User Stories](#user-stories)

---


## 1. Strategy Plane

### Business Goals (Problem - Solution)

#### 1. Secondary income from a larger audience.

**Problem**: The artist’s current income consists of a stable but low teacher's salary and occasional local gallery sales. Because his sales are currently limited to physical local galleries, his audience is restricted geographically, which limits his potential to grow his secondary income.

**Solution**: A dedicated individual portfolio website with integrated e-commerce features. This could make his artwork visible to a larger national and international audience and by integrating an e-commerce checkout, he can sell his unique contemporary sculptures directly online to this expanded market, creating a more reliable secondary income alongside his teaching salary.


#### 2. Professional separation.

**Problem**: The artist’s current digital footprint is limited entirely to a personal Facebook account that blends his personal life with his professional art. A social media account is a casual communication tool and cannot showcase a recognized sculptor’s portfolio in a professional manner. This conflicts with his first stated goal of increasing audiece for his artwork.

**Solution**: A custom portfolio website that establishes a strict professional separation from his personal Facebook profile.

#### 3. Establishing a brand.

**Problem**: While the sculptor’s artwork is deeply unique and centered around specific, powerful themes like flight, time, and angels, his current online presence does not represent this artistic vision. By relying entirely on Facebook, his identity is forced into a standard, generic layout that gets lost among millions of identical casual profiles, making it impossible to create a memorable or impactful digital brand.

**Solution**: A dedicated, custom website that establishes an original and memorable digital brand. This platform gives the artist total control over the visual presentation, allowing the website's name, logo, design, typography, and layout to directly mirror the specific themes of his sculpture, ensuring his online identity is unique and representative of his artwork.

#### 4. Establishing trust.

**Problem**: The artist has never sold his artwork online before, meaning he has no pre-existing digital reputation or track record of processing distant transactions. For a buyer looking at high-value, unique contemporary sculptures, the lack of an established, secure verification path creates high transactional hesitation and a fear of fraud.

**Solution**: A dedicated website that builds immediate consumer trust through explicit safety features and social proof. The platform will feature a direct inquiry form, giving buyers an immediate line of communication. Additionally, the site will feature a dedicated testimonials section showcasing reviews of his artwork generally, alongside specific delivery-completed reviews from verified customers regarding their online shopping experience.
Another feature that increases customer confidence is mandatory account registration before any purchase, ensuring that every high-value transaction has a reliable communication channel.


### Target Audience Segmentation: User Needs and Conversion Value

The website's user base is divided into three distinct groups based on why they visit the site, what they look for, and how they buy.

#### 1. The B2C Private Collector (Consumer Buyers)
*   **The Intent:** They use their own savings to buy original art for their homes.
*   **User Needs (International):**
    *   To feel confident about the artist's professional background and history before spending money online.
    *   To see the exact size, shape, and physical texture of a sculpture from a screen since they cannot visit the studio in person.
    *   To use a familiar, safe payment method and understand exactly how the heavy, fragile artwork will be protected during shipping and customs checks.
    *   To trust that my personal and payment information is handled securely when creating an account and making a purchase.
*   **User Needs (Local):**
    *   To browse the artist's current studio inventory online but avoid expensive delivery fees and border paperwork completely.
*   **Conversion Value [Revenue & Core Sales]:** These are the buyers who make direct purchases, creating the extra income the artist needs to support his teaching salary.

#### 2. The B2B Trade Professional (Designers, Architects & Curators)
*   **The Intent:** They are business-focused buyers who look for art using budgets from companies, institutions, or interior clients for housing projects or public exhibitions.
*   **User Needs:**
    *   To quickly find exact physical details (size, weight, materials) to make sure a heavy sculpture will fit perfectly into their client's specific room layout.
    *   To review a professional list of the artist's past exhibitions and career history so they can justify the high cost of the art to their business managers or clients.
    *   To trust that account and transaction details are kept secure and confidential, particularly for business-related purchases.
*   **Conversion Value [High-Volume & Commission Pipeline]:** These buyers represent businesses that purchase high-value items or build long-term relationships for future custom-made art commissions.

#### 3. The General Audience (Academic Peers, Art Students & Fellow Sculptors)
*   **The Intent:** They visit the site for school research, technical ideas, and to follow the local art scene or the artist's career timeline.
*   **User Needs:**
    *   To check a clean timeline of past gallery shows and public projects for school or research purposes.
    *   To have a simple way to leave feedback or read comments from other artists and exhibition visitors.
*   **Conversion Value [Reputation, SEO & Community Validation]:** These visitors do not buy art directly, but their online clicks build search engine traction. Their comments and reviews create the public trust and social proof that the actual buyers need to see before spending their money.


### Developer Goals

*   **Academic Goals [Course Completion & Passing Criteria]:** To build a complete web application that meets all the grading rules for Unit 4 (Full Stack Frameworks with Django) with a tight deadline.
*   **Professional Goals [Portfolio Piece & Future Freelance Business]:** To create an MVP website for a real-world client that serves as a main project in my personal portfolio. Building this site proves I can deliver safe, working software, which will hopefully help me start my own freelance business creating websites for people and businesses in the future. One skill to showcase is building custom, permission-gated content management (allowing the client to add/edit/delete his own sculptures, events, and bio directly within the site) rather than relying on Django's built-in admin — demonstrating the ability to deliver tailored, non-technical-user-friendly tools.


**Note on acknowledged but partially unaddressed need:** The Local Private Collector need identified above (avoiding delivery fees and border paperwork) is only partially met within this build. The Art Basel and UBS report cited below notes local markets outperformed international ones in 2025 due to customs costs, therefore a dedicated, localized Romanian offering - separate pricing, region-relevant payment methods, and a market-specific experience - would likely serve this need more effectively than a single unified international flow; business logic alone suggests building this Romanian-first. However, this project is assessed in English, and the academic constraint of the assessment governs the scope of this build. Local buyers are not excluded — studio pickup avoids shipping costs and customs complexity within the current build — but full market-specific localization is treated as a high-priority direction for the live version of the site, to be addressed once assessment constraints no longer apply.


### Resources Consulted

General market context was informed by the following industry reports

* **[The Art Basel and UBS Global Art Market Report](https://theartmarket.artbasel.com/):** https://theartmarket.artbasel.com/download/The-Art-Basel-and-UBS-Art-Market-Report-2026-by-Arts-Economics.pdf
*   **[The Deloitte Romania Art Report (with Artmark & RAD)](https://business-review.eu/lifestyle/art/romanias-art-market-shifts-toward-investment-and-growth-295739):** https://business-review.eu/lifestyle/art/deloitte-study-romanian-collectors-are-mainly-motivated-by-aesthetic-and-personal-reasons-283658

---

## 2. Scope Plane

### Theme Justification

The following themes for User Stories have been derived from the user needs, business goals, and developer goals identified at Strategy level:
- Authentication
- Sculpture/Gallery
- Cart & Checkout
- Shipping & Handling
- Artist Background (incl. Events)
- Testimonials
- Sculptor Controls
- Contact
- UX/UI

Below is a table showing how each of these themes was derived from Strategy inputs.  Not every theme is justified by all categories of stakeholders - some are driven by only one or two, therefore some cells are left blank rather than forced.

Order reflects the actual translation pipeline: Strategy (user needs + business goals + developer goals) -> Scope (with themes as the output).

| User Need | Business Goal | Developer Goal | -> Theme |
|---|---|---|---|
| Access personal account; trust that personal/payment data is handled securely | Reliable order communication for high-value transactions (no guest checkout) | — | **Authentication** |
| Browse and find pieces; see exact size/weight/material (B2C + B2B); view artwork for research/interest (academic peers, fellow sculptors) | Reach a wider audience, generate sales | — | **Sculpture/Gallery** |
| Purchase securely, track orders | Convert visitors into paying customers | — | **Cart & Checkout** |
| Trust that fragile, high-value items arrive safely | Reduce disputes/damage claims on high-value items | — | **Shipping & Handling** |
| Learn about the artist; review exhibition history (B2B + academic peers) | Establish a distinct brand, separate from personal/casual social presence | — | **Artist Background (incl. Events)** |
| See social proof before a high-value purchase | Establish trust with no prior online sales track record | — | **Testimonials** |
| — | Reduce sculptor's reliance on developer for ongoing updates; professional separation from personal admin | Demonstrates ability to build custom, permission-gated client tools (vs. relying on Django admin) — directly transferable to future freelance client work | **Sculptor Controls** |
| Ask questions before a significant purchase | Immediate line of communication builds buyer confidence | — | **Contact** |
| Usable regardless of device or ability | Avoid losing customers to poor experience, wider reach | — | **UX/UI (cross-cutting)** |


### User Stories

#### Authentication Theme
<details><summary>
1. As a visitor, I want to register for an account, so that I can access features reserved for registered users.
</summary>


**Acceptance Criteria:**

- [ ]
- [ ]
- [ ]

</details>

<details><summary>
2. As a registered user, I want to log in to my account, so that I can access my personal information and account features.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
3. As a logged-in user, I want to log out of my account, so that my personal information is protected.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
4. As a new user, I want to receive a confirmation email after registering, so that I can verify my account.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
5. As a new user, I want to click a verification link in my email to activate my account, so that I can log in and access member features.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
6. As a visitor without an account, I want to be prompted to register or log in when I try to purchase, so that my order is tied to a verified account.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
7. As a registered user, I want to view my personalized profile and order history, so that I can track my past purchases.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

#### Sculpture/Gallery (browse, filter) Theme

<details><summary>
8. As a visitor, I want to be able to see a selection of artist's sculptures ordered by theme, so that I get to understand the artistic vision of this sculptor.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
9. As a visitor, I want to be able to see a representative image of the sculpture, along with a full description of material, dimensions, and price, so that I'm fully informed about that particular artwork.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
10. As a visitor, I want to filter sculptures by material and availability, so that I can find pieces that match what I'm looking for and are still available for purchase.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

#### Cart & Checkout (including order history) Theme

<details><summary>
11. As a registered user, I want to add a sculpture to my cart, so that I can proceed to payment.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
12. As a registered user, I want to provide my delivery details and complete payment securely, so that I can finalize the transaction.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
13. As a registered user, I want to be clearly informed whether delivery is available to my country, so that I know whether I can proceed to payment.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
14. As a registered user, I want to choose between home delivery and studio pickup before payment, so that I can select the option that best suits me.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
15. As a registered user, I want to provide my delivery details and be redirected to a secure payment page to complete my purchase, so that I can finalize the transaction.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
16. As a registered user, I want to receive feedback on whether my transaction was successful or not, so that I am aware of the outcome.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
17. As a registered user, I want to see the total price and a breakdown of costs before making a payment, so that I know exactly what I'm being charged for.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
18. As a registered user, I want to view my order history, so that I can review my past purchases.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>


#### Shipping & Handling Theme

<details><summary>
19. As a visitor, I want to know how my order would be packed and shipped, so that I feel confident the artwork will arrive safely.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
20. As a registered user, I want to be offered transparent information about insurance and insurance costs, so that I can make an informed decision when buying a sculpture.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
21. As a registered user, I want to be informed that a Certificate of Authenticity is included with my purchase, so that I can trust the piece's provenance and value.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>


#### Artist Background Theme

<details><summary>
22. As a visitor, I want to learn about the sculptor's background, so that I can understand his artistic journey and history.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
23. As a visitor, I want to be informed of the sculptor's past and upcoming events, so that I can understand his presence in the local artistic world and visit one of his exhibitions if I have the chance.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

#### Testimonials Theme

<details><summary>
24. As an authenticated user, I want to share my impressions of the sculptor's work, so that I can express my appreciation and contribute to the site's community of supporters.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
25. As a verified buyer, I want to share a testimonial about my purchase experience, so that other prospective buyers can trust the quality, value, and overall service.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
26. As a registered user, I want to edit or delete my own testimonial, so that I can keep it accurate or remove it if my views change.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
27. As a visitor, I want to filter testimonials by type (general impressions or verified purchase experiences), so that I can find the perspective most relevant to me.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>


#### Sculptor Dashboard (role-based views) Theme

<details><summary>
28. As the sculptor, I want my account to have elevated permissions, so that only I can access content-management controls across the site.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
29. As the sculptor, I want to add, edit, or delete themes (with safeguards preventing deletion of a theme still assigned to sculptures), so that I can keep my thematic index accurate and up to date.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
30. As the sculptor, I want to upload or replace a sculpture's image when adding or editing it, so that the listing accurately reflects the artwork.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
31. As the sculptor, I want to add a new sculpture, edit the details of an existing one, or remove it from the gallery (permanently deleting it if never sold, or archiving it if it has been), so that I have complete control over what's displayed in my gallery page.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
32. As the sculptor, I want to be notified by email and see a list of new orders, so that I know what to prepare and ship.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
33. As the sculptor, I want to edit the content of my bio, so that I keep it up to date.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
34. As the sculptor, I want to add, edit, or remove events, so that I keep a clear and accurate list of my participations.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>


#### Contact Theme

<details><summary>
35. As a site visitor, I want to be able to send the sculptor a message for any reason - inquiries about a piece, custom commissions, collaborations, or general questions — so that I can reach him directly regardless of my purpose for visiting.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>


#### UX/UI Theme

<details><summary>
36. As a visitor, I want to be welcomed by a homepage that represents the artist's work and vision, so that I'm invited to explore further.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
37. As a visitor, I want the site to adapt to my screen size (mobile, tablet, desktop), so that I can browse and shop comfortably on any device.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
38. As a visitor with accessibility needs, I want the site to follow accessibility best practices (screen reader support, keyboard navigation, sufficient colour contrast), so that I can use the site regardless of ability.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
39. As a visitor, I want easy and intuitive navigation throughout the site, so that I can find what I'm looking for without confusion.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

<details><summary>
40. As a user, I want clear feedback on all my relevant interactions with the website (adding to cart, submitting forms, completing payment, etc.), so that I always know the outcome of my actions.
</summary>

**Acceptance Criteria:**
- [ ]
- [ ]
- [ ]

</details>

