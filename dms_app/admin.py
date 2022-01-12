from django.contrib import admin
from .models import Department, DocumentType, DocumentModel

admin.site.register(Department)
admin.site.register(DocumentType)
admin.site.register(DocumentModel)
