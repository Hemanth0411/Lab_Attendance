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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
