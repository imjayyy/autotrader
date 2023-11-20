from django.db import models
from django.apps import apps

class SocialMediaAccounts(models.Model):
    Id = models.BigAutoField(primary_key=True)
    SocialMediaId = models.IntegerField()
    AccountLink = models.TextField()

    @property
    def SocialMedia(self):
        model = apps.get_model("myroot.SocialMedia")
        return model.objects.get(Id=self.SocialMediaId)

    class Meta:
        db_table = 'SocialMediaAccounts'

    def __str__(self):
        return self.AccountLink
