from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from updator import post_api

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(post_api.update_related_post_titles, 'interval', minutes=10)
    scheduler.start()