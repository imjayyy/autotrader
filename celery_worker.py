import os
import subprocess
import sys

import django
from autotrader_web.myroot.process_data import Db_updater


"""
- Command to run celery_worker: celery -A celery_worker worker -B -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
"""

if os.getenv("SCRAPY_DEBUG") != "YES":
    sys.path.append(
        os.path.join(
            os.path.abspath(os.getcwd()), "./autotrader_scraper/autotrader_scraper"
        )
    )
    os.environ["DJANGO_SETTINGS_MODULE"] = "autotrader.settings"

    if os.getenv("ONLY_IMPORT_TASKS_FROM_CELERY") != "YES":
        sys.path.append(os.path.join(os.path.abspath(os.getcwd()), "autotrader_web"))
        django.setup()

    from celery import Celery
    from celery.utils.log import get_task_logger

    app = Celery("autotrader_celery")
    app.config_from_object("django.conf:settings", namespace="CELERY")
    # app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    app.control.enable_events(reply=True)
    logger = get_task_logger(__name__)


    @app.task
    def scrape_auctions_task_copart(*args, **kwargs):

        # Using Subprocess will avoid ReactorAlreadyRunning Exception

        cwd = os.path.abspath("autotrader_scraper/")
        Db_updater().update_all()
        
        subprocess.Popen(['scrapy', 'crawl', 'auction_spider_copart'], cwd=cwd)



    @app.task
    def scrape_auctions_task(*args, **kwargs):
        # Using Subprocess will avoid ReactorAlreadyRunning Exception

        cwd = os.path.abspath("autotrader_scraper/")
        subprocess.Popen(['scrapy', 'crawl', 'merged_auction_spider'], cwd=cwd)



