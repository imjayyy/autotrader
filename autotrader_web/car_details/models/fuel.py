from django.db import models
from django.apps import apps


class Fuel(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.CharField(max_length=100)
    NameEn = models.CharField(max_length=100)
    NameRu = models.CharField(max_length=100)
    CustomsCalculatorId = models.IntegerField(unique=True, null=True, default=None)

    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(FuelId=self.Id)

    class Meta:
        db_table = 'Fuel'
        verbose_name = 'Fuel'
        verbose_name_plural = 'Fuel'

    def __str__(self):
        return self.NameEn
