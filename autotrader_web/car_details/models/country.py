from django.db import models
from django.contrib import admin


class Country(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.TextField()

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'Country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class CountryAdmin(admin.ModelAdmin):
    list_display = ['Id', 'Name']


admin.site.register(Country, CountryAdmin)
