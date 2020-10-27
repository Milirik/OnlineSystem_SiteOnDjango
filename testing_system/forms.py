from django import forms
from .models import StudentCodeModel


class StudentCodeModelForm(forms.ModelForm):

    class Meta:
        model = StudentCodeModel
        fields = '__all__'
