from django.db import models

class Admin(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Username = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Password = models.TextField()

    class Meta:
        db_table = 'Admin'