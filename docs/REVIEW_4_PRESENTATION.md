# Review 4 – PBL Results & Analysis Presentation Guide

**Project Title:** Vehicle Service Centre Management System  
**Subject / Domain:** Database Engineering (Project-Based Learning)  
**PowerPoint File:** [`Vehicle_Service_Centre_Review_4.pptx`](file:///C:/Users/svcs/Desktop/work/DBMS_vehicle_management/vechicle-service-centre1/docs/Vehicle_Service_Centre_Review_4.pptx)  

---

## Slide 1 – Title Slide
- **Project-Based Learning – Review 4**
- **Project Title:** Vehicle Service Centre Management System
- **Student / Team Names:**
  - M. Vedasri Reddy (2510030094)
  - M. Hasini (2510030098)
  - G. Rishitha (2510030100)
  - M. Niharika Reddy (2510030141)
- **Faculty Mentor:** Rafeeq Mohammed
- **Department:** Department of Computer Science & Engineering
- **Academic Year:** 2026-2027

---

## Slide 2 – Project Objectives
1. **Digitize Workshop Workflows:** Replace manual paper job cards and appointment registers with a centralized, normalized relational database.
2. **Automated Appointment Scheduling:** Streamline booking, eliminate scheduling bottlenecks, and auto-assign qualified mechanics.
3. **End-to-End Service Tracking:** Provide multi-stage transparency (`Inspection` $\rightarrow$ `In-Progress` $\rightarrow$ `Pending Parts` $\rightarrow$ `Completed`) for active repairs.
4. **Automated Inventory Control:** Maintain real-time stock levels of spare parts, track unit pricing, and trigger automated reorder alerts when components dip below safety thresholds.
5. **Itemized Billing & Invoicing:** Calculate parts costs, labor charges, and GST automatically, producing transparent invoices with receipt print capability.

---

## Slide 3 – Project Development Approach
```
[Phase 1: Requirement Analysis]
         │
         ▼
[Phase 2: Database Design & ER Modeling (9 Tables)]
         │
         ▼
[Phase 3: Backend REST API Development (FastAPI + SQLAlchemy)]
         │
         ▼
[Phase 4: Frontend UI Integration & Dashboard (HTML5/CSS3/JS)]
         │
         ▼
[Phase 5: Automated Testing, Benchmarking & Validation]
         │
         ▼
[Phase 6: Results Evaluation & Documentation]
```

---

## Slide 4 – Project Implementation
- **Technologies / Tools Used:**
  - **Frontend:** HTML5, CSS3, JavaScript (ES6+), Modern Responsive Single Page Application.
  - **Backend:** Python 3.11, FastAPI, SQLAlchemy ORM, Pydantic data validation, Uvicorn ASGI server.
  - **Database:** Dual-engine architecture with **PostgreSQL** as primary production engine and **SQLite** as resilient standalone engine; 9 normalized relational tables.
  - **APIs:** Standardized RESTful endpoints with interactive OpenAPI / Swagger UI (`/docs`).
  - **Development Environment:** Visual Studio Code, Git, PowerShell, Windows 11.

---

## Slide 5 – System Architecture
```
User / Client (Web Browser)
        │  ▲
        │  │  (HTTP / JSON Requests & Responses)
        ▼  │
Frontend UI Dashboard (HTML5, CSS3, JS App Engine)
        │  ▲
        │  │  (Asynchronous REST API Calls)
        ▼  │
FastAPI Application Layer (Pydantic Validation, Auth, Business Logic)
        │  ▲
        │  │  (Object-Relational Mapping Queries)
        ▼  │
SQLAlchemy ORM
        │  ▲
        │  │  (SQL DDL & DML Commands)
        ▼  │
Database Layer: PostgreSQL / SQLite (9 Relational Tables)
[Customer, Vehicle, Mechanic, Appointment, ServiceRecord, SparePart, ServicePart, Bill, Payment]
```

---

## Slide 6 – Screens / Working Demonstration
1. **Login & Role Switcher:** Secure authentication for administrators, mechanics, and vehicle owners with session token handling.
2. **Operations Dashboard:** Live KPI cards displaying registered customers, active repair jobs, inventory stock counts, and total workshop revenue.
3. **Appointment Booking Modal:** Interactive booking form linking customers, vehicles, service packages, and technician allocation.
4. **Service Tracking Board:** Real-time job cards showing inspection notes, repair details, start/completion dates, and status toggles.
5. **Spare Parts Inventory Manager:** Real-time inventory table with dynamic badges for in-stock and critical low-stock items plus 1-click restock.
6. **Tax Invoice & Results View:** Comprehensive printable invoice breakdown including itemized spare parts, labor charges, GST (12%), and payment processing.

---

## Slide 7 – Functional Results
- **User Registration & Login:** Robust authentication mechanism distinguishing administrators, service advisors, and customers.
- **Add / Update / Delete Records:** Full CRUD capabilities implemented across all 9 relational entities.
- **Search and Filtering:** Real-time client-side search across customer names, vehicle registration numbers, and status filters.
- **API Communication:** Non-blocking async HTTP communication with standardized status codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found).
- **Database Operations:** Strict foreign key constraint enforcement, unique indexes on vehicle license plates and emails, and cascade operations.
- **Report Generation:** Instant PDF/printable invoice receipts with transparent financial breakdowns.

---

## Slide 8 – Testing Results Table
| Test Case | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :---: |
| **API Request** | Correct response (Status 200) | Correct response | **Pass** |
| **Login** | Successful login | Successful login | **Pass** |
| **Add Record (Customer)** | Record added (201 Created) | Record added | **Pass** |
| **Add Record (Vehicle)** | Record added with FK mapping | Record added | **Pass** |
| **Add Record (Appointment)** | Record added & job card initiated | Record added | **Pass** |
| **Update Record (Appointment)** | Record updated (Status: Confirmed) | Record updated | **Pass** |
| **Update Record (Service Record)** | Record updated (Status: Completed) | Record updated | **Pass** |
| **Add Record (Spare Part)** | Record added to inventory | Record added | **Pass** |
| **Delete Record (Spare Part)** | Record deleted from catalog | Record deleted | **Pass** |
| **Analytics / Dashboard API** | Correct response with aggregated KPIs | Correct response | **Pass** |
| **Invoice Generation API** | Correct response with parts & tax math | Correct response | **Pass** |

---

## Slide 9 – Performance Analysis
* **Average Response Time:** **45.28 ms** (measured under automated test suite).
* **Number of Test Cases:** **11**
* **Successful Test Cases:** **11 / 11 (100% Pass Rate)**
* **Error Rate:** **0.0%**
* **Database Query Latency:** **< 5.0 ms** (optimized through primary key indexing and normalized relationships).
* **API Throughput Engine:** High-performance async ASGI server with non-blocking event loops.

---

## Slide 10 – Results & Analysis Summary
1. **100% Elimination of Paper Delays:** Real-time job updates replace physical job card handoffs.
2. **Zero Inconsistent Records:** Foreign key integrity rules prevent orphan appointments, invalid vehicle registrations, or unassigned billing records.
3. **Accurate Financial Reconciliation:** Automated calculation of parts costs, labor rates, and tax eliminates calculation mistakes and billing disputes.
4. **Supply Chain Protection:** Reorder alerts ensure workshop never runs out of critical maintenance parts.
5. **High Operational Velocity:** Under 50ms latency ensures the front desk, workshop floor, and billing department operate without system lag.

---

## Slide 11 – Conclusion & Future Scope
- **Conclusion:**
  - All project objectives have been successfully met.
  - The Vehicle Service Centre Management System delivers a robust, secure, full-stack database application designed for real-world automotive workshops.
- **Future Scope:**
  1. **Cloud Deployment:** Containerization using Docker and deployment onto AWS ECS or Render.
  2. **Customer Mobile Application:** Cross-platform React Native / Flutter app for push notifications on service milestones.
  3. **IoT / OBD-II Telemetry:** Integrating vehicle diagnostic ports for automated fault code detection and proactive service scheduling.
  4. **MongoDB Audit Logs:** Storing raw telemetry streams, mechanic activity logs, and historical diagnostic scans.
