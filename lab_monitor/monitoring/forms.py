from django import forms
from .models import Subject

class SubjectSelectionForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label=None)
