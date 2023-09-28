from django.db import models
from .status import Status
from django.apps import apps
from django.contrib import admin
from django import forms


class Car(models.Model):
    Id = models.BigAutoField(primary_key=True)
    StatusId = models.IntegerField()
    BrandId = models.IntegerField()
    ModelId = models.IntegerField()
    FuelId = models.IntegerField()
    ColorId = models.IntegerField()
    CurrencyId = models.IntegerField()
    BanTypeId = models.IntegerField()
    Distance = models.IntegerField()
    Year = models.IntegerField()
    SpeedBoxId = models.IntegerField()
    EngineCapacity = models.DecimalField(max_digits=18, decimal_places=4)
    MainImage = models.TextField()
    VideoLink = models.TextField()
    Price = models.DecimalField(max_digits=18, decimal_places=4)
    PriceWithSale = models.DecimalField(max_digits=18, decimal_places=4)
    Location = models.CharField(max_length=200)
    Date = models.DateTimeField()
    AboutAz = models.TextField()
    AboutEn = models.TextField()
    AboutRu = models.TextField()

    @property
    def Status(self):
        model = apps.get_model("car_details.Status")
        return model.objects.filter(Id=self.StatusId)

    @property
    def StatusAdminSite(self):
        return self.Status[0] if self.Status.exists() else ''

    @property
    def Brand(self):
        model = apps.get_model("car_details.Brand")
        return model.objects.filter(Id=self.BrandId)

    @property
    def BrandAdminSite(self):
        return self.Brand[0] if self.Brand.exists() else ''

    @property
    def Model(self):
        model = apps.get_model("car_details.Model")
        return model.objects.filter(Id=self.ModelId)

    @property
    def ModelAdminSite(self):
        return self.Model[0] if self.Model.exists() else ''

    @property
    def BanType(self):
        model = apps.get_model("car_details.BanType")
        return model.objects.filter(Id=self.BanTypeId)

    @property
    def Ban(self):
        return self.BanType[0] if self.Model.exists() else ''

    @property
    def Fuel(self):
        model = apps.get_model("car_details.Fuel")
        return model.objects.filter(Id=self.FuelId)

    @property
    def Color(self):
        model = apps.get_model("car_details.Color")
        return model.objects.filter(Id=self.ColorId)

    @property
    def Currency(self):
        model = apps.get_model("myroot.Currency")
        return model.objects.get(Id=self.CurrencyId)

    @property
    def SpeedBox(self):
        model = apps.get_model("car_details.SpeedBox")
        return model.objects.filter(Id=self.SpeedBoxId)

    @property
    def CarImage(self):
        model = apps.get_model("car_details.CarImage")
        return model.objects.filter(CarId=self.Id)

    class Meta:
        db_table = 'Cars'


class CarAdminForm(forms.ModelForm):
    Model = forms.ChoiceField(label='Model', choices=[])
    BanType = forms.ChoiceField(label='BanType', choices=[])
    Status = forms.ChoiceField(label='Status', choices=[])
    Brand = forms.ChoiceField(label='Brand', choices=[])
    Fuel = forms.ChoiceField(label='Fuel', choices=[])
    Color = forms.ChoiceField(label='Color', choices=[])
    Currency = forms.ChoiceField(label='Currency', choices=[])

    class Meta:
        model = Car
        exclude = ['BanTypeId', 'StatusId', 'BrandId', 'ModelId', 'FuelId',
                   'ColorId', 'CurrencyId']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all available ModelIds
        model_ids = {model.Id: model.NameAz for model in apps.get_model("car_details.Model").objects.all()}
        ban_type_ids = {model.Id: model.NameAz for model in apps.get_model("car_details.BanType").objects.all()}
        status_ids = {model.Id: model.NameAz for model in apps.get_model("car_details.Status").objects.all()}
        brand_ids = {model.Id: model.NameAz for model in apps.get_model("car_details.Brand").objects.all()}
        fuel_ids = {model.Id: model.NameAz for model in apps.get_model("car_details.Fuel").objects.all()}
        color_ids = {model.Id: model.NameAz for model in apps.get_model("car_details.Color").objects.all()}
        currency_ids = {model.Id: model.Symbol for model in apps.get_model("myroot.Currency").objects.all()}
        # Set the choices for the custom fields
        self.fields['Model'].choices = [(id, name) for id, name in model_ids.items()]
        self.fields['BanType'].choices = [(id, name) for id, name in ban_type_ids.items()]
        self.fields['Status'].choices = [(id, name) for id, name in status_ids.items()]
        self.fields['Brand'].choices = [(id, name) for id, name in brand_ids.items()]
        self.fields['Fuel'].choices = [(id, name) for id, name in fuel_ids.items()]
        self.fields['Color'].choices = [(id, name) for id, name in color_ids.items()]
        self.fields['Currency'].choices = [(id, name) for id, name in currency_ids.items()]

    def save(self, commit=True):
        # Retrieve the selected custom IDs
        selected_model_id = self.cleaned_data.get('Model')
        selected_ban_type_id = self.cleaned_data.get('BanType')
        selected_status_id = self.cleaned_data.get('Status')
        selected_brand_id = self.cleaned_data.get('Brand')
        selected_fuel_id = self.cleaned_data.get('Fuel')
        selected_color_id = self.cleaned_data.get('Color')
        selected_currency_id = self.cleaned_data.get('Currency')
        # Set the custom fields in the Car instance
        self.instance.ModelId = selected_model_id
        self.instance.BanTypeId = selected_ban_type_id
        self.instance.StatusId = selected_status_id
        self.instance.BrandId = selected_brand_id
        self.instance.FuelId = selected_fuel_id
        self.instance.ColorId = selected_color_id
        self.instance.CurrencyId = selected_currency_id
        return super().save(commit)

class CarAdmin(admin.ModelAdmin):
    form = CarAdminForm

    list_display = ['Id', 'StatusAdminSite', 'BrandAdminSite', 'ModelAdminSite', 'Price', 'Ban']


admin.site.register(Car, CarAdmin)
