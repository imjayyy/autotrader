from django.db import models
from django.contrib import admin


class KoreanLotImage(models.Model):

    Id = models.BigAutoField(primary_key=True)
    Image = models.ImageField()

    class Meta:
        db_table = 'KoreanLotImage'
        verbose_name = 'Korean Lot Image'
        verbose_name_plural = 'Korean Lot Images'


class KoreanLotImageAdmin(admin.ModelAdmin):
    list_display = ['Id', 'Image']


admin.site.register(KoreanLotImage, KoreanLotImageAdmin)
