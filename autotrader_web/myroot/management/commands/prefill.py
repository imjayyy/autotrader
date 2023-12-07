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
        parent_conn, child_conn = Pipe()
        Db_updater().update_all(child_conn)
        
        self.stdout.write(self.style.SUCCESS(f'Task Completed, DB Updated'))

