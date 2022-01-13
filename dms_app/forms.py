from dataclasses import fields
from pyexpat import model
from django import forms
from .models import DocumentModel


class DocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentModel
        fields = '__all__'


# https://www.agiliq.com/blog/2019/01/django-createview/
# https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
