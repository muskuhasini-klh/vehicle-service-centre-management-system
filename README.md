# Vehicle Service Centre Management System

> **Database Engineering PBL – Final Implementation & Review 4 Results**

A complete, full-stack, production-grade management system for automotive service centers, featuring a high-performance **FastAPI** backend, resilient **dual-database architecture** (PostgreSQL with seamless SQLite fallback), an interactive modern **frontend dashboard**, automated test suite, and complete **Review 4 presentation materials**.

---

## 👥 Project Team & Mentorship
- **M. Vedasri Reddy** (2510030094)
- **M. Hasini** (2510030098)
- **G. Rishitha** (2510030100)
- **M. Niharika Reddy** (2510030141)
- **Faculty Mentor:** Rafeeq Mohammed
- **Department:** Department of Computer Science & Engineering
- **Academic Year:** 2026-2027

---

## 📁 Repository File Structure

```
vechicle-service-centre1/
├── .env                              # Active environment configuration
├── .env.example                      # Configuration template
├── README.md                         # Project documentation and quick start guide
│
├── database/
│   ├── schema.sql                    # Normalized 9-table DDL schema for PostgreSQL
│   └── seed_data.py                  # Standalone script to populate sample test data
│
├── backend/
│   ├── database.py                   # Dual-engine connection manager (PostgreSQL + SQLite fallback)
│   ├── models.py                     # SQLAlchemy ORM models with 9 relational entities & cascades
│   ├── schemas.py                    # Pydantic schemas for Create, Update, Response & Auth
│   ├── auth.py                       # Password hashing & session token utilities
│   ├── main.py                       # FastAPI application with full CRUD, stats & static serving
│   ├── test_system.py                # Automated test suite (Slide 8 & 9 verification)
│   ├── vehicle_service.db            # Initialized SQLite database
│   └── venv/                         # Python 3.11 virtual environment
│
├── frontend/
│   ├── index.html                    # Responsive single-page application dashboard
│   ├── styles.css                    # Professional dark teal styling & print layout
│   └── app.js                        # Client application engine, live API fetch & modal handlers
│
└── docs/
    ├── Vehicle_Service_Centre_Review_4.pptx  # Editable PowerPoint Presentation deck for Review 4
    ├── generate_presentation.py      # Automated PPTX presentation generator script
    └── REVIEW_4_PRESENTATION.md      # Detailed slide-by-slide speaker notes & rubrics
```

---

## 🚀 How to Run the Application in VS Code

### 1. Open the Project in VS Code
Open folder:
`C:\Users\svcs\Desktop\work\DBMS_vehicle_management\vechicle-service-centre1`

### 2. Start the Backend & Web Dashboard
In the VS Code terminal (PowerShell):
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Access the Application
- **Web Dashboard:** Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Direct Frontend:** You can also open `frontend/index.html` directly in any browser.

---

## 🧪 Running Automated Tests (Review 4 Slide 8 & 9)

To verify all test cases and measure latency:
```powershell
cd backend
.\venv\Scripts\python.exe test_system.py
```

### Results Summary:
- **Test Cases:** 11 / 11 Passed (100% Pass Rate)
- **Error Rate:** 0.0%
- **Average Response Time:** ~45 ms

---

## 📊 PowerPoint Presentation for Review 4

The generated 16:9 widescreen presentation deck is located at:
`docs/Vehicle_Service_Centre_Review_4.pptx`

It contains all 11 required slides styled in the professional forest green and mint palette matching the PBL Review criteria.
