from django.db import models
from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

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


class CitiesAdminResource(resources.ModelResource):
    class Meta:
         model = Cities
         import_id_fields = ['Id']

class CitiesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CitiesAdminResource

    list_display = [ 'Id',  'Name',  'Port',  'State',  'Country', ]
    search_fields = ['Name'] 
    list_filter = ('Country', 'State',)  # Add fields you want to filter on



admin.site.register(Cities,CitiesAdmin)

