from django import forms
from .models import StudentCodeModel, Task


class StudentCodeModelForm(forms.ModelForm):

    class Meta:
        model = StudentCodeModel
        fields = '__all__'


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'
