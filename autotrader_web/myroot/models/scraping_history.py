from django.db import models
from django.contrib import admin


class ScrapingHistory(models.Model):
    Id = models.BigAutoField(primary_key=True)
    StartDate = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now_add=True)
    TotalLotsScraped = models.BigIntegerField(default=0)
    TotalCrawlPages = models.BigIntegerField(default=0)
    TotalLotsStartedScraping = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'ScrapingHistory'


class ScrapingHistoryAdmin(admin.ModelAdmin):
    list_display = ['Id',  'StartDate',  'LastUpdated',  'TotalLotsScraped']


admin.site.register(ScrapingHistory, ScrapingHistoryAdmin)

