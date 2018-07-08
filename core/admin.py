from django.contrib import admin
from .models import Document, Person

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['description', 'document', 'ipaddr_and_date', 'uploaded_at', 'updated']

admin.site.register(Person)