# Calendar Application (FastAPI + React + Schedule-X)

A full-stack calendar system where users can authenticate, create events, invite participants, and receive email notifications upon event creation.  
The application features a clean backend architecture using FastAPI and PostgreSQL, and a modern React frontend powered by Schedule-X.

---

## **1. Features**

### Authentication
- Email + password login
- Google OAuth login
- LocalStorage-based session persistence

### Calendar UI
- Weekly and monthly views (Schedule-X)
- Dynamically loads the logged user's events
- Click event → show details modal

### Event Creation
- Title, description, date  
- Start/end time (15-minute rounding)
- Location
- Participant search with auto-complete
- Stored in PostgreSQL

### Participants
- Search users by partial email (substring)
- Add/remove participants dynamically
- Each participant automatically sees the event in their calendar

### Email Notifications
- Sent to all invited participants
- Implemented using **Strategy Pattern**
- Triggered automatically using **Observer Pattern**
- SMTP support (Gmail)

---

##  **2. Technologies Used**

### Backend
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Alembic** (migrations)
- **Authlib** (Google OAuth)
- **SMTP email sender (smtplib)**

### Frontend
- **React**
- **React Router**
- **Schedule-X Calendar**
- **Custom Event Creation Modal**
- **LocalStorage auth**

---

## **3. Design Patterns Used**

This project applies the **Strategy** and **Observer** design patterns because they provide practical architectural benefits and are directly required by the application's workflow.

---

# 3.1. **Why These Design Patterns Were Used**

### **Observer Pattern – event-driven architecture**
The application needs to perform additional actions automatically when an event is created.
Currently, the only action is sending email notifications to invited participants, but the Observer pattern ensures that the event creation logic remains decoupled from notification logic.
Even if there is only one subscriber, the architecture allows adding new behaviors (logging, metrics, push notifications, syncing to external systems) without modifying the event creation service.

---

### **Strategy Pattern – different notification channels**
Notification delivery should be independent from event creation or business logic.
Strategy allows the application to define different notification delivery mechanisms (email, SMS, in-app, push) and swap them without modifying the event-creation code.
The event service only calls a strategy interface, remaining unaware of the actual notification channel

---

# 3.1. **What problems does these design pattern solve**

### **Observer Pattern**
- Prevents the event creation service from containing notification logic, keeping business code clean.
- Avoids tight coupling between event creation and side effects.
- Makes it possible to extend the behavior triggered by event creation (adding logging, analytics, webhooks, etc.) without editing the core service.

---

### **Strategy Pattern**
- Removes hard-coded SMTP or notification logic from business services.
- Allows adding new notification channels without changing the event creation code.
- Centralizes notification behavior into a reusable, interchangeable component.
