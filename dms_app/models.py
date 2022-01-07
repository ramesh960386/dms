import os
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


DOC_TYPE = (
    ('1', 'agreement'),
    ('2', 'Presentation'),
    ('3', 'SOP'),
    ('4', 'Training Manual'),
)


class DocumentModel(models.Model):
    doc_name = models.CharField(max_length=200)
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE)
    # doc_owner = models.ForeignKey(User, on_delete=models.SET_NULL)
    doc_owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_doc_owner')
    doc_dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    document = models.FileField(upload_to='uploads/')
    comment = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, null=True, editable=False, on_delete=models.SET_NULL,
                                   related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, null=True, editable=False, on_delete=models.SET_NULL,
                                    related_name='%(class)s_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # status = models.CharField(max_length=20)

    # def get_download_info(self):
    #     _file = self.document
    #     download_name = self.name + ".pdf"
    #     content_type = "application/pdf"
    #     return content_type, download_name, _file

    def filename(self):
        # return self.file.name.split('/')[-1:][0]
        return os.path.basename(self.document.name)

    def __str__(self):
        return self.doc_name
