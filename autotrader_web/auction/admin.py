from django.contrib import admin

# Register your models here.
import csv

from django.contrib import admin
from import_export.admin import ImportMixin
from .models.shipping_auction_fee import ShippingAuctionFee
from .resources import ShippingAuctionFeeResource

class ShippingAuctionFeeAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ShippingAuctionFeeResource
    list_display = [ 'Id',  'AuctionShippingId',  'UserTypesId',  'CitiesId',  'Fee', ]
    search_fields = ['CitiesId'] 
    list_filter = ('AuctionShippingId', )  # Add fields you want to filter on

    # Define the admin action
    def import_data_from_csv(self, request, queryset):
        # Specify the CSV file path
        csv_file_path = '/autotrader_web/media/root/' + request.FILES['import_file'].name

        # Open and read the CSV file
        try:
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    try:
                        # Get the relevant fields from the CSV row
                        id_value = row.get('Id')
                        auction_shipping_id = row.get('AuctionShippingId')
                        user_types_id = row.get('UserTypesId')
                        cities_id = row.get('CitiesId')
                        fee = row.get('Fee')

                        # Look up the object in the queryset by 'Id'
                        obj = queryset.get(Id=id_value)

                        # Update the object fields
                        obj.AuctionShippingId = auction_shipping_id
                        obj.UserTypesId = user_types_id
                        obj.CitiesId = cities_id
                        obj.Fee = fee

                        # Save the updated object
                        obj.save()
                    except ShippingAuctionFee.DoesNotExist:
                        # Handle the case where the object with the specified 'Id' doesn't exist
                        new_obj = ShippingAuctionFee(
                                        Id=id_value,
                                        AuctionShippingId=auction_shipping_id,
                                        UserTypesId=user_types_id,
                                        CitiesId=cities_id,
                                        Fee=fee)
                        new_obj.save()
            # Provide a success message
            self.message_user(request, "Data imported successfully from CSV.")
        except FileNotFoundError:
            # Handle the case where the CSV file is not found
            self.message_user(request, "CSV file not found.")

    import_data_from_csv.short_description = "Import data from CSV"


admin.site.register(ShippingAuctionFee, ShippingAuctionFeeAdmin)
