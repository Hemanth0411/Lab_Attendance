from django import forms
from .models import Student, Attendance, Subject

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'first_name', 'last_name', 'dob', 'year', 'batch']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        year = kwargs.pop('year', None)
        super(StudentForm, self).__init__(*args, **kwargs)
        
        self.fields['year'].widget = forms.Select(choices=[(i, i) for i in range(1, 5)])
        
        if year:
            if year == 3:
                batch_choices = [('A', 'A'), ('B', 'B'), ('C', 'C')]
            else:
                batch_choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
            self.fields['batch'].widget = forms.Select(choices=batch_choices)
        else:
            self.fields['batch'].widget = forms.Select(choices=[])
        
        self.fields['batch'].widget.attrs['disabled'] = 'disabled' if not year else ''

    def clean_roll_no(self):
        roll_no = self.cleaned_data['roll_no']
        if len(roll_no) != 12 or not roll_no.isdigit() or roll_no.startswith('0'):
            raise forms.ValidationError("Roll no must be a 12 digit number and cannot start with 0.")
        return roll_no

class YearBatchForm(forms.Form):
    year = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])
    batch = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

class AttendanceForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    students = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        students_queryset = kwargs.pop('students', None)
        super(AttendanceForm, self).__init__(*args, **kwargs)
        if students_queryset is not None:
            self.fields['students'].choices = [(student.roll_no, f"{student.first_name} {student.last_name}") for student in students_queryset]