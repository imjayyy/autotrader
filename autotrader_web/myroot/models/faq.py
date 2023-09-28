from django.db import models
from django.contrib import admin


class Faq(models.Model):
    Id = models.BigAutoField(primary_key=True)
    QuestionAz = models.TextField()
    QuestionEn = models.TextField()
    QuestionRu = models.TextField()
    AnswerAz = models.TextField()
    AnswerEn = models.TextField()
    AnswerRu = models.TextField()

    class Meta:
        db_table = 'Faqs'

class FaqAdmin(admin.ModelAdmin):
    list_display = ['Id', 'QuestionAz', 'AnswerAz']

admin.site.register(Faq,FaqAdmin)