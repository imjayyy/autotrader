from django.db import models
from django.contrib import admin


class Testimonial(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Fullname = models.CharField(max_length=100)
    Profession = models.CharField(max_length=100)
    Comment = models.TextField(max_length=500)
    Image = models.TextField()
    AddDate = models.DateTimeField()
    StarCount = models.IntegerField()

    class Meta:
        db_table = 'Testimonials'



class TestimonialAdmin(admin.ModelAdmin):
    list_display = [ 'Id',  'Fullname',  'Profession',  'Comment',  'Image',  'AddDate',  'StarCount', ]

admin.site.register(Testimonial,TestimonialAdmin)

    