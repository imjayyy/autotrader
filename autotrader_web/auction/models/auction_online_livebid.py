from django.db import models
from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin


class AuctionOnlinelivebid(models.Model):
    Id = models.BigAutoField(primary_key=True)
    AuctionCompanyId = models.BigIntegerField()
    StartPrice = models.DecimalField(max_digits=18,decimal_places=4)
    EndPrice = models.DecimalField(max_digits=18,decimal_places=4)
    Fee = models.DecimalField(max_digits=18,decimal_places=4)
    
    @property
    def AuctionCompany(self):
        model = apps.get_model("auction.AuctionCompany")
        return model.objects.filter(Id=self.AuctionCompanyId)

    class Meta:
        db_table = 'AuctionOnlinelivebids'


class AuctionOnlinelivebidAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [ 'Id',  'AuctionCompanyId',  'StartPrice',  'EndPrice',  'Fee', ]
admin.site.register(AuctionOnlinelivebid,AuctionOnlinelivebidAdmin)

