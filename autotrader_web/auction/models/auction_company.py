from django.db import models
from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin


class AuctionCompany(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    GateFee = models.DecimalField(max_digits=18,decimal_places=4)
    AuctionShipping = models.ManyToManyField(
        'auction.ShippingCompany', 
        through='auction.AuctionShipping',
    )
    
    @property
    def AuctionFee(self):
        model = apps.get_model("auction.AuctionFee")
        return model.objects.filter(AuctionCompanyId=self.Id) 
    
    @property
    def AuctionOnlinelivebid(self):
        model = apps.get_model("auction.AuctionOnlinelivebid")
        return model.objects.filter(AuctionCompanyId=self.Id)

    class Meta:
        db_table = 'AuctionCompanies'

    def __str__(self):
        return self.Name

class AuctionCompanyAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['Id','Name','GateFee']

admin.site.register(AuctionCompany, AuctionCompanyAdmin)
