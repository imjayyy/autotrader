from django.db import models
from django.contrib import admin


class Gallery(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Type = models.IntegerField()
    ImagePath = models.TextField()
    VideoLink = models.TextField()

    @property
    def File(self):
        if self.ImagePath != "":
            return self.ImagePath
        else:
            return self.VideoLink

    class Meta:
        db_table = 'Galleries'

class GalleryAdmin(admin.ModelAdmin):
    list_display = ['Id', 'File']

admin.site.register(Gallery,GalleryAdmin)
