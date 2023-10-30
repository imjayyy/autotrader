# myroot/tasks.py

from celery import shared_task
from process_data import Db_updater  # Import your existing function

@shared_task
def daily_db_update():
    Db_updater().update_all()
