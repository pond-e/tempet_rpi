import requests
import time
import active
import remember
import stop


while(True):
    res = requests.get('https://tempet.sakura.tv/tempet/Raspi_state.txt')
    print(res.content)

    res2 = res.content.decode()
    print(res2)

    if res2 == "active":
        active.main()
    elif res2 == "cooling":
        remember.main(res2)
    elif res2 == "heating":
        remember.main(res2)
    elif res2 == "dehumidificaton":
        remember.main(res2)
    elif res2 == "temperature":
        remember.main(res2)
    elif res2 == "power":
        remember.main(res2)
    elif res2 == "stop_button":
        remember.main(res2)
    elif res2 == "stop":
        stop.main()
    
    time.sleep(10)