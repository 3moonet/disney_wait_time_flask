from main import app
import multiprocessing
from main.mksched import execute_schedule

def run():
    p1 = multiprocessing.Process(target=execute_schedule, args=('tdl',))
    p2 = multiprocessing.Process(target=execute_schedule, args=('tds',))
    p1.daemon = True
    p2.daemon = True
    p1.start()
    p2.start()
    app.run()

if __name__ == "__main__":
    run()