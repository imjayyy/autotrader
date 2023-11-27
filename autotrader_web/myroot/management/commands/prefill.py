from django.core.management.base import BaseCommand, CommandError
from autotrader_web.service.utils import update_model_from_csv
from car_details.models import *
from auction.models import *
from myroot.models import *
import os
from ...process_data import Db_updater
from multiprocessing import Process, Pipe

class Command(BaseCommand):
    help = 'Scrapping data from API daily'

    def handle(self, *args, **options):
        # parent_conn, child_conn = Pipe()
        # process = Process(target=Db_updater().update_all, args=(child_conn,))

        # def stream_function_output():
        #     process.start()            
        #     process.join()
        #     while True:
        #         try:
        #             yield parent_conn.recv() + '\n'
        #         except EOFError:
        #             break  # End the streaming when the process is done

        # stream_function_output()
        Db_updater().update_all
        # print(os.getcwd())
        # model_dict = [
        #     # car_details data
        #     {"data": "car.csv", "model": Car},
        #     {"data": "brand.csv", "model": Brand},
        #     {"data": "ban_type.csv", "model": BanType},
        #     {"data": "fuel.csv", "model": Fuel},
        #     {"data": "speed_box.csv", "model": SpeedBox},
        #     {"data": "status.csv", "model": Status},
        #     {"data": "car_image.csv", "model": CarImage},
        #     {"data": "color.csv", "model": Color},
        #     {"data": "model.csv", "model": Model},
        #     # auction data
        #     {"data": "cities.csv", "model": Cities},
        #     {"data": "auction_company.csv", "model": AuctionCompany},
        #     {"data": "auction_fee.csv", "model": AuctionFee},
        #     {"data": "auction_online_live_bid.csv", "model": AuctionOnlinelivebid},
        #     {"data": "shipping_company.csv", "model": ShippingCompany},
        #     {"data": "auction_shipping.csv", "model": AuctionShipping},
        #     {"data": "shipping_auction_fee.csv", "model": ShippingAuctionFee},
        #     {"data": "user_types.csv", "model": UserTypes},
        #     {"data": "users.csv", "model": Users},
        #     # myoot data
        #     {"data": "about.csv", "model": About},
        #     {"data": "admin.csv", "model": Admin},
        #     {"data": "blog.csv", "model": Blog},
        #     {"data": "cart.csv", "model": Cart},
        #     {"data": "currency.csv", "model": Currency},
        #     {"data": "faq.csv", "model": Faq},
        #     {"data": "gallery.csv", "model": Gallery},
        #     {"data": "message.csv", "model": Message},
        #     {"data": "order.csv", "model": Order},
        #     {"data": "partner.csv", "model": Partner},
        #     {"data": "product.csv", "model": Product},
        #     {"data": "product_image.csv", "model": ProductImage},
        #     {"data": "sale.csv", "model": Sale},
        #     {"data": "sale_product.csv", "model": SaleProduct},
        #     {"data": "service.csv", "model": Service},
        #     {"data": "setting.csv", "model": Setting},
        #     {"data": "slider_image.csv", "model": SliderImage},
        #     {"data": "social_media.csv", "model": SocialMedia},
        #     {"data": "social_media_account.csv", "model": SocialMediaAccounts},
        #     {"data": "team.csv", "model": Team},
        #     {"data": "team_social_media.csv", "model": TeamSocialMedia},
        #     {"data": "testimonial.csv", "model": Testimonial},
        #     {"data": "damage_type.csv", "model": DamageType}
        # ]

        # for x in model_dict:
        #     update_model_from_csv(f'autotrader_web/myroot/data/{x.get("data")}', x.get("model"))

        self.stdout.write(self.style.SUCCESS(f'Task Completed, DB Updated'))

