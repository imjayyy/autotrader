from django.db import models
from django.contrib import admin


class Order(models.Model):
    Id = models.BigAutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Content = models.TextField()
    AddDate = models.DateTimeField()

    class Meta:
        db_table = 'Orders'

class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'FullName',  'Phone',  'Email',  'Content',  'AddDate', ]
admin.site.register(Order,OrderAdmin)

