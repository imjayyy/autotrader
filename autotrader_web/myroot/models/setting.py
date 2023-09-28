from django.db import models
from django.contrib import admin


class Setting(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Email = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    Address = models.TextField(max_length=300)
    CustomerCount = models.IntegerField()
    CarCount = models.IntegerField()
    AuctionCount = models.IntegerField()
    NameAz = models.TextField()
    NameEn = models.TextField()
    NameRu = models.TextField()

    class Meta:
        db_table = 'Settings'



class SettingAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'Email',  'Phone',  'Address',  'CustomerCount',  'CarCount',  'AuctionCount',  'NameAz',  'NameEn',  'NameRu', ]

admin.site.register(Setting,SettingAdmin)

    