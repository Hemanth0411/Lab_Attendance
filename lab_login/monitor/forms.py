from django import forms
from .models import Student
from django.forms import modelformset_factory

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'name', 'dob', 'batch', 'year']

StudentFormSet = modelformset_factory(Student, form=StudentForm, extra=5)
