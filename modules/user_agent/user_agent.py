import random
import requests
from rich.console import Console


def random_user_agent():
    # Open File
    ua_list = []
    test_url = "https://httpbin.org/user-agent"
    console = Console()

    with open('modules/user_agent/user_agent.txt', 'r', encoding='UTF-8') as file:
        for f in file.readlines():
            ua_list.append(f.strip())

    random_ua = ua_list[random.randint(0, len(ua_list))]
    req = requests.get(test_url, headers={
        "user-agent": random_ua
    })


    if (req.status_code == 200) & (req.json()['user-agent'] == random_ua):
        console.print("User Agent oluşturuldu..", style="bold green")

        return random_ua
    else:
        console.print('Bir sorun meydana geldi. [user-agent]', style="bold red")
    