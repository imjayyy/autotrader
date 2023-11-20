from django.db import models
from django.apps import apps
from django.contrib import admin


class Sale(models.Model):
    Id = models.BigAutoField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Address = models.TextField(max_length=300)
    City = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    Postcode = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    Total = models.DecimalField(max_digits=18,decimal_places=4)
    Quantity = models.IntegerField()
    Date = models.DateTimeField()
    PaymentStatus = models.IntegerField()
    
    @property
    def SaleProduct(self):
        model = apps.get_model("myroot.SaleProduct")
        return model.objects.filter(SaleId=self.Id)

    

    class Meta:
        db_table = 'Sales'



class SaleAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'FirstName',  'LastName',  'Address',  'City',  'Country',  'Postcode',  'Phone',  'Total',  'Quantity',  'Date',  'PaymentStatus', ]

admin.site.register(Sale,SaleAdmin)

    