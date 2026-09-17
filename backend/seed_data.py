"""
Database Seed Script (SOP Section 7.3 & 14)
Populates realistic sample departments and student records for demonstration.
Run with: python seed_data.py
"""
import os
import sys
import django
from datetime import date

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from students.models import Department, Student

def seed():
    print("--- Starting Database Seeding ---")

    # 1. Seed Departments
    departments_data = [
        {"name": "Computer Science & Engineering", "code": "CSE", "description": "Software, Algorithms, and Systems"},
        {"name": "Information Technology", "code": "IT", "description": "Networks, Cloud Computing, and Information Systems"},
        {"name": "Electronics & Communication", "code": "ECE", "description": "Hardware, Embedded Systems, and Telecommunications"},
        {"name": "Mechanical Engineering", "code": "MECH", "description": "Thermodynamics, Robotics, and Mechanics"},
        {"name": "Business Administration", "code": "MBA", "description": "Management, Finance, and Marketing"}
    ]

    dept_objs = {}
    for d in departments_data:
        obj, created = Department.objects.get_or_create(
            code=d["code"],
            defaults={"name": d["name"], "description": d["description"]}
        )
        dept_objs[d["code"]] = obj
        status_str = "Created" if created else "Existing"
        print(f"[{status_str}] Department: {obj.name} ({obj.code})")

    # 2. Seed Students
    students_data = [
        {
            "student_id": "STU2024001",
            "first_name": "Aarav",
            "last_name": "Sharma",
            "email": "aarav.sharma@university.edu",
            "phone": "+919876543210",
            "department": dept_objs["CSE"],
            "enrollment_date": date(2023, 8, 1),
            "gpa": 3.92,
            "status": "Active"
        },
        {
            "student_id": "STU2024002",
            "first_name": "Priya",
            "last_name": "Patel",
            "email": "priya.patel@university.edu",
            "phone": "+919876543211",
            "department": dept_objs["IT"],
            "enrollment_date": date(2023, 8, 1),
            "gpa": 3.84,
            "status": "Active"
        },
        {
            "student_id": "STU2024003",
            "first_name": "Rohan",
            "last_name": "Verma",
            "email": "rohan.verma@university.edu",
            "phone": "+919876543212",
            "department": dept_objs["ECE"],
            "enrollment_date": date(2022, 8, 1),
            "gpa": 3.45,
            "status": "Active"
        },
        {
            "student_id": "STU2024004",
            "first_name": "Ananya",
            "last_name": "Iyer",
            "email": "ananya.iyer@university.edu",
            "phone": "+919876543213",
            "department": dept_objs["CSE"],
            "enrollment_date": date(2021, 8, 1),
            "gpa": 3.98,
            "status": "Graduated"
        },
        {
            "student_id": "STU2024005",
            "first_name": "Marcus",
            "last_name": "Vance",
            "email": "marcus.v@university.edu",
            "phone": "+14155552671",
            "department": dept_objs["MECH"],
            "enrollment_date": date(2023, 8, 1),
            "gpa": 3.15,
            "status": "Active"
        },
        {
            "student_id": "STU2024006",
            "first_name": "Elena",
            "last_name": "Rostova",
            "email": "elena.r@university.edu",
            "phone": "+14155552672",
            "department": dept_objs["MBA"],
            "enrollment_date": date(2024, 1, 15),
            "gpa": 3.75,
            "status": "Active"
        },
        {
            "student_id": "STU2024007",
            "first_name": "Kavita",
            "last_name": "Reddy",
            "email": "kavita.reddy@university.edu",
            "phone": "+919876543214",
            "department": dept_objs["IT"],
            "enrollment_date": date(2022, 8, 1),
            "gpa": 2.80,
            "status": "Inactive"
        },
        {
            "student_id": "STU2024008",
            "first_name": "David",
            "last_name": "Kim",
            "email": "david.kim@university.edu",
            "phone": "+14155552673",
            "department": dept_objs["CSE"],
            "enrollment_date": date(2023, 8, 1),
            "gpa": 3.60,
            "status": "Active"
        }
    ]

    for s in students_data:
        obj, created = Student.objects.get_or_create(
            student_id=s["student_id"],
            defaults=s
        )
        status_str = "Created" if created else "Existing"
        print(f"[{status_str}] Student: {obj.student_id} - {obj.full_name}")

    print(f"\n--- Seeding Complete! Total Students: {Student.objects.count()}, Total Departments: {Department.objects.count()} ---")

if __name__ == '__main__':
    seed()
