from django.db import models
from django.contrib import admin


class Feature(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.TextField()

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'Feature'
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['Id', 'Name']


admin.site.register(Feature, FeatureAdmin)
