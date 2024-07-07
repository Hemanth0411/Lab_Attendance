from django.db import models

# Create your models here.
class Student(models.Model):
    GENDER_CHOICES=[
        ("M", "Male"),
        ("F", "Female")
        ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    email_id = models.EmailField(max_length=254, unique = True)
    phone_number = models.CharField(max_length=100, blank=True)
    student_gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    student_address = models.TextField(max_length=1000)
    student_dept = models.ManyToManyField('Departments')
    date_of_birth = models.DateField()
    
class Departments(models.Model):
    department_name = models.CharField(max_length=20)