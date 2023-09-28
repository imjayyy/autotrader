from django.db import models
from django.apps import apps
from django.contrib import admin


class Team(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    Image = models.TextField()
    Profession = models.CharField(max_length=200)
    Email = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    Address = models.TextField(max_length=300)
    Biography = models.TextField()
    
    @property
    def TeamSocialMedia(self):
        model = apps.get_model("myroot.TeamSocialMedia")
        return model.objects.filter(TeamId=self.Id)

    class Meta:
        db_table = 'Teams'



class TeamAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'Firstname',  'Lastname',  'Image',  'Profession',  'Email',  'Phone',  'Address',  'Biography', ]

admin.site.register(Team,TeamAdmin)

    