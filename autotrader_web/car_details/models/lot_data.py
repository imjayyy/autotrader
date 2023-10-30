from datetime import datetime
from .bid_information import *
from .sale_information import *
from .lot_images import *
from django.contrib import admin


class LotData(models.Model):
    id = models.BigAutoField(primary_key=True)
    lotId = models.BigIntegerField(unique=True,default=0)
    year = models.BigIntegerField(null=True)
    make = models.CharField(max_length=255, null=True)
    modelGroup = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    bodyStyle = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    primaryDamage = models.CharField(max_length=255, null=True)
    vin = models.CharField(max_length=255, null=True)
    odometer = models.IntegerField(null=True)
    engineSize = models.CharField(max_length=255, null=True)
    locationName = models.CharField(max_length=255, null=True)
    vehicleType = models.CharField(max_length=255, null=True)
    imageFull = models.CharField(max_length=255, null=True)
    imageThumb = models.CharField(max_length=255, null=True)
    vinHash = models.CharField(max_length=255, null=True)
    saledate = models.DateTimeField(blank=True, null=True) 
    searchTerm = models.CharField(max_length=255, null=True)
    dateCreated = models.DateTimeField(default=datetime.now, blank=True)
    transmission = models.CharField(max_length=255, null=True)
    drive = models.CharField(max_length=255, null=True)
    cylinders = models.TextField(null=True)
    fuel = models.CharField(max_length=255, null=True)
    keys = models.CharField(max_length=255, null=True)
    secondaryDamage = models.CharField(max_length=255, null=True)
    odometerType = models.CharField(max_length=255, null=True)
    auctionCompanyId = models.IntegerField(null=True)
    buyItNow = models.IntegerField(null=True)

    @property
    def BidInformation(self):
        bid_info = BidInformation.objects.filter(LotId=self.lotId)
        if len(bid_info) <=0:
            return BidInformation(LotId=self)
        return bid_info[0]
    
    @property
    def SaleInformation(self):
        sale_info = SaleInformation.objects.filter(LotId=self)
        if len(sale_info) <=0:
            return SaleInformation(LotId=self)
        return sale_info[0]

    @property
    def LotImages(self):
        return LotImages.objects.filter(LotId=self)

    class Meta:
        db_table = 'LotData'


class LotDataAdmin(admin.ModelAdmin):
    list_display = [ 'id' , 'year', 'make', 'model', 'bodyStyle', 'locationName']

admin.site.register(LotData, LotDataAdmin)
