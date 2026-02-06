---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Jane Dane]

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

## Codemap

[Describe how your app is structured. Don't aim for completeness, rather describe *just* the most important parts.]

## Cross-cutting concerns

[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]
