from django import forms
from app1.models import Category

class category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields='__all__'


