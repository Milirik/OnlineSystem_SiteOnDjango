from django import forms
from django.core.exceptions import ValidationError

from .models import StudentCodeModel, Task


class StudentCodeModelForm(forms.ModelForm):
    def clean(self):
        super().clean()
        print(self.cleaned_data['file'])
        if self.cleaned_data['code_text'] == '' and not self.cleaned_data['file']:
            print('err')
            raise ValidationError('Оба поля пусты')

    class Meta:
        model = StudentCodeModel
        fields = '__all__'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
