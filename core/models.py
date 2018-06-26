from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ipaddr_and_date = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.description

class Person(User):
    documents = models.ManyToManyField(Document, blank=True)
