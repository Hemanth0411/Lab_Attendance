from django import forms
from .models import Student, Attendance, Subject

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'name', 'year', 'batch']

    def __init__(self, *args, **kwargs):
        year = kwargs.pop('year', None)
        super(StudentForm, self).__init__(*args, **kwargs)
        
        # Set default choices for year and batch
        self.fields['year'].widget = forms.Select(choices=[('2021-25', '2021-25'), ('2022-26', '2022-26'), ('2023-27', '2023-27'), ('2024-28', '2024-28')])
        
        if year:
            if year == '2021-25':
                batch_choices = [('A', 'A'), ('B', 'B'), ('C', 'C')]
            elif year == '2024-28':
                batch_choices = [('A', 'A'), ('B', 'B')]
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
    year = forms.ChoiceField(choices=[
        ('2021-25', '2021-25'),
        ('2022-26', '2022-26'),
        ('2023-27', '2023-27'),
        ('2024-28', '2024-28')
    ])
    batch = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])


class AttendanceForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    students = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    in_time = forms.ChoiceField(choices=[
        ('09:30', '9:30'),
        ('10:30', '10:30'),
        ('12:00', '12:00'),
        ('14:00', '2:00'),
        ('15:00', '3:00')
    ])
    out_time = forms.ChoiceField(choices=[
        ('10:30', '10:30'),
        ('11:30', '11:30'),
        ('13:00', '1:00'),
        ('15:00', '3:00'),
        ('16:00', '4:00')
    ])
    lab = forms.ChoiceField(choices=[
        ('Lab-1', 'Lab-1'),
        ('Lab-2', 'Lab-2'),
        ('Lab-3', 'Lab-3'),
        ('Lab-4', 'Lab-4')
    ], required=False)

    def __init__(self, *args, **kwargs):
        students_queryset = kwargs.pop('students', None)
        super(AttendanceForm, self).__init__(*args, **kwargs)
        if students_queryset is not None:
            self.fields['students'].choices = [(student.roll_no, f"{student.name}") for student in students_queryset]
            
            
class SessionFilterForm(forms.Form):
    ALL_CHOICES = [('', 'All')]  # Choice for selecting 'All'
    year = forms.ChoiceField(choices=ALL_CHOICES + [(y, y) for y in ['2021-25', '2022-26', '2023-27', '2024-28']], required=False)
    batch = forms.ChoiceField(choices=ALL_CHOICES + [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], required = False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)
    roll_no = forms.CharField(required=False)
    
class ImportStudentsForm(forms.Form):
    excel_file = forms.FileField()
    
class PartFilter(forms.Form):
    ALL_CHOICES = [('', 'All')]
    year = forms.ChoiceField(choices=ALL_CHOICES + [(y, y) for y in ['2021-25', '2022-26', '2023-27', '2024-28']], required=False)
    batch = forms.ChoiceField(choices=ALL_CHOICES + [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], required = False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)
    roll_no = forms.CharField(required=False)
    
class UploadSessionsForm(forms.Form):
    excel_file = forms.FileField()
    
class ReduceAttendanceForm(forms.Form):
    roll_no = forms.CharField(required=False)
    subject = forms.ChoiceField(choices=[
        ('C Language', 'C Language'),
        ('IT', 'IT'),
        ('DS', 'DS'),
        ('OS', 'OS'),
        ('Java', 'Java'),
        ('DBMS', 'DBMS'),
        ('Python', 'Python'),
        ('WT', 'WT'),
        ('R', 'R'),
        ('CD', 'CD'),
        ('SD', 'SD'),
        ('DV', 'DV')
    ], label="Select Subject")