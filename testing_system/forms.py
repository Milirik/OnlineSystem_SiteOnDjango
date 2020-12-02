from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import StudentCodeModel, Task, Test, Course


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
        widgets = {
            'teacher': forms.HiddenInput,
            'course': forms.HiddenInput
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('students',)
        widgets = {'teacher': forms.HiddenInput}


class TestForm(forms.ModelForm):
    input = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Входные данные'
    )

    output = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Выходные данные'
    )

    class Meta:
        model = Test
        exclude = ()


TestFormSet = inlineformset_factory(Task, Test, TestForm, extra=3)