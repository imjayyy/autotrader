from django.db import models
from django.apps import apps


class Status(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.CharField(max_length=100)
    NameEn = models.CharField(max_length=100)
    NameRu = models.CharField(max_length=100)
    
    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(StatusId=self.Id)

    class Meta:
        db_table = 'Status'

    def __str__(self):
        return self.NameEn