from django.contrib import admin
from django.db import models
from django.apps import apps


class Color(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.CharField(max_length=100)
    NameEn = models.CharField(max_length=100)
    NameRu = models.CharField(max_length=100)

    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(ColorId=self.Id)

    class Meta:
        db_table = 'Colors'

    def __str__(self):
        return self.NameEn


class ColorAdmin(admin.ModelAdmin):
    list_display = ['Id', "NameAz", "NameEn", "NameRu", ]


admin.site.register(Color, ColorAdmin)
