from django.db import models
from django.apps import apps


class CarImage(models.Model):
    Id = models.BigAutoField(primary_key=True)
    CarId = models.IntegerField()
    MainImage = models.TextField()
    
    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(Id=self.CarId)

    class Meta:
        db_table = 'CarImage'
