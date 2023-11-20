from django.db import models
from django.contrib import admin


class Message(models.Model):
    Id = models.BigAutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Subject  = models.TextField()
    Content = models.TextField()
    AddDate = models.DateTimeField()

    class Meta:
        db_table = 'Messages'

class MessageAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'FullName',  'Phone',  'Email',  'Subject',  'Content',  'AddDate', ]
admin.site.register(Message,MessageAdmin)

