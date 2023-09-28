from django.db import models
from django.contrib import admin


class Partner(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    LogoPath = models.TextField()

    class Meta:
        db_table = 'Partners'

class PartnerAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'Name',  'LogoPath', ]

admin.site.register(Partner,PartnerAdmin)

    