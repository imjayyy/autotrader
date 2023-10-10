from django.db import models
from django.apps import apps
from django.contrib import admin


class LotImages(models.Model):
    Id = models.BigAutoField(primary_key=True)
    LotId = models.BigIntegerField()
    ImageFull = models.TextField()

    class Meta:
        db_table = 'LotImages'

class LotImagesAdmin(admin.ModelAdmin):
    list_display = [ 'Id' , 'LotId', 'ImageFull']

admin.site.register(LotImages, LotImagesAdmin)