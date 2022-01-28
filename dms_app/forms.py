from django import forms
from .models import DocumentModel


class DocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentModel
        # fields = '__all__'
        exclude = ('doc_owner',)

    def __init__(self, *args, **kwargs):
        # self.created_by = args.remove('user', None)
        # self.created_by = fields.pop('user', None)
        # self.fields['used_his'].queryset = User.objects.filter(pk = user.id)
        super(DocumentForm, self).__init__(*args, **kwargs)


# https://www.agiliq.com/blog/2019/01/django-createview/
# https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
