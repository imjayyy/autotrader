from django.db import models
from django.apps import apps

class TeamSocialMedia(models.Model):
    Id = models.BigAutoField(primary_key=True)
    TeamId = models.IntegerField()
    SocialMediaId = models.IntegerField()
    AccountLink = models.TextField()
    Icon = models.TextField()
    
    @property
    def Team(self):
        model = apps.get_model("myroot.Team")
        return model.objects.filter(Id=self.TeamId)
    
    @property
    def SocialMedia(self):
        model = apps.get_model("myroot.SocialMedia")
        return model.objects.get(Id=self.SocialMediaId)

    class Meta:
        db_table = 'TeamSocialMedias'