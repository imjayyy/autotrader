from django.db import models
from django.apps import apps

class SaleProduct(models.Model):
    Id = models.BigAutoField(primary_key=True)
    SaleId = models.IntegerField()
    ProductId = models.IntegerField()
    Quantity = models.IntegerField()
    Total = models.DecimalField(max_digits=18,decimal_places=4)
    
    @property
    def Sale(self):
        model = apps.get_model("myroot.Sale")
        return model.objects.filter(Id=self.SaleId)

    @property
    def Product(self):
        model = apps.get_model("myroot.Product")
        return model.objects.filter(Id=self.ProductId)


    class Meta:
        db_table = 'SaleProduct'