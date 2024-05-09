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
i = 1
while True:
    try:
        payload = {
            "authorid": userid,
        }
        url = "https://www.elibrary.ru/author_items_print.asp"
        req = requests.get(url, data=payload, headers=headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'lxml')
            table = soup.find_all('table')[1]
            publications = table.find_all("tr")
            publication_list = list()
            for publication in publications:
                place = publication.text
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
