from django.db import models

class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    batch = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return self.name
