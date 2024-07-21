from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    number = models.IntegerField(null=True)  # e.g., 1, 2, 3, ...
    department = models.ForeignKey(Department, related_name='semesters', on_delete=models.CASCADE)

    def __str__(self):
        return f"Semester {self.number} - {self.department.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, related_name='subjects', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.semester}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100, null=True)
    semester = models.IntegerField(null=True)  # Current semester
    batch = models.CharField(max_length=9)  # e.g., "2022-2026"
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

class Computer(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=100, default='available')

    def __str__(self):
        return self.unique_id

class Session(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    current_semester = models.IntegerField(null=True)  # Semester of the session
    subject = models.CharField(max_length=100, null=True)  # Subject related to the session

    def end_session(self):
        self.end_time = timezone.now()
        self.computer.status = 'available'
        self.computer.save()
        self.save()

    def __str__(self):
        return f"{self.student} on {self.computer} for {self.subject} at {self.start_time}"
