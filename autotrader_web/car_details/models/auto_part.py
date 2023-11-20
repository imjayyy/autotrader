from django.db import models
from django.contrib import admin


class AutoPart(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.TextField()

    class Meta:
        db_table = 'AutoPart'


class AutoPartAdmin(admin.ModelAdmin):
    list_display = ['Id', 'Name']


admin.site.register(AutoPart, AutoPartAdmin)
