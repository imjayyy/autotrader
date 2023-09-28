from car_details.models import LotData
from django.db.models import Count
from auction.models import AuctionCompany


def admin_index_middleware(get_response):

    def middleware(request):
        if "/admin" in request.path:

            try:
                request.iaai_lots = LotData.objects.filter(auctionCompanyId=AuctionCompany.objects.get(Name__icontains="IAAI").Id).values("auctionCompanyId").annotate(total=Count("auctionCompanyId"))[0].get("total")
            except Exception as e:
                request.iaai_lots = 0
            try:
                request.copart_lots = LotData.objects.filter(auctionCompanyId=AuctionCompany.objects.get(Name__icontains="Copart").Id).values("auctionCompanyId").annotate(total=Count("auctionCompanyId"))[0].get("total")
            except Exception as e:
                request.copart_lots = 0

        response = get_response(request)
        return response

    return middleware
