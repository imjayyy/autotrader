from django.db import models
from django.apps import apps

class Currency(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Symbol = models.CharField(max_length=10)
    
    @property
    def Car(self):
        model = apps.get_model("car_details.Car")
        return model.objects.filter(CurrencyId=self.Id)
    
    @property
    def Product(self):
        model = apps.get_model("myroot.Product")
        return model.objects.filter(CurrencyId=self.Id)


    class Meta:
        db_table = 'Currencies'