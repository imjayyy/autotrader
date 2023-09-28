from django.db import models
from django.contrib import admin


class OrderNow(models.Model):
    Id = models.BigAutoField(primary_key=True)
    FirstName = models.CharField(max_length=255, null=True)
    LastName = models.CharField(max_length=255, null=True)
    Phone = models.CharField(max_length=255, null=True)
    Email = models.CharField(max_length=255, null=True)
    Message = models.TextField(null=True)
    LotId = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'OrderNow'

    def __str__(self):
        return self.FirstName

class OrderNowAdmin(admin.ModelAdmin):
    list_display = ['Id', 'FirstName', 'LastName', 'Phone', 'Email']
    change_form_template = 'admin/order_now/change_form.html'

    def change_view(self, request, object_id, extra_context=None):
        obj = OrderNow.objects.get(Id=object_id)
        lot_details_url = f'/lots/{obj.LotId}'
        extra_context = extra_context or {}
        extra_context["details_url"] = lot_details_url
        return super().change_view(request, object_id, extra_context=extra_context)

admin.site.register(OrderNow, OrderNowAdmin)
