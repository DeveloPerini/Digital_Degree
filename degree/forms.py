from django import forms
from . models import Student

class StudentForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    birth_date = forms.DateField()
    graduation_date = forms.DateField()
    grade = forms.FloatField()
    degree = forms.ChoiceField(choices=Student.DEGREE_CHOICES)
    