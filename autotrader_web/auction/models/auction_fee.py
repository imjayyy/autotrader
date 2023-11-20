from django.db import models
from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin


class AuctionFee(models.Model):
    Id = models.BigAutoField(primary_key=True)
    StartPrice = models.DecimalField(max_digits=18,decimal_places=4)
    EndPrice = models.DecimalField(max_digits=18,decimal_places=4)
    Fee = models.DecimalField(max_digits=18,decimal_places=4)
    AuctionCompanyId = models.BigIntegerField()
    
    @property
    def AuctionCompany(self):
        model = apps.get_model("auction.AuctionCompany")
        model.objects.filter(Id=self.AuctionCompanyId)

    class Meta:
        db_table = 'AuctionFees'


class AuctionFeeAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['Id', 'StartPrice', 'EndPrice', 'Fee']

admin.site.register(AuctionFee, AuctionFeeAdmin)
