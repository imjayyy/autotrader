from django.db import models
from django.apps import apps
from django.contrib import admin
# from .lot_data import LotData

class LotImages(models.Model):
    Id = models.BigAutoField(primary_key=True)
    LotId = models.ForeignKey('LotData', on_delete=models.CASCADE)
    ImageFull = models.TextField()

    class Meta:
        db_table = 'LotImages'

class LotImagesAdmin(admin.ModelAdmin):
    list_display = [ 'Id' , 'LotId', 'ImageFull']

admin.site.register(LotImages, LotImagesAdmin)