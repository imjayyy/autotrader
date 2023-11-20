from django.db import models
from django.apps import apps
from django.contrib import admin


class Product(models.Model):
    Id = models.BigAutoField(primary_key=True)
    BrandId = models.IntegerField()
    ModelId = models.IntegerField()
    CurrencyId = models.IntegerField()
    Code = models.TextField()
    NameAz = models.TextField()
    NameEn = models.TextField()
    NameRu = models.TextField()
    Price = models.DecimalField(max_digits=18,decimal_places=4)
    PriceWithSale = models.DecimalField(max_digits=18,decimal_places=4)
    StockCount = models.IntegerField()
    MainImage = models.TextField()
    AboutAz = models.TextField()
    AboutEn = models.TextField()
    AboutRu = models.TextField()
    AddDate = models.DateTimeField()
    
    @property
    def Brand(self):
        model = apps.get_model("car_details.Brand")
        return model.objects.filter(Id=self.BrandId)
    
    @property
    def Model(self):
        model = apps.get_model("car_details.Model")
        return model.objects.filter(Id=self.ModelId)
    
    @property
    def Currency(self):
        model = apps.get_model("myroot.Currency")
        return model.objects.filter(Id=self.CurrencyId)
    
    @property
    def ProductImage(self):
        model = apps.get_model("myroot.ProductImage")
        return model.objects.filter(ProductId=self.Id)
    
    @property
    def SaleProduct(self):
        model = apps.get_model("myroot.SaleProduct")
        return model.objects.filter(ProductId=self.Id)

    class Meta:
        db_table = 'Products'



class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'BrandId',  'ModelId',  'CurrencyId',  'Code',  'NameAz',  'NameEn',  'NameRu',  'Price',  'PriceWithSale',  'StockCount',  'MainImage',  'AboutAz',  'AboutEn',  'AboutRu',  'AddDate', ]

admin.site.register(Product,ProductAdmin)

    