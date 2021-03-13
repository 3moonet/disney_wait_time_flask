import schedule
import datetime
from time import sleep

from main.post import post_wait_time, post_opening_time, post_show_list, post_daily_close


def execute_schedule(park):
    while True:
        opening_time = post_opening_time(park=park)
        sleep(5)
        post_daily_close(park=park)
        sleep(5)
        
        open_time = opening_time[0]
        close_time = opening_time[1]
        
        while True: # before open
            now = datetime.datetime.now().time()
            if now < open_time:
                sleep(900)
            else:
                break
        

        now = datetime.datetime.now().time()
        if now < close_time:
            post_show_list(park=park)

        
        schedule.clear()
        schedule.every().hour.at(':15').do(post_wait_time, park=park)
        schedule.every().hour.at(':45').do(post_wait_time, park=park)
        while True: # while opening
            now = datetime.datetime.now().time()
            if now < close_time:
                schedule.run_pending()
                sleep(50)
            else:
                break
        
        today = datetime.datetime.now().date()
        while True: #after close, bofore new day
            now_day = datetime.datetime.now().date()
            if now_day == today:
                sleep(900)
            else:
                break
