import schedule
import time
from main import run_agent

POST_TIMES = [
    "14:06",
    "15:00",
    "21:00"
]

for t in POST_TIMES:
    schedule.every().day.at(t).do(run_agent)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(20)