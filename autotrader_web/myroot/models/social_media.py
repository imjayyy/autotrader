from django.db import models
from django.apps import apps
from django.contrib import admin

class SocialMedia(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Icon = models.TextField()
    
    @property
    def SocialMediaAccounts(self):
        model = apps.get_model("myroot.SocialMediaAccounts")
        return model.objects.filter(SocialMediaId=self.Id)

    @property
    def TeamSocialMedia(self):
        model = apps.get_model("myroot.TeamSocialMedia")
        return model.objects.filter(SocialMediaId=self.Id)

    @property
    def Link(self):
        return self.SocialMediaAccounts[0] if self.SocialMediaAccounts.exists() else ''

    class Meta:
        db_table = 'SocialMedias'



class SocialMediaAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'Name',  'Link', ]

admin.site.register(SocialMedia,SocialMediaAdmin)

    