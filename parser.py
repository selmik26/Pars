import requests
from bs4 import BeautifulSoup
import time
import random


def connect(userid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        'Connection': 'close'
    }

    payload = {
        "authorid": userid,
    }

    url = "https://www.elibrary.ru/author_items_print.asp"

    i = 1
    while True:
        try:
            req = requests.get(url, data=payload, headers=headers)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'lxml')
                req.close()
            else:
                print("Ошибка подключения", req.status_code)
                exit()
            return soup
        except Exception as e:
            print("Попытка", i)
            print("Ошибка")
            print(e)
            print()
            i += 1
            time.sleep(20)


# id155572 - Васильев Денис Юрьевич
# id112663 - Картак Вадим Михайлович
userid = "112663"

soup = connect(userid)
table = soup.find_all('table')[1]
publications = table.find_all("tr")
publication_list = list()
ind = 1
for publication in publications:
    information = publication.find_all('td')[1]
    information_text = list(information.strings)
    if information.find('i') == None:
        if information_text[0] == "\n":
            i = 1
        else:
            i = 0
        name = information_text[i]
        author = "No authors"
        place = information_text[i + 1]
    else:
        if information_text[0] == "\n":
            i = 1
        else:
            i = 0
        name = information_text[i]
        author = information_text[i + 1]
        place = information_text[i + 2]
    print(ind)
    print(name)
    print(author)
    print(place)
    print()
    ind += 1
print(soup)
