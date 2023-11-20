from django.db import models
from django.contrib import admin


class Blog(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Username = models.TextField()
    UserImage = models.TextField()
    TitleAz = models.TextField()
    TitleEn = models.TextField()
    TitleRu = models.TextField()
    ContentAz = models.TextField()
    ContentEn = models.TextField()
    ContentRu = models.TextField()
    AddDate = models.DateTimeField()
    Image = models.TextField()
    Count = models.IntegerField()
    ContentHtmlAz = models.TextField()
    ContentHtmlEn = models.TextField()
    ContentHtmlRu = models.TextField()

    @property
    def Day(self):
        return self.AddDate.strftime("%d")

    @property
    def Month(self):
        return self.AddDate.strftime("%b")

    class Meta:
        db_table = 'Blogs'

class BlogAdmin(admin.ModelAdmin):
    list_display = ['Id', 'Image', 'TitleEn', 'Username', 'AddDate', 'Count']

admin.site.register(Blog, BlogAdmin)
