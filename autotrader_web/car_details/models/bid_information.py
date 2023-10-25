from django.db import models
# from .lot_data import LotData

class BidInformation(models.Model):
    Id = models.BigAutoField(primary_key=True)
    LotId = models.ForeignKey('LotData', on_delete=models.CASCADE)
    BidStatus = models.TextField(null=True)
    SaleStatus = models.TextField(null=True)
    CurrentBid = models.TextField(null=True)
    Currency = models.TextField(null=True)

    class Meta:
        db_table = 'BidInformation'
