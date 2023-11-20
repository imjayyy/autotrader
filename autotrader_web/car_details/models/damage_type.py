from django.db import models


class DamageType(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.TextField()
    Priority = models.IntegerField()

    class Meta:
        db_table = 'DamageType'
