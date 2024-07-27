from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_roll_no(value):
    """ Custom validator for roll_no """
    if len(value) != 12:
        raise ValidationError('Roll number must be 12 digits long.')
    if value[0] == '0':
        raise ValidationError('Roll number cannot start with 0.')
    if not re.match(r'^\d+$', value):
        raise ValidationError('Roll number must contain only digits.')

class Subject(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Student(models.Model):
    roll_no = models.CharField(
        max_length=12,
        unique=True,
        primary_key=True,
        validators=[validate_roll_no]
    )
    first_name = models.CharField(max_length=50, default='N/A')  # Default value provided
    last_name = models.CharField(max_length=50, default='N/A')   # Default value provided
    dob = models.DateField()
    batch = models.CharField(max_length=20, default='N/A')       # Default value provided
    year = models.IntegerField(default=2024)                      # Default value provided
    c_language_attendance = models.IntegerField(default=0)
    it_attendance = models.IntegerField(default=0)
    ds_attendance = models.IntegerField(default=0)
    os_attendance = models.IntegerField(default=0)
    java_attendance = models.IntegerField(default=0)
    dbms_attendance = models.IntegerField(default=0)
    python_attendance = models.IntegerField(default=0)
    wt_attendance = models.IntegerField(default=0)
    r_attendance = models.IntegerField(default=0)
    cd_attendance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
