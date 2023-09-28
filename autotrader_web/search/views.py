import math
from django.views.generic.base import TemplateView
from car_details.models import *
import datetime as datetime
from django.db.models import Count,Q
from myroot.languages import languages
from django.shortcuts import render
from service.auction.search import AuctionSearchService
from myroot.languages import languages


class SearchView(TemplateView):
    template_name = 'auction/search.html'

    def get(self, request):
        page = 1 if "page" not in request.GET.keys() else int(request.GET.get("page"))
        auction_lots_service = AuctionSearchService()
        search_results = auction_lots_service.search_lots(request.GET)
        active_filters = auction_lots_service.get_active_filters(request.GET)
        context = {
            "search_results": auction_lots_service.get_page_from_search_results(search_results, page),
            "active_filters": active_filters,
            "search_filters": auction_lots_service.get_search_filters(search_results, active_filters, languages[request.lang]),
            "total_search_results": len(search_results),
            "buy_it_now_total": LotData.objects.filter(buyItNow=1).count(),
            "lang": languages[request.lang]}
        # for fi in context["search_filters"]:
        #     if fi.get("name") == "Damage Type":
        #         for row in fi.get("data"):
        #             row["value"] = languages[request.lang][row["value"]] if row["value"] in languages[request.lang].keys() else row["value"]
        response = render(request, self.template_name, context)
        return response
