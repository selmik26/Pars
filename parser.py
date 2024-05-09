import requests
from bs4 import BeautifulSoup
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    'Connection': 'close'
}

# id155572 - Васильев Денис Юрьевич
# id112663 - Картак Вадим Михайлович
userid = "155572"
##i = 1
##while True:
##    try:
##        url = "https://www.elibrary.ru/author_profile.asp?authorid=112663"
##        req = requests.get(url, headers=headers)
##        src = req.text
##        print(src)
##        break
##    except Exception:
##        print(i)
##        i += 1

##time.sleep(5)


i = 1
while True:
    try:
        payload = {
            "authorid": userid,
            # "pagenum": "6"
        }
        url = "https://www.elibrary.ru/author_items_print.asp"
        req = requests.get(url, data=payload, headers=headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'lxml')
            #print(soup)
            table = soup.find_all('table')[1]
            #            print(table)
            publications = table.find_all("tr")
            for publication in publications:
                print(publication)
                print()
            break
        else:
            print("Ошибка", req.status_code)
            break
    except Exception as e:
        print("Попытка", i)
        print("Ошибка")
        print(e)
        print()
        i += 1
        time.sleep(random.randint(5, 15))
req.close()
