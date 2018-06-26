from django.contrib import admin
from .models import Document, Person

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['description', 'document', 'uploaded_at']

admin.site.register(Person)