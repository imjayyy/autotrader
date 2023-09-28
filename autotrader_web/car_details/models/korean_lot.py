from django.db import models
from django.utils.functional import lazy
from car_details.models import Brand, Model, BanType, Color, Status, Fuel
from auction.models import Cities
from django.contrib import admin
from .korean_lot_image import KoreanLotImage
from django.utils.translation import gettext_lazy as _
from .auto_part import AutoPart
from .country import Country
from .feature import Feature


class KoreanLot(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Make = models.ForeignKey(Brand, on_delete=models.CASCADE)
    Model = models.ForeignKey(Model, on_delete=models.CASCADE)
    BodyStyle = models.ForeignKey(BanType, on_delete=models.CASCADE)
    Year = models.IntegerField()
    Engine = models.IntegerField()
    Odometer = models.IntegerField()
    Color = models.ForeignKey(Color, on_delete=models.CASCADE)
    Price = models.FloatField()
    Status = models.ForeignKey(Status, on_delete=models.CASCADE)
    NumberOfSeats = models.IntegerField()
    Vin = models.TextField()
    Commnet = models.TextField()
    FuelType = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    Drive = models.CharField(max_length=255, choices=[('FWD', _('FWD')), ('RWD', _('RWD')), ('AWD', _('AWD'))])
    Transmission = models.CharField(max_length=255, choices=[('Automatic', _('Automatic')), ('Manual', _('Manual'))])
    Location = models.ForeignKey(Country, on_delete=models.CASCADE)
    IsPublished = models.CharField(max_length=255, choices=[('YES', _('YES')), ('NO', _('NO'))])
    MainImage = models.ImageField()
    Images = models.ManyToManyField(KoreanLotImage)
    VideoLink = models.TextField()
    # TODO: Make this ManyToMany
    Documents = models.FileField()
    ChangedParts = models.ManyToManyField(AutoPart, related_name='manual_lots_parts_changed')
    PaintedParts = models.ManyToManyField(AutoPart, related_name='manual_lots_parts_painted')
    Features = models.ManyToManyField(Feature, related_name='manual_lots')

    class Meta:
        db_table = 'KoreanLot'
        verbose_name = 'Korean Lot'
        verbose_name_plural = 'Korean Lots'

    def __str__(self):
        return f"{self.Make.NameEn} {self.Model.NameEn} {self.Year}"


class KoreanLotAdmin(admin.ModelAdmin):
    list_display = ['Id', 'Make', "Model", "Year"]


admin.site.register(KoreanLot, KoreanLotAdmin)
