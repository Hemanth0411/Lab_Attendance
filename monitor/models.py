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
        primary_key=True,
        unique=True,
        validators=[validate_roll_no])
    name = models.CharField(default='N/A', max_length=100)
    year = models.CharField(default='2024-28', max_length=10)
    batch = models.CharField(default='A', max_length=5)
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
    sd_attendance = models.IntegerField(default=0)
    dv_attendance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
    
    def reduce_attendance(self, subject_name):
        # Map subject names to corresponding attendance fields
        field_map = {
            'C Language': 'c_language_attendance',
            'IT': 'it_attendance',
            'DS': 'ds_attendance',
            'OS': 'os_attendance',
            'Java': 'java_attendance',
            'DBMS': 'dbms_attendance',
            'Python': 'python_attendance',
            'WT': 'wt_attendance',
            'R': 'r_attendance',
            'CD': 'cd_attendance',
            'SD': 'sd_attendance',
            'DV': 'dv_attendance'
        }

        field_name = field_map.get(subject_name)
        if field_name:
            current_value = getattr(self, field_name, 0)
            if current_value > 0:
                setattr(self, field_name, current_value - 1)
                self.save()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class Session(models.Model):
    IN_TIME_CHOICES = [
        ('09:30', '9:30'),
        ('10:30', '10:30'),
        ('12:00', '12:00'),
        ('14:00', '2:00'),
        ('15:00', '3:00')
    ]
    
    OUT_TIME_CHOICES = [
        ('10:30', '10:30'),
        ('11:30', '11:30'),
        ('13:00', '1:00'),
        ('15:00', '3:00'),
        ('16:00', '4:00')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    in_time = models.CharField(max_length=5, choices=IN_TIME_CHOICES)
    out_time = models.CharField(max_length=5, choices=OUT_TIME_CHOICES)
    lab = models.CharField(max_length=10, choices=[
        ('Lab-1', 'Lab-1'),
        ('Lab-2', 'Lab-2'),
        ('Lab-3', 'Lab-3'),
        ('Lab-4', 'Lab-4')
    ], blank=True, null=True)

    def __str__(self):
        return f"{self.student.roll_no} - {self.subject} - {self.date}"
    
    
