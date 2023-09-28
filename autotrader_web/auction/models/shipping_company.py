from django.db import models
from django.contrib import admin
from import_export.admin import ExportActionMixin


class ShippingCompany(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Chosen = models.IntegerField()
    AuctionShipping = models.ManyToManyField(
        'auction.AuctionCompany', 
        through='auction.AuctionShipping',
    )
    
    class Meta:
        db_table = 'ShippingCompanies'

    def __str__(self):
        return self.Name

class ShippingCompanyAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['Id',  'Name',  'Chosen',  ]
admin.site.register(ShippingCompany,ShippingCompanyAdmin)

    