from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?[0-9]{10,15}$',
    message="Phone number must be between 10 and 15 digits, optionally prefixed with '+'."
)

class Department(models.Model):
    """
    Department Entity (SOP Section 7.3: Relational schema)
    Represents an academic department to which students belong.
    """
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    code = models.CharField(max_length=10, unique=True, null=False, blank=False)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    """
    Student Entity (SOP Section 6 & 7.3: Core management entity)
    Represents a student enrolled in the institution.
    """
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Graduated', 'Graduated'),
        ('Suspended', 'Suspended'),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        help_text="Unique student registration/roll number"
    )
    first_name = models.CharField(max_length=60, null=False, blank=False)
    last_name = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        help_text="Student official email address"
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        default=''
    )
    department = models.ForeignKey(
        Department,
        related_name='students',
        on_delete=models.PROTECT,
        help_text="Department student belongs to"
    )
    enrollment_date = models.DateField(null=False, blank=False)
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00, message="GPA cannot be negative."),
            MaxValueValidator(4.00, message="GPA cannot exceed 4.00.")
        ],
        help_text="Cumulative GPA on a 4.00 scale"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
