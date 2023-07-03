from django.forms import ModelForm
from .models import Task
from django import forms
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        widgets ={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo tarea'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'important':forms.CheckboxInput(attrs={'class':'form-check-input text-center'})
        }