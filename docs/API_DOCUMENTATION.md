# Student Management System - REST API Reference Documentation

**Base URL**: `http://127.0.0.1:8000/api`  
**Content-Type**: `application/json`

---

## Overview of Endpoints

| Resource | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Students** | `GET` | `/students/` | List all students (supports search & filters) |
| **Students** | `POST` | `/students/` | Create a new student record |
| **Students** | `GET` | `/students/{id}/` | Retrieve single student by primary key ID |
| **Students** | `PUT` | `/students/{id}/` | Update all fields of an existing student |
| **Students** | `PATCH` | `/students/{id}/` | Partially update student fields |
| **Students** | `DELETE` | `/students/{id}/` | Delete student record |
| **Statistics** | `GET` | `/students/stats/` | Retrieve aggregate metrics for dashboard |
| **Departments** | `GET` | `/departments/` | List all departments |
| **Departments** | `POST` | `/departments/` | Create a new department |

---

## 1. List All Students

- **URL**: `/api/students/`
- **Method**: `GET`
- **Query Parameters**:
  - `search` *(optional, string)*: Filter by student roll number, first name, last name, or email.
  - `department` *(optional, integer)*: Filter by department ID.
  - `status` *(optional, string)*: Filter by status (`Active`, `Inactive`, `Graduated`, `Suspended`).

### Example Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/students/?search=Aarav&status=Active"
```

### Response (200 OK):
```json
[
  {
    "id": 1,
    "student_id": "STU2024001",
    "first_name": "Aarav",
    "last_name": "Sharma",
    "full_name": "Aarav Sharma",
    "email": "aarav.sharma@university.edu",
    "phone": "+919876543210",
    "department": 1,
    "department_name": "Computer Science & Engineering",
    "department_code": "CSE",
    "enrollment_date": "2023-08-01",
    "gpa": "3.92",
    "status": "Active",
    "created_at": "2026-09-17T10:00:00Z",
    "updated_at": "2026-09-17T10:00:00Z"
  }
]
```

---

## 2. Retrieve Single Student

- **URL**: `/api/students/{id}/`
- **Method**: `GET`

### Example Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/students/1/"
```

### Response (200 OK):
```json
{
  "id": 1,
  "student_id": "STU2024001",
  "first_name": "Aarav",
  "last_name": "Sharma",
  "full_name": "Aarav Sharma",
  "email": "aarav.sharma@university.edu",
  "phone": "+919876543210",
  "department": 1,
  "department_name": "Computer Science & Engineering",
  "department_code": "CSE",
  "enrollment_date": "2023-08-01",
  "gpa": "3.92",
  "status": "Active",
  "created_at": "2026-09-17T10:00:00Z",
  "updated_at": "2026-09-17T10:00:00Z"
}
```

---

## 3. Create Student

- **URL**: `/api/students/`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`

### Request Payload:
```json
{
  "student_id": "STU2026099",
  "first_name": "Elena",
  "last_name": "Gilbert",
  "email": "elena.g@university.edu",
  "phone": "+14155551234",
  "department": 1,
  "enrollment_date": "2026-09-01",
  "gpa": 3.85,
  "status": "Active"
}
```

### Response (201 Created):
```json
{
  "status": "success",
  "message": "Student 'Elena Gilbert' created successfully.",
  "data": {
    "id": 9,
    "student_id": "STU2026099",
    "first_name": "Elena",
    "last_name": "Gilbert",
    "full_name": "Elena Gilbert",
    "email": "elena.g@university.edu",
    "phone": "+14155551234",
    "department": 1,
    "department_name": "Computer Science & Engineering",
    "department_code": "CSE",
    "enrollment_date": "2026-09-01",
    "gpa": "3.85",
    "status": "Active",
    "created_at": "2026-09-17T11:00:00Z",
    "updated_at": "2026-09-17T11:00:00Z"
  }
}
```

### Validation Error Response (400 Bad Request):
```json
{
  "status": "error",
  "message": "Validation failed. Please correct the highlighted errors.",
  "errors": {
    "student_id": ["A student with ID 'STU2026099' already exists."],
    "gpa": ["GPA must be between 0.00 and 4.00."]
  }
}
```

---

## 4. Update Student

- **URL**: `/api/students/{id}/`
- **Method**: `PUT`
- **Headers**: `Content-Type: application/json`

### Request Payload:
```json
{
  "student_id": "STU2026099",
  "first_name": "Elena",
  "last_name": "Salvatore",
  "email": "elena.salvatore@university.edu",
  "phone": "+14155551234",
  "department": 2,
  "enrollment_date": "2026-09-01",
  "gpa": 3.95,
  "status": "Graduated"
}
```

### Response (200 OK):
```json
{
  "status": "success",
  "message": "Student 'Elena Salvatore' updated successfully.",
  "data": {
    "id": 9,
    "student_id": "STU2026099",
    "first_name": "Elena",
    "last_name": "Salvatore",
    "full_name": "Elena Salvatore",
    "email": "elena.salvatore@university.edu",
    "department": 2,
    "department_name": "Information Technology",
    "department_code": "IT",
    "gpa": "3.95",
    "status": "Graduated"
  }
}
```

---

## 5. Delete Student

- **URL**: `/api/students/{id}/`
- **Method**: `DELETE`

### Response (200 OK):
```json
{
  "status": "success",
  "message": "Student 'Elena Salvatore' has been deleted."
}
```

---

## 6. Dashboard Statistics

- **URL**: `/api/students/stats/`
- **Method**: `GET`

### Response (200 OK):
```json
{
  "total_students": 8,
  "active_students": 6,
  "average_gpa": 3.56,
  "by_department": [
    { "department__name": "Computer Science & Engineering", "department__code": "CSE", "count": 3 },
    { "department__name": "Information Technology", "department__code": "IT", "count": 2 }
  ],
  "by_status": [
    { "status": "Active", "count": 6 },
    { "status": "Graduated", "count": 1 },
    { "status": "Inactive", "count": 1 }
  ]
}
```
