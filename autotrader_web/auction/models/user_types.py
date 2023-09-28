from django.db import models
from django.apps import apps
from django.contrib import admin
from import_export.admin import ExportActionMixin


class UserTypes(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Marja = models.DecimalField(max_digits=18,decimal_places=4)
    ServiceFee = models.DecimalField(max_digits=18,decimal_places=4)
    ToBakuFee = models.DecimalField(max_digits=18,decimal_places=4)
    
    @property
    def Users(self):
        model = apps.get_model("auction.Users")
        return model.objects.filter(UserTypesId=self.Id)

    @property
    def ShippingAuctionFee(self):
        model = apps.get_model("auction.ShippingAuctionFee")
        return model.objects.filter(UserTypesId=self.Id)

    class Meta:
        db_table = 'UserTypes'



class UserTypesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [ 'Id',  'Name',  'Marja',  'ServiceFee',  'ToBakuFee', ]
admin.site.register(UserTypes,UserTypesAdmin)

    