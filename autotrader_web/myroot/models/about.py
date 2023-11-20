from django.db import models
from django.contrib import admin

class About(models.Model):
    Id = models.BigAutoField(primary_key=True)
    TitleAz = models.TextField()
    TitleEn = models.TextField()
    TitleRu = models.TextField()
    ContentAz = models.TextField()
    ContentEn = models.TextField()
    ContentRu = models.TextField()
    Image = models.TextField()
    FooterAz = models.TextField()
    FooterEn = models.TextField()
    FooterRu = models.TextField()

    class Meta:
        db_table = 'About'

class AboutAdmin(admin.ModelAdmin):
    list_display = ['Id', 'Image', 'TitleEn', 'ContentEn','FooterEn']

admin.site.register(About, AboutAdmin)
