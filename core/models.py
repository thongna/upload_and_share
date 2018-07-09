import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/', default='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ipaddr_and_date = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.description

    def get_ip_of_document(self):
        return self.ipaddr_and_date.rsplit('_', 1)[0]

    class Meta:
        ordering = ('-uploaded_at',)


class Person(User):
    documents = models.ManyToManyField(Document, blank=True)

def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)

@receiver(pre_delete, sender=Document)
def delete_file_pre_delete_document(sender, instance, *args, **kwargs):
    if instance.document:
        _delete_file(instance.document.path)

@receiver(pre_save, sender=Document)
def delete_file_pre_update_document(sender, instance, *args, **kwargs):
    print("hello")
    if instance.document:
        try:
            doc = Document.objects.get(ipaddr_and_date=str(instance.ipaddr_and_date))
            _delete_file(doc.document.path)
        except:
            pass
