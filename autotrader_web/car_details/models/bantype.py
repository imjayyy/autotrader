from django.db import models
from django.apps import apps
from django.contrib import admin


class BanType(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.CharField(max_length=100)
    NameEn = models.CharField(max_length=100)
    NameRu = models.CharField(max_length=100)
    
    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(BanTypeId=self.Id)

    class Meta:
        db_table = 'BanTypes'

    def __str__(self):
        return self.NameEn

class BanTypeAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'NameAz','NameRu','NameEn']

admin.site.register(BanType,BanTypeAdmin)

    