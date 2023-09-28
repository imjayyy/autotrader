from django.db import models


class BidInformation(models.Model):
    Id = models.BigAutoField(primary_key=True)
    LotId = models.BigIntegerField()
    BidStatus = models.TextField(null=True)
    SaleStatus = models.TextField(null=True)
    CurrentBid = models.TextField(null=True)
    Currency = models.TextField(null=True)

    class Meta:
        db_table = 'BidInformation'
