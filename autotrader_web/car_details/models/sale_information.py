from django.db import models
# from .lot_data import LotData

class SaleInformation(models.Model):
    Id = models.BigAutoField(primary_key=True)
    LotId = models.ForeignKey('LotData', on_delete=models.CASCADE)
    Lane = models.TextField(null=True)
    Item = models.TextField(null=True)
    Grid = models.TextField(null=True)
    Row = models.TextField(null=True)
    LastUpdated = models.DateTimeField()

    class Meta:
        db_table = 'SaleInformation'
