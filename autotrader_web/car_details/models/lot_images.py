from django.db import models
from django.apps import apps


class LotImages(models.Model):
    Id = models.BigAutoField(primary_key=True)
    LotId = models.BigIntegerField()
    ImageFull = models.TextField()

    class Meta:
        db_table = 'LotImages'
