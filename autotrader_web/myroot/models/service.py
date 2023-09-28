from django.db import models
from django.contrib import admin


class Service(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.TextField()
    NameEn = models.TextField()
    NameRu = models.TextField()
    AboutAz = models.TextField()
    AboutEn = models.TextField()
    AboutRu = models.TextField()
    ImagePath = models.TextField()
    MainImage = models.TextField()

    class Meta:
        db_table = 'Services'
        


class ServiceAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'NameAz',  'NameEn',  'NameRu',  'AboutAz',  'AboutEn',  'AboutRu',  'ImagePath',  'MainImage', ]

admin.site.register(Service,ServiceAdmin)

    