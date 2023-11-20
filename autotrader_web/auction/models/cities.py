from django.db import models
from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin


class Cities(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Port = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    Country = models.CharField(max_length=255, null=True)
    
    @property
    def ShippingAuctionFee(self):
        model = apps.get_model("auction.ShippingAuctionFee")
        return model.objects.filter(CitiesId=self.Id)

    class Meta:
        db_table = 'Cities'

    def __str__(self):
        return self.Name


class CitiesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [ 'Id',  'Name',  'Port',  'State',  'Country', ]
admin.site.register(Cities,CitiesAdmin)

