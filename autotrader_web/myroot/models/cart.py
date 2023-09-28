from django.db import models
from django.apps import apps

class Cart(models.Model):
    Id = models.BigAutoField(primary_key=True)
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    Price = models.DecimalField(max_digits=18,decimal_places=4)
    Total = models.DecimalField(max_digits=18,decimal_places=4)
    Quantity = models.IntegerField()
    
    @property
    def Product(self):
        model = apps.get_model("myroot.Product")
        return model.objects.filter(Id=self.ProductId)

    class Meta:
        db_table = 'Carts'