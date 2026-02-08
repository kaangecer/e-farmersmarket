---
title: Summary of individual contributions
parent: Team Evaluation
nav_order: 4
---

{: .no_toc }
# Summary of individual contributions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Diego Jahndorf

### Contributions
- **Homepage: Design + Inhalt + statische Berlin-Map mit Pins**
  - home.html (Hero, Sections, Map-Preview, Produzenten-Pins, CTA)
  - home.css (Layout, Typo, Hero-Design, Map-Preview, Pins, Responsive)
  - app.py (Homepage-Route mit map_pins Datenquelle)

- **Produzentenprofil + Funktionen (weiterentwickelt / vervollständigt)**
  - business_account.html (Producer-Dashboard: Profilinfos, Produkte-Liste, Bestellungen)
  - edit_producer_profile.html (Profil bearbeiten)
  - edit_address.html (Adresse bearbeiten)
  - product_form.html (Produkt anlegen/bearbeiten)
  - forms.py (Erweiterungen/Anpassungen für Producer-Forms, z. B. SignupFormProducers, ProductForm mit Kategorie)
  - app.py (Business-Routes, Producer-Login/Signup-Flow, Produkt anlegen/bearbeiten, Address/Profile-Edit)

- **Seiten „Produzenten“ und „Produkte“ (Bearbeitung/Erweiterung)**
  - producers.html (Produzenten-Übersicht)
  - producer_details.html (Detailseite Produzent)
  - products.html (Produkt-Übersicht)
  - app.py (Routes für producers, producer_detail, products)


## Kaan Deniz Gecer

### Contributionas
- **app.py route architecture.**
  - Aufbau der grundlegenden Routenstruktur (Customer-Flow), inkl. Mapping von URLs zu Views und Templates für Listen-, Detail- und Account-Seiten
  - Implementierung der role-basierten Logik im Backend (Unterscheidung Customer vs. Producer) 
  - Anbindung der Routen an die Datenbank-Modelle, sodass Produkte, Profile und Bestellungen konsistent geladen und gespeichert werden

- **Email-first-login Workflow**
  - Konzeption und Implementierung des mehrstufigen, E‑Mail‑first Authentifizierungsflows mit step-Parameter (E-Mail, Passwort, Signup), wiederverwendet für Customer und Producer
  - Role-Handling im User-Modell, sodass jede Session klar einem Rollen-Typ zugeordnet ist und nicht versehentlich beide Rollen gleichzeitig aktiv werden

- **Data Model**
  - Vollstandige erstellung des Datenmodells.
  - Implementierung zentraler SQLAlchemy-Modelle und ihrer Beziehungen, sodass die wichtigsten Entitäten im System konsistent miteinander verknüpft sind (siehe Visual overview Data Model)

- **Forms.py**
  - Implementierung und Erweiterung zentraler Flask-WTF-Forms in forms.py, insbesondere für Authentifizierung und Kund:innen-Seiten (z. B. E-Mail-first-Login mit EmailOnlyLoginForm und PasswordOnlyLoginForm)
  - Abstimmung der Form-Felder mit dem Datenmodell (User, Address, Profile), inklusive Validierung und Fehlerbehandlung, sodass Formulardaten sauber in die zugehörigen SQLAlchemy-Modelle übernommen werden können

- **Cart Functionality**
  - Implementierung der Warenkorb-Logik, inklusive Route, Session-Nutzung und Verknüpfung mit dem eingeloggten User für den Checkout
  - Aufbau eines Checkout-Forms (CartForm) mit Validierung für Kontakt-, Adress- und Zahlungsdaten sowie Einbindung in die Cart-Seite
  - Erweiterung der Produkt- und Produzentenseiten um „In den Warenkorb“-Funktionalität und Darstellung der aktuellen Cart-Inhalte auf der Cart-Seite
