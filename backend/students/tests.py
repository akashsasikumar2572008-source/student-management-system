from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from .models import Department, Student

class StudentAPITests(APITestCase):
    """
    Automated Test Suite for Student Management System CRUD operations
    Strictly follows SOP Section 10 (Testing Procedure) & Section 16 (Evaluation Rubric).
    """

    def setUp(self):
        # Setup initial Department
        self.dept_cs = Department.objects.create(
            name="Computer Science & Engineering",
            code="CSE",
            description="Computer Science Department"
        )
        self.dept_it = Department.objects.create(
            name="Information Technology",
            code="IT",
            description="Information Technology Department"
        )

        # Setup initial Student
        self.student1 = Student.objects.create(
            student_id="STU2026001",
            first_name="Alice",
            last_name="Johnson",
            email="alice.j@university.edu",
            phone="+1234567890",
            department=self.dept_cs,
            enrollment_date=date(2023, 8, 15),
            gpa=3.85,
            status="Active"
        )

        self.list_url = reverse('student-list')
        self.detail_url = reverse('student-detail', kwargs={'pk': self.student1.pk})

    # ==================== READ TESTS ====================
    def test_read_all_students(self):
        """Test GET /api/students/ returns list with 200 OK (SOP 7.6)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DRF without pagination returns a list
        data = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['student_id'], "STU2026001")

    def test_read_single_student_valid_id(self):
        """Test GET /api/students/{id}/ returns single student with 200 OK"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_id'], "STU2026001")
        self.assertEqual(response.data['first_name'], "Alice")
        self.assertEqual(response.data['department_code'], "CSE")

    def test_read_single_student_invalid_id(self):
        """Test GET /api/students/{invalid_id}/ returns 404 NOT FOUND"""
        invalid_url = reverse('student-detail', kwargs={'pk': 99999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==================== CREATE TESTS ====================
    def test_create_student_valid_data(self):
        """Test POST /api/students/ creates record and returns 201 CREATED (SOP 7.6)"""
        payload = {
            "student_id": "STU2026002",
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@university.edu",
            "phone": "+9876543210",
            "department": self.dept_it.id,
            "enrollment_date": "2024-01-10",
            "gpa": 3.45,
            "status": "Active"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(student_id="STU2026002").exists())
        created = Student.objects.get(student_id="STU2026002")
        self.assertEqual(created.first_name, "Bob")
        self.assertEqual(created.department.code, "IT")

    def test_create_student_duplicate_student_id(self):
        """Test POST with duplicate student_id returns 400 BAD REQUEST (SOP 9)"""
        payload = {
            "student_id": "STU2026001",  # Duplicate ID
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie.b@university.edu",
            "department": self.dept_cs.id,
            "enrollment_date": "2024-01-10",
            "gpa": 3.00,
            "status": "Active"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already exists", str(response.data))

    def test_create_student_duplicate_email(self):
        """Test POST with duplicate email returns 400 BAD REQUEST (SOP 9)"""
        payload = {
            "student_id": "STU2026999",
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "alice.j@university.edu",  # Duplicate email
            "department": self.dept_cs.id,
            "enrollment_date": "2024-01-10",
            "gpa": 3.00,
            "status": "Active"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already registered", str(response.data))

    def test_create_student_invalid_gpa_range(self):
        """Test POST with GPA > 4.00 or < 0.00 returns 400 BAD REQUEST (SOP 9)"""
        payload = {
            "student_id": "STU2026003",
            "first_name": "David",
            "last_name": "Miller",
            "email": "david.m@university.edu",
            "department": self.dept_cs.id,
            "enrollment_date": "2024-01-10",
            "gpa": 4.50,  # Invalid GPA (>4.0)
            "status": "Active"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_missing_mandatory_fields(self):
        """Test POST with missing required fields returns 400 BAD REQUEST (SOP 9)"""
        payload = {
            "student_id": "STU2026004"
            # Missing name, email, department, gpa, enrollment_date
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ==================== UPDATE TESTS ====================
    def test_update_student_valid_data(self):
        """Test PUT /api/students/{id}/ updates record and returns 200 OK (SOP 7.6)"""
        payload = {
            "student_id": "STU2026001",
            "first_name": "Alice",
            "last_name": "Williams",  # Updated surname
            "email": "alice.williams@university.edu",  # Updated email
            "phone": "+1234567890",
            "department": self.dept_it.id,  # Switched department
            "enrollment_date": "2023-08-15",
            "gpa": 3.95,  # Updated GPA
            "status": "Graduated"  # Updated status
        }
        response = self.client.put(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student1.refresh_from_db()
        self.assertEqual(self.student1.last_name, "Williams")
        self.assertEqual(self.student1.department.code, "IT")
        self.assertEqual(float(self.student1.gpa), 3.95)
        self.assertEqual(self.student1.status, "Graduated")

    def test_partial_update_student(self):
        """Test PATCH /api/students/{id}/ updates single field (SOP 7.6)"""
        payload = {"gpa": 3.99}
        response = self.client.patch(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student1.refresh_from_db()
        self.assertEqual(float(self.student1.gpa), 3.99)

    # ==================== DELETE TESTS ====================
    def test_delete_student_valid_id(self):
        """Test DELETE /api/students/{id}/ deletes record and returns 200 OK (SOP 7.6)"""
        response = self.client.delete(self.detail_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.assertFalse(Student.objects.filter(pk=self.student1.pk).exists())

    def test_delete_student_invalid_id(self):
        """Test DELETE /api/students/{invalid_id}/ returns 404 NOT FOUND (SOP 10)"""
        invalid_url = reverse('student-detail', kwargs={'pk': 88888})
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==================== SEARCH & FILTER TESTS ====================
    def test_search_student_by_name(self):
        """Test GET /api/students/?search=Alice returns matched student"""
        response = self.client.get(f"{self.list_url}?search=Alice")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['first_name'], "Alice")

    def test_filter_student_by_department(self):
        """Test GET /api/students/?department={id} filters properly"""
        response = self.client.get(f"{self.list_url}?department={self.dept_cs.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(data), 1)

    def test_dashboard_stats_endpoint(self):
        """Test GET /api/students/stats/ returns summary metrics"""
        stats_url = reverse('student-stats')
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_students'], 1)
        self.assertEqual(response.data['active_students'], 1)
