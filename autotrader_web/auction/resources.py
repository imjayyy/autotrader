# yourapp/resources.py
from import_export import resources
from .models.shipping_auction_fee import ShippingAuctionFee

class ShippingAuctionFeeResource(resources.ModelResource):
    class Meta:
        model = ShippingAuctionFee
    def get_import_id_fields(self):
        return ['Id']