from django.db import models
from django.contrib import admin


class SliderImage(models.Model):
    Id = models.BigAutoField(primary_key=True)
    ImagePath = models.TextField()
    TitleAz = models.TextField(max_length=500)
    TitleEn = models.TextField(max_length=500)
    TitleRu = models.TextField(max_length=500)

    class Meta:
        db_table = 'SliderImages'



class SliderImageAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'ImagePath',  'TitleAz',  'TitleEn',  'TitleRu', ]

admin.site.register(SliderImage,SliderImageAdmin)

    