---
title: Design Decisions
nav_order: 3
---

{: .label }
[Kaan Deniz Gecer]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---

## Mandatory Technologies Defined by Course

### Meta

Status  
: Decided (external constraint)

Updated  
: 08-Feb-2026

### Problem statement

Certain core technologies for the semester project are predefined by the course rules and therefore not subject to our own architectural choice. These constraints must be documented explicitly so that one does not confuse them with design decisions taken by the team.

### Decision

We acknowledge that the following technologies are mandatory by course definition and therefore excluded from our design space:

- Programming language: Python.  
- Web framework: Flask.  
- Templating engine: Jinja2 for server-side HTML rendering.  
- Database: Relational database running locally, with SQLite recommended; remote databases (e.g., Firebase, hosted PostgreSQL) are not allowed.  
- Frontend: HTML + CSS rendered via Flask/Jinja2; no custom JavaScript is allowed, except Bootstrap’s built-in JavaScript if Bootstrap is used.  
- Application behavior: The app must handle multiple HTTP routes with non-trivial business logic and support user roles (e.g., anonymous vs. identified users).  
- Infrastructure: All components must run natively on current Windows or macOS; Docker, VMs, or similar containerization are not permitted.  

These items are treated as given constraints, not as design decisions by the team.

### Regarded options

Because these tools and technologies are mandated, we did not evaluate alternatives such as:

- Other backend frameworks (e.g., FastAPI, Django, Node.js).  
- Client-side JavaScript frameworks (e.g., React, Vue, Angular).  
- Cloud-hosted or NoSQL databases (e.g., Firebase, remote PostgreSQL, MongoDB).  
- Containerization or virtualization (e.g., Docker, virtual machines).  

---

## Technical design decisions

### 01: Authentication Flow

### Meta

Status  
: Decided

Updated  
: 08-Feb-2026

### Problem statement

The application must support different user roles and provide a secure, comprehensible authentication experience without client-side JavaScript. The login/signup process should minimize duplicated routes, keep URL structure simple, and ensure that customers cannot accidentally log in as producers (and vice versa), while still allowing future extensions of roles and profile data.

### Decision

This is an **Architectural design decision**.

We implement a multi-step, email-first authentication flow and centralize role handling in the `User` model, with separate customer and producer profiles:

- The application uses two main entry routes for auth: `/login` for customers and `/business` for producers. Both routes implement a step-based workflow controlled by the `step` query parameter (e.g. `step=email`, `step=password`, `step=signup`) instead of defining many separate endpoints.  
- In the customer flow (`/login`), the default `step="email"` uses `EmailOnlyLoginForm` to capture the email and check `User.query.filter_by(email=…)`. If a user exists, the flow redirects to `step="password"`; otherwise, it redirects to `step="signup"`. The password step uses `PasswordOnlyLoginForm` plus `check_password_hash` to authenticate; on success, `login_user(user)` is called and the user is redirected to `/account` for customers or `/business_account` for producers, depending on `user.role`.  
- In the producer flow (`/business`), we use a similar multi-step approach but enforce that only users with `role="PRODUCER"` can proceed. The landing step checks the email; if the user exists but has a different role, an error is added to the form and the login is refused. If a producer exists, the flow continues to the password step and logs the user into the business dashboard (`/business_account`). If not, the flow redirects to the producer signup step.  
- User identity and role are stored centrally in the `User` table (`id`, `email`, `password_hash`, `role`, etc.). Role-specific data is moved into one-to-one profile tables: `CustomerProfile` and `ProducerProfile`, each linked via `user_id`. The code consistently accesses `current_user.customer_profile` and `current_user.producer_profile` to retrieve role-specific information (e.g. address, products).  
- Role-based access and routing are enforced throughout the code using `@login_required` and `login_manager.login_view = "login"`. Customer-specific pages like `/account`, `/cart`, and `/address/edit` rely on `current_user.customer_profile`, while business pages like `/business/account`, `/business/products/new`, and `/business/profile/edit` require `current_user.producer_profile`. The business entry route short-circuits for already authenticated producers by redirecting them directly to `/business/account`.

This architecture keeps the URL surface small but expressive, ensures that producers cannot use the customer login flow (and vice versa), and keeps shared concerns (auth, passwords, role field) in one place while allowing the two roles to diverge in behavior and data through their dedicated profiles.

### Regarded options

**Separate endpoints per role and per step**  

- Example: `/login/email`, `/login/password`, `/signup/customer`, `/signup/producer`, `/business/login`, etc.  
- Pros: Very explicit URLs, simpler branching logic inside each route.  
- Cons: Many routes to implement and maintain, duplicated templates and business logic, higher risk of inconsistencies between flows.

**Single generic auth endpoint without explicit role separation**  

- Example: a single `/auth` route that handles all roles and both login and signup.  
- Pros: Minimal routing surface, simple URL structure.  
- Cons: Harder to enforce role-specific UX; producers could authenticate through the customer-facing flow; redirects to dashboards become ambiguous; complex conditional logic in one place.

**Chosen approach: multi-step email-first flow on a small set of role-specific routes**  

- `/login` for customers, `/business` for producers, with `step` indicating the current phase.  
- Pros:  
  - Avoids route explosion while maintaining clear separation of entry points per role.  
  - Email-first pattern allows early existence checks and tailored next steps without extra endpoints.  
  - Role-based redirects (`/account`, `/business_account`) are straightforward and predictable.  
  - Polymorphic profile design (shared `User`, dedicated profiles) keeps the schema normalized and extensible.  
- Cons:  
  - Route handlers must manage internal state via `step` and form data.  
  - Templates must cover multiple steps, increasing view complexity slightly.  

---

## Product and business decisions

### 01: USP – Local Producer Marketplace with Producer-Managed Inventory

### Meta

Status  
: Decided  

Updated  
: 08-Feb-2026  

### Problem statement

We need a clear value proposition that differentiates our app from generic online supermarkets or simple product catalogs. The course requires non-trivial business logic and meaningful user roles, so the core idea must justify why we have both producers and customers, producer dashboards, and an inventory model instead of a static content site.

### Decision

This is a **Product and business decision**.

We define our USP as a local producer marketplace where real producers manage their own inventory and profiles, and customers can discover them through dedicated producer and product overviews:

- Producers get a business area (`/business`, `/business/account`) where they can log in, maintain a profile, and manage their own products (create, edit, activate/deactivate).  
- Customers see a product overview (`/products`) and a producer overview (`/producers`, `/producer/<id>`) that highlight who is behind the products, not just the items themselves.  
- Orders are tied to both the customer (`Order.customer_id`) and the producer (`OrderItem.producer_id`), enabling producer-centric workflows (e.g. future per-producer order views).  
- The architecture (separate producer/customer roles, profile tables, product ownership, order structure) is chosen specifically to support this USP: the site is not a generic one-sided shop but a small marketplace emphasizing producers and their offerings.

### Regarded options

**Generic online shop focused only on products**  

- Products exist, but producers are not modeled as first-class entities; there is no business dashboard.  
- Pros: Simpler data model and fewer screens to implement.  
- Cons: No clear differentiation; weaker justification for separate roles and business logic; less interesting from an architectural perspective.

**Information portal about local food (no real inventory/ordering)**  

- Static pages about farms and markets without actual product management or ordering flows.  
- Pros: Very easy to implement; mainly content and simple routes.  
- Cons: Violates the spirit of a database-backed application with CRUD and meaningful workflows; no inventory, no cart, no orders.

**Chosen approach: local producer marketplace with producer-managed inventory**  

- Producers and their products are first-class citizens; customers browse both.  
- Pros:  
  - Justifies the two-role architecture and producer dashboard.  
  - Naturally leads to a richer data model (`User`, `ProducerProfile`, `Product`, `Order`, `OrderItem`).  
  - Aligns with the course requirement for multiple HTTP requests with distinct business logic.  
- Cons:  
  - Higher implementation effort (more routes, forms, and templates).  
  - Requires careful design of role-specific flows and permissions.  

---

## Additional minor design decisions

### User as central identity with role string

All humans are stored in one `User` table with shared fields (name, email, username, `password_hash`, `role`).  
The `role` field (e.g. `"CUSTOMER"`, `"PRODUCER"`) drives behavior and redirects, instead of separate tables per role.

### Address as reusable entity

`Address` is modeled as its own table and linked from profiles via `address_id`.  
This avoids duplicating address fields across `CustomerProfile` and `ProducerProfile` and allows re-use/updates in one place.

### Products owned by producers

`Product` records belong to a single `ProducerProfile` via `producer_id` and to a `Category` via `category_id`.  
This enables producer-specific inventories and category-based filtering.

### Session-based cart, not persisted as a separate model

The shopping cart is stored in the Flask `session` as a simple dict `{product_id: quantity}` and only turned into `Order`/`OrderItem` rows on checkout.  
This keeps the schema smaller and avoids cart cleanup logic in the database.
