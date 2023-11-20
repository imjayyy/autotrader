from django.db import models
from django.apps import apps


class SpeedBox(models.Model):
    Id = models.BigAutoField(primary_key=True)
    NameAz = models.CharField(max_length=100)
    NameEn = models.CharField(max_length=100)
    NameRu = models.CharField(max_length=100)
    
    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(SpeedBoxId=self.Id)

    class Meta:
        db_table = 'SpeedBoxes'
