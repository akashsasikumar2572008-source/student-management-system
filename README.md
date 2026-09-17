# Student Management System (EduTrack Pro)
**Complete CRUD-Based Web Application Development**  
*Compliant with Standard Operating Procedure (SOP) Guidelines*

![Tech Stack](https://img.shields.io/badge/Stack-Django%20REST%20%7C%20JavaScript%20%7C%20SQLite-blue)
![Architecture](https://img.shields.io/badge/Architecture-3--Tier%20RESTful-green)
![Status](https://img.shields.io/badge/Testing-100%25%20Passed-success)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/akashsasikumar2572008-source/student-management-system)

**Repository Link**: [https://github.com/akashsasikumar2572008-source/student-management-system](https://github.com/akashsasikumar2572008-source/student-management-system)

---

## 📖 Overview
EduTrack Pro is a production-grade, full-stack Student Management System designed and built in strict accordance with the **Standard Operating Procedure (SOP)**. The application provides end-to-end Create, Read, Update, and Delete (CRUD) operations, client-side and server-side validation, relational database persistence, responsive mobile-friendly UI, and a complete suite of automated tests and documentation.

---

## 🌟 Key Features
- **Full CRUD Capabilities**:
  - **Create**: Add new students with roll number, department, admission date, contact info, and GPA.
  - **Read**: Live table with statistics, department tags, status badges, and aggregate metrics.
  - **Update**: Edit existing student records with prefilled modal forms and real-time feedback.
  - **Delete**: Remove records with dedicated confirmation modal to prevent accidental loss.
- **Search & Filter**: Real-time debounced search by name/ID/email and filtering by department and status.
- **Two-Tier Validation**:
  - *Client-side*: Real-time HTML5 and JavaScript regex and range validation.
  - *Server-side*: Django REST Framework serializers enforcing uniqueness, format, and 0.00–4.00 GPA constraints.
- **Relational Integrity**: Foreign-key relation linking `Student` records to academic `Department` entities with `ON DELETE PROTECT`.
- **Responsive Design**: Fluid UI tested across desktop, tablet, and mobile displays.
- **API Testing**: Exportable Postman collection (`v2.1`) and Django automated unit test suite.

---

## 🗂️ Project Directory Structure

```
student-management-system/
├── backend/
│   ├── manage.py                   # Django CLI utility
│   ├── requirements.txt            # Python dependencies
│   ├── seed_data.py                # Database seeder (creates departments & students)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py             # Settings with CORS, DRF, and SQLite
│   │   ├── urls.py                 # Core routing
│   │   └── wsgi.py                 # WSGI application
│   └── students/
│       ├── __init__.py
│       ├── admin.py                # Django admin registration
│       ├── apps.py                 # App configuration
│       ├── models.py               # Department & Student models
│       ├── serializers.py          # DRF serializers with validation logic
│       ├── urls.py                 # REST API routes
│       ├── views.py                # StudentViewSet & DepartmentViewSet
│       ├── tests.py                # Automated APITestCase suite
│       └── migrations/
│           ├── __init__.py
│           └── 0001_initial.py     # Initial relational database schema
├── frontend/
│   ├── index.html                  # Dashboard, modals, and responsive tables
│   ├── css/
│   │   └── styles.css              # Modern CSS variables, grid, flexbox, animations
│   └── js/
│       ├── api.js                  # Modular Fetch API REST client
│       └── app.js                  # UI Controller, state, validation, and rendering
├── docs/
│   ├── PROJECT_REPORT.md           # SOP Section 13 full academic project report
│   ├── API_DOCUMENTATION.md        # Detailed REST API specification
│   └── Student_Management_API.postman_collection.json # Ready-to-import Postman suite
├── run_backend.bat                 # One-click Windows launcher for backend
├── run_frontend.bat                # One-click Windows launcher for frontend
├── .gitignore                      # Git ignore file
└── README.md                       # Master instructions
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python** (version 3.8 to 3.12)
  *(If Python is not yet installed on Windows, install via Microsoft Store, Python.org, or `winget install Python.Python.3.12`)*

### 1. Backend Setup & Run
Open a terminal (PowerShell or Command Prompt) and run:

```powershell
cd backend

# 1. Install required packages
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py migrate

# 3. Seed initial sample data (Departments and sample Students)
python seed_data.py

# 4. Start the Django development server
python manage.py runserver 127.0.0.1:8000
```
> The REST API will be active at: `http://127.0.0.1:8000/api/`

### 2. Frontend Launch
Simply open `frontend/index.html` in any web browser (Chrome, Edge, Firefox, Safari).  
Alternatively, double-click `run_frontend.bat` or use any static server:
```powershell
# Optional using python:
cd frontend
python -m http.server 3000
```
Open `http://127.0.0.1:3000` in your browser.

---

## 🧪 Running Automated Tests (SOP Section 10)

To execute the automated test suite covering all CRUD endpoints and validation boundary cases:
```powershell
cd backend
python manage.py test students -v 2
```

### Expected Output:
```text
test_create_student_duplicate_email (students.tests.StudentAPITests) ... ok
test_create_student_duplicate_student_id (students.tests.StudentAPITests) ... ok
test_create_student_invalid_gpa_range (students.tests.StudentAPITests) ... ok
test_create_student_missing_mandatory_fields (students.tests.StudentAPITests) ... ok
test_create_student_valid_data (students.tests.StudentAPITests) ... ok
test_dashboard_stats_endpoint (students.tests.StudentAPITests) ... ok
test_delete_student_invalid_id (students.tests.StudentAPITests) ... ok
test_delete_student_valid_id (students.tests.StudentAPITests) ... ok
test_filter_student_by_department (students.tests.StudentAPITests) ... ok
test_partial_update_student (students.tests.StudentAPITests) ... ok
test_read_all_students (students.tests.StudentAPITests) ... ok
test_read_single_student_invalid_id (students.tests.StudentAPITests) ... ok
test_read_single_student_valid_id (students.tests.StudentAPITests) ... ok
test_search_student_by_name (students.tests.StudentAPITests) ... ok
test_update_student_valid_data (students.tests.StudentAPITests) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.421s

OK
```

---

## 📮 Postman API Testing (SOP Section 4 & 10)
1. Open **Postman**.
2. Click **Import** and select `docs/Student_Management_API.postman_collection.json`.
3. Ensure the backend server is running on `http://127.0.0.1:8000`.
4. Click **Run Collection** to automatically execute all 10 endpoint tests with automated status code assertions.

---

## 📊 Evaluation Rubric Mapping (SOP Section 16)

| SOP Component | Weightage | Evidence in this Project |
| :--- | :--- | :--- |
| **Requirement & Design** | 10% | Problem definition, 3-tier architecture, and ER diagram in `docs/PROJECT_REPORT.md`. |
| **Frontend** | 20% | Semantic HTML5, responsive CSS3 design, dynamic cards & table, modals, live filter. |
| **Backend / API** | 20% | Django REST Framework ModelViewSets, serializers, error codes, and CORS headers. |
| **CRUD Functionality** | 20% | Create, Read, Update, and Delete fully operational and synchronized. |
| **Database** | 10% | Relational schema (`Department` 1:N `Student`), unique constraints, migration scripts. |
| **Testing** | 10% | 15 automated Django unit test cases + Postman collection with test assertions. |
| **Documentation & Viva** | 10% | Detailed project report (`PROJECT_REPORT.md`), API reference, and Viva Q&A guide. |

---

## 👨‍🏫 Final Demonstration Checklist (SOP Section 17)
- [x] Application starts without errors.
- [x] Database connection works correctly.
- [x] Create operation works with client & server validation.
- [x] Read/list operation works with statistics and badges.
- [x] Update operation works with prefilled form.
- [x] Delete operation works with confirmation modal.
- [x] Validation catches empty fields, invalid emails, and out-of-range GPAs.
- [x] Search & filter works in real-time.
- [x] All REST API endpoints demonstrated with Postman.
- [x] Source code and documentation completely packaged.
