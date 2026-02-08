---
title: Route Details
parent: Reference documentation
nav_order: 1
---

{: .no_toc }
# Route Details

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---

## Home
**Route:** `/`  
**Methods:** `GET`  
**Purpose:** Render the home page.

---

## Products
**Route:** `/products`  
**Methods:** `GET`  
**Purpose:** Show all active products and categories.

---

## Producer JSON
**Route:** `/producer/<int:producer_id>/json`  
**Methods:** `GET`  
**Purpose:** Return producer profile and address as JSON.

---

## Producer Details
**Route:** `/producer/<int:producer_id>`  
**Methods:** `GET`  
**Purpose:** Show producer details page.

---

## Cart Add (JSON)
**Route:** `/cart/add-json`  
**Methods:** `POST`  
**Purpose:** Add a product to cart via JSON API.

---

## Producers List
**Route:** `/producers`  
**Methods:** `GET`  
**Purpose:** Show all producers.

---

## Maps
**Route:** `/maps`  
**Methods:** `GET`  
**Purpose:** Show map page.

---

## Cart
**Route:** `/cart`  
**Methods:** `GET`, `POST`  
**Purpose:** Show cart page and handle checkout.

---

## Login
**Route:** `/login`  
**Methods:** `GET`, `POST`  
**Purpose:** Customer login/signup workflow.

---

## Account
**Route:** `/account`  
**Methods:** `GET`  
**Purpose:** Show customer account page and orders.

---

## Logout
**Route:** `/logout`  
**Methods:** `POST`  
**Purpose:** Log out current user.

---

## Business Login/Signup
**Route:** `/business`  
**Methods:** `GET`, `POST`  
**Purpose:** Producer login/signup workflow.

---

## Business Account
**Route:** `/business/account`  
**Methods:** `GET`  
**Purpose:** Show producer dashboard with products.

---

## Edit Producer Profile
**Route:** `/business/profile/edit`  
**Methods:** `GET`, `POST`  
**Purpose:** Edit producer profile.

---

## Edit Address
**Route:** `/address/edit`  
**Methods:** `GET`, `POST`  
**Purpose:** Edit address for customer or producer.

---

## Create Product
**Route:** `/business/products/new`  
**Methods:** `GET`, `POST`  
**Purpose:** Create new product (producer).

---

## Edit Product
**Route:** `/business/products/<int:product_id>/edit`  
**Methods:** `GET`, `POST`  
**Purpose:** Edit existing product (producer).

---

## Business Order Detail
**Route:** `/business/orders/<int:order_id>`  
**Methods:** `GET`  
**Purpose:** Show order details for producer.

---

## Delete Account
**Route:** `/delete_account`  
**Methods:** `POST`  
**Purpose:** Delete current user account.
