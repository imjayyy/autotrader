from django.db import models
from django.apps import apps

class ProductImage(models.Model):
    Id = models.BigAutoField(primary_key=True)
    ProductId = models.IntegerField()
    ImagePath = models.TextField()
    
    @property
    def Product(self):
        model = apps.get_model("myroot.Product")
        return model.objects.filter(Id=self.ProductId)

    class Meta:
        db_table = 'ProductImages'