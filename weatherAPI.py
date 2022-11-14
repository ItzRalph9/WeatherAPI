import requests
import time
from datetime import datetime
import traceback

starttime = time.time()

lat = 52.274040
lon = 5.166590
API_key = "Ain't getting my key" # API key from 'weerlive.com'

def barometricPressure():
    response = requests.get(f"https://weerlive.nl/api/json-data-10min.php?key={API_key}&locatie=Bussum")
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    time_since_start = time.time() - starttime

    text_formatted = f"The pressure is: {response.json()['liveweer'][0]['luchtd']} mBar. Time: {current_time}"
    text_raw = f"{response.json()['liveweer'][0]['luchtd']} {current_time} {time_since_start}"
    
    with open("pressureData.txt", "a") as f:
        f.write(f"{text_formatted}\n")

    with  open("pressureDataRaw.txt", "a") as f:
        f.write(f"{text_raw}\n")

# an accurate way of running a function every 5 minutes
def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
    next_time += (time.time() - next_time) // delay * delay + delay

import threading
threading.Thread(target=lambda: every(300, barometricPressure)).start()
