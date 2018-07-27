from django.contrib import admin
from .models import Document, Person, Department
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['description', 'document', 'ipaddr_and_date', 'uploaded_at', 'updated']

admin.site.register(Person)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department', 'available']
    list_editable = ['available',]

