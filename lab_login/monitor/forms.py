from django import forms
from .models import Student

YEAR_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4')]
BATCH_CHOICES_YEAR_1_2_4 = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
BATCH_CHOICES_YEAR_3 = [('A', 'A'), ('B', 'B'), ('C', 'C')]

class StudentForm(forms.ModelForm):
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True)
    batch = forms.ChoiceField(choices=[], required=True)

    class Meta:
        model = Student
        fields = ['roll_no', 'first_name', 'last_name', 'dob','year', 'batch']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})  # Date picker for easier DOB selection
        }

    def __init__(self, *args, **kwargs):
        year = kwargs.pop('year', None)
        super(StudentForm, self).__init__(*args, **kwargs)
        if year:
            if year == '3':
                self.fields['batch'].choices = BATCH_CHOICES_YEAR_3
            else:
                self.fields['batch'].choices = BATCH_CHOICES_YEAR_1_2_4
        else:
            self.fields['batch'].choices = []  # Default empty choices
