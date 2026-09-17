from rest_framework import serializers
from .models import Student, Department
import re

class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department entity.
    """
    student_count = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'student_count', 'created_at']
        read_only_fields = ['id', 'student_count', 'created_at']


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student entity implementing strict server-side validation (SOP Section 9).
    Supports full CRUD operations with rich representation.
    """
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'department',
            'department_name',
            'department_code',
            'enrollment_date',
            'gpa',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'full_name', 'department_name', 'department_code', 'created_at', 'updated_at']

    def validate_student_id(self, value):
        """Validate student_id format and uniqueness"""
        val = value.strip().upper()
        if len(val) < 3:
            raise serializers.ValidationError("Student ID must be at least 3 characters long.")
        
        # Check uniqueness on create and update
        qs = Student.objects.filter(student_id__iexact=val)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(f"A student with ID '{val}' already exists.")
        return val

    def validate_first_name(self, value):
        val = value.strip()
        if not val:
            raise serializers.ValidationError("First name cannot be blank or whitespace.")
        if len(val) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        return val

    def validate_last_name(self, value):
        val = value.strip()
        if not val:
            raise serializers.ValidationError("Last name cannot be blank or whitespace.")
        if len(val) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long.")
        return val

    def validate_email(self, value):
        val = value.strip().lower()
        qs = Student.objects.filter(email__iexact=val)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(f"Email '{val}' is already registered.")
        return val

    def validate_gpa(self, value):
        try:
            val = float(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("GPA must be a valid decimal number.")
        if val < 0.0 or val > 4.0:
            raise serializers.ValidationError("GPA must be between 0.00 and 4.00.")
        return round(val, 2)

    def validate_phone(self, value):
        if value:
            val = value.strip()
            if not re.match(r'^\+?[0-9]{10,15}$', val):
                raise serializers.ValidationError("Phone number must contain 10-15 digits, optionally prefixed with '+'.")
            return val
        return ''
