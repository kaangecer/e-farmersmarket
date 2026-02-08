---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

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

#### Meta
Status
: Decided (external constraint)

Updated
: 08-Feb-2026

#### Problem statement
Certain core technologies for the semester project are predefined by the course rules and therefore not subject to our own architectural choice. These constraints must be documented explicitly so that one does not confuse them with design decisions taken by the team.

#### Decision
We acknowledge that the following technologies are mandatory by course definition and therefore excluded from our design space:
​
Programming language: Python.

Web framework: Flask.

Templating engine: Jinja2 for server-side HTML rendering.

Database: Relational database running locally, with SQLite recommended; remote databases (e.g., Firebase, hosted PostgreSQL) are not allowed.

Frontend: HTML + CSS rendered via Flask/Jinja2; no custom JavaScript is allowed, except Bootstrap’s built-in JavaScript if Bootstrap is used.

Application behavior: The app must handle multiple HTTP routes with non-trivial business logic and support user roles (e.g., anonymous vs. identified users).

Infrastructure: All components must run natively on current Windows or macOS; Docker, VMs, or similar containerization are not permitted.

These items are treated as given constraints, not as design decisions by the team.

#### Regarded options
Because these tools and technologies are mandated, we did not evaluate alternatives such as:

---
## Architectural design decisions

### 01: [Title]

#### Meta

Status
: **Work in progress** - Decided - Obsolete

Updated
: DD-MMM-YYYY

#### Problem statement

[Describe the problem to be solved or the goal to be achieved. Include relevant context information.]

#### Decision

[Describe **which** design decision was taken for **what reason** and by **whom**.]

#### Regarded options

[Describe any possible design decision that will solve the problem. Assess these options, e.g., via a simple pro/con list.]


---
## Product and business decisions

---
## Operational and data design decisions

---