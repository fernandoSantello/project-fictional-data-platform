from apscheduler.schedulers.blocking import BlockingScheduler
from controller.controller import Controller

def main():
    controller = Controller()
    scheduler = BlockingScheduler()
    scheduler.add_job(controller.execution_process, 'interval', minutes=1)
    scheduler.start()

if __name__ == '__main__':
    main()
    