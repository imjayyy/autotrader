from django.db import models
from django.apps import apps
from django.contrib import admin


class Model(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.CharField(max_length=100)
    NameEn = models.CharField(max_length=100)
    NameRu = models.CharField(max_length=100)
    BrandId = models.IntegerField()
    
    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(ModelId=self.Id)

    @property
    def Brand(self):
        model = apps.get_model("car_details.Brand")
        return model.objects.get(Id=self.BrandId)

    class Meta:
        db_table = 'Models'

    def __str__(self):
        return self.NameEn

class ModelAdmin(admin.ModelAdmin):
    list_display = ['Id','Brand', 'NameEn', 'NameRu', 'NameAz']

admin.site.register(Model, ModelAdmin)
