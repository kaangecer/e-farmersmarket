---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Kaan Deniz Gecer]

{: .no_toc }
# Architecture

{: .attention }
> This page describes how the application is structured and how important parts of the app work. It should give a new-joiner sufficient technical knowledge for contributing to the codebase.
> 
> See [this blog post](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) for an explanation of the concept and these examples:
>
> + <https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md>
> + <https://github.com/Uriopass/Egregoria/blob/master/ARCHITECTURE.md>
> + <https://github.com/davish/obsidian-full-calendar/blob/main/src/README.md>
> 
> For structural and behavioral illustration, you might want to leverage [Mermaid](../ui-components.md), e.g., by charting common [C4](https://c4model.com/) or [UML](https://www.omg.org/spec/UML) diagrams.
> 
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

FoodLoop is a web application that connects local farmers and food producers with nearby consumers, focusing on transparency, short supply chains, and reduced food waste. It provides a simple marketplace-like interface where producers can present their offerings and products and consumers can discover, compare, and plan their weekly grocery needs.

The application follows a classic web architecture. HTTP requests hit a Flask backend that manages routing, business logic, and database access, while Jinja templates render HTML pages sent back to the browser. This seperation keep templates, Flask routes, forms, and database/models structured and seperated. Thus, new contributors can reason about changes in one layer at a time.

[Give a high-level overview of what your app does and how it achieves it: similar to the value proposition, but targeted at a fellow developer who wishes to contribute.]

--- 

## Codemap

The FoodLoop web application is organized around four main areas: the application entry point, forms, the data model (including initial data), and the UI layer.

### Application file (app.py) 
This is the central entry point of the web app. It creates and configures the Flask application instance, sets up the database connection, and registers all routes. In app.py, URLs are mapped to view functions that handle incoming HTTP requests, prepare data, and select which template to render.

### Forms (forms.py) 
Forms encapsulate user input and validation logic for key interactions such as signing up, logging in, and creating or editing producer and product entries. Each form class defines the fields, validation rules, and error messages, so route functions can work with already-validated data instead of manually checking every field.

### Data model and initial data seeding (models.py, seed_data.py) 
The data model defines the core entities of FoodLoop (for example, users, producers, and products) and how they relate to each other. These model classes map to database tables and provide a structured way to query and update application data. Initial data seeding scripts populate the database with a basic set of users, producers, and products, allowing developers to start the app with realistic test data and making it easier to demo the core flows.

### UI (HTML templates and styling) 
The UI is built with Jinja-powered HTML templates and shared stylesheets. A base layout defines the common page frame (navigation, header, footer), while feature-specific templates render lists, details, and forms for different parts of the app. Styling is handled through CSS files in the static assets, giving the application a consistent look and feel across all pages.


[Describe how your app is structured. Don't aim for completeness, rather describe *just* the most important parts.]

--- 

## Cross-cutting concerns

This section describes anything that is important for a solid understanding of our codebase and its behaviour.

### Routing and request flow 
Every browser request starts in app.py, where routes define what should happen for a given URL and HTTP method. \ A typical request flow is: \ the browser calls a route → the route creates/validates a form or reads query parameters → it talks to the data model to fetch or update records → it passes the result into a Jinja template, \ which renders the final HTML page. Understanding this **request → route → model → template** chain is key for debugging and extending features.

### Forms and validation 
User input is never trusted directly from request.form. Instead, forms encapsulate which fields exist and how they are validated (required, length, format, etc.). Routes call the form’s validation method and only proceed with database writes when validation passes. \ This means that whenever you add a new interaction (like a new kind of submission or edit), you typically have to touch three spots: define or extend a form, update a route to use it, and adjust the template to render fields and show validation errors.

### Authentication, authorization, and protected actions 
Any route that exposes personalized or sensitive data—such as a producer editing their products or a user viewing their own information—depends on authentication and authorization checks. These checks live in decorators or helper functions but depend on data from the model (User.ROLE="customer" or "producer"). When adding new routes that read or modify data, it’s essential to ask *who is logged in?* and reuse the existing patterns so that security and functinoality is consistent across the app.




[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]
