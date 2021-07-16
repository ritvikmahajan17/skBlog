from django import forms
from .models import post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model= post
        fields = ['title','type','img','content']
