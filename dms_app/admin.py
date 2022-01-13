from django.contrib import admin
from .models import Department, DocumentType, DocumentModel



class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'doc_name', 'doc_type', 'doc_owner', 'doc_dept', 'description',)
    list_display_links = ('doc_name',)


admin.site.register(Department)
admin.site.register(DocumentType)
admin.site.register(DocumentModel, DocumentAdmin)
