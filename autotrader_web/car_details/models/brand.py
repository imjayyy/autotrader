from django.db import models
from django.apps import apps
from django.contrib import admin


class Brand(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.CharField(max_length=100)
    NameEn = models.CharField(max_length=100)
    NameRu = models.CharField(max_length=100)
    
    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(BrandId=self.Id)
    
    @property
    def Model(self):
        model = apps.get_model("car_details.Model")
        return model.objects.filter(BrandId=self.Id)
    
    @property
    def Product(self):
        model = apps.get_model("myroot.Product")
        return model.objects.filter(BrandId=self.Id)

    class Meta:
        db_table = 'Brands'

    def __str__(self):
        return self.NameEn

class BrandAdmin(admin.ModelAdmin):
    list_display = ['Id', 'NameAz', 'NameEn', 'NameRu']

admin.site.register(Brand, BrandAdmin)
