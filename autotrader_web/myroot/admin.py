import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from car_details.models import LotData
from celery_worker import *

from myroot.management.commands.prefill import Command

class MyrootAdminSite(admin.AdminSite):
    index_template = 'admin/index.html'

    def get_urls(self):
        return [
            path('run-scraper/', self.run_scraper),
            path('run-copart-scraper/', self.run_copart_scraper),
            path('run-iaai-scraper/', self.run_iaai_scraper),
            path('open-calculator/', self.open_calculator),
            path('delete-old-lots/', self.delete_old_lots),
            path('update-from-csv/', self.update_from_csv),
        ] + super().get_urls()

    def run_scraper(self, request):
        scrape_auctions_task.delay()
        scrape_auctions_task_copart.delay()
        return HttpResponseRedirect("../")

    def run_copart_scraper(self, request):
        scrape_auctions_task_copart.delay()
        LotData.objects.filter(auctionCompanyId=1, saledate__lte=datetime.datetime.now()).delete()
        return HttpResponseRedirect("../")

    def run_iaai_scraper(self, request):
        scrape_auctions_task.delay()
        LotData.objects.filter(auctionCompanyId=2, saledate__lte=datetime.datetime.now()).delete()
        return HttpResponseRedirect("../")

    def update_from_csv(self, request):
        Command().handle()
        return HttpResponseRedirect("../")

    def open_calculator(self, request):
        return HttpResponseRedirect("/calc-page")

    def delete_old_lots(self, request):
        LotData.objects.filter(saledate__lte=(datetime.datetime.now()-datetime.timedelta(days=1))).delete()
        return HttpResponseRedirect("../")