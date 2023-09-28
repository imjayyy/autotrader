from pyexpat import model
from django.db import models
from django.apps import apps


class Users(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Surname = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Phone = models.CharField(max_length=50)
    Address = models.CharField(max_length=200)
    Active = models.IntegerField()
    UserTypesId = models.BigIntegerField()
    

    @property
    def UserTypes(self):
        model = apps.get_model("auction.UserTypes")
        return model.objects.filter(Id=self.UserTypesId)
    
    class Meta:
        db_table = 'Users'