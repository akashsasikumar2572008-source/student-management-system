from django.contrib import admin
from .models import Department, Student

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'department', 'gpa', 'status', 'enrollment_date')
    list_filter = ('status', 'department', 'enrollment_date')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
