from django.db import models
from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin


class ShippingAuctionFee(models.Model):
    Id = models.BigAutoField(primary_key=True)
    AuctionShippingId = models.BigIntegerField()
    UserTypesId = models.BigIntegerField()
    CitiesId = models.BigIntegerField()
    Fee = models.DecimalField(max_digits=18,decimal_places=4)

    @property
    def AuctionShipping(self):
        model = apps.get_model("auction.AuctionShipping")
        return model.objects.filter(Id=self.AuctionShippingId)
    
    @property
    def Cities(self):
        model = apps.get_model("auction.Cities")
        return model.objects.filter(Id=self.CitiesId)

    @property
    def UserTypes(self):
        model = apps.get_model("auction.UserTypes")
        return model.objects.filter(Id=self.UserTypesId)

    class Meta:
        db_table = 'ShippingAuctionFees'

