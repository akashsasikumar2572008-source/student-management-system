import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(help_text='Unique student registration/roll number', max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('email', models.EmailField(help_text='Student official email address', max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, default='', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be between 10 and 15 digits, optionally prefixed with '+'.", regex='^\\+?[0-9]{10,15}$')])),
                ('enrollment_date', models.DateField()),
                ('gpa', models.DecimalField(decimal_places=2, help_text='Cumulative GPA on a 4.00 scale', max_digits=3, validators=[django.core.validators.MinValueValidator(0.0, message='GPA cannot be negative.'), django.core.validators.MaxValueValidator(4.0, message='GPA cannot exceed 4.00.')])),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Graduated', 'Graduated'), ('Suspended', 'Suspended')], default='Active', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(help_text='Department student belongs to', on_delete=django.db.models.deletion.PROTECT, related_name='students', to='students.department')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'ordering': ['-created_at'],
            },
        ),
    ]
