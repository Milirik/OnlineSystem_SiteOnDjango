from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import StudentCodeModel, Task, Test


class StudentCodeModelForm(forms.ModelForm):
    def clean(self):
        super().clean()
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


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ()


TestFormSet = inlineformset_factory(Task, Test, TestForm, extra=3)
