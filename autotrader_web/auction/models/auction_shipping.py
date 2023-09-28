from django.db import models
from django.contrib import admin
from import_export.admin import ExportActionMixin


class AuctionShipping(models.Model):
    Id = models.BigAutoField(primary_key=True)
    AuctionCompanyId = models.ForeignKey(
        'auction.AuctionCompany', 
        on_delete=models.CASCADE,
        db_column='AuctionCompanyId'
    )
    ShippingCompanyId = models.ForeignKey(
        'auction.ShippingCompany', 
        on_delete=models.CASCADE,
        db_column='ShippingCompanyId'
    )

    class Meta:
        db_table = 'AuctionShippings'


class AuctionShippingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [ 'Id',  'AuctionCompanyId',  'ShippingCompanyId', ]
admin.site.register(AuctionShipping,AuctionShippingAdmin)

