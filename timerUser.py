import time
from multiprocessing.context import Process
import schedule

class ScheduleMessage:
    def try_send_schedule():
        while True:
            schedule.run_pending()
            timer.sleep(1)

    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()
