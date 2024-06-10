import requests
from bs4 import BeautifulSoup
import time
import math


def connect(payload, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Connection": "close",
    }

    i = 1
    while True:
        try:
            req = requests.get(url, data=payload, headers=headers)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'lxml')
                if soup.title == None:
                    print("Ваш IP-адрес забанили. Поменяйте IP")
                    input("Нажмите enter чтобы продолжить\n")
                    i = 1
                    time.sleep(20)
                    continue
                if soup.title.text == 'Тест Тьюринга':
                    print("Зайдите на сайт и пройдите Тест Тьюринга")
                    input("Нажмите enter чтобы продолжить\n")
                    i = 1
                    time.sleep(20)
                    continue
            else:
                print("Ошибка подключения", req.status_code)
                exit()
            return soup
        except Exception as error:
            print("Попытка", i)
            print("Ошибка")
            print(error)
            print()
            i += 1


##            time.sleep(20)


def extract_pub(soup):
    list_id = []
    table = soup.find("table", {"id": "restab"})
    pub = table.find_all('tr', {"valign": "middle"})[1:]
    for i in range(len(pub)):
        list_id.append(pub[i]["id"][3:])
    return list_id


def extraction(soup):
    pub_list = list()
    page = soup.find("table", {"border": "0", "cellpadding": "0", "cellspacing": "3", "width": "480"})
    page = int(page.find('td', {"class": "redref"}).b.text)
    print("страница 1 из ", math.ceil(page / 20), "\n")
    pub_list += extract_pub(soup)
    for i in range(2, math.ceil(111 / 20) + 1):
        print("страница ", i, " из ", math.ceil(page / 20), "\n")
        payload = {
            "authorid": "112663",
            "pagenum": i,
            "show_option": "1",
        }
        url = "https://www.elibrary.ru/author_items.asp"
        soup = connect(payload, url)
        pub_list += extract_pub(soup)

    return pub_list


FileID = open("ID.txt", 'r')
FilePub = open("publications.csv", 'w')

for userid in FileID:
    userid = userid.strip()
    print(userid)

    payload = {
        "authorid": "112663",
        "pagenum": "1",
        "show_option": "1",
    }
    url = "https://www.elibrary.ru/author_items.asp"
    soup = connect(payload, url)

    publication_list = extraction(soup)

    for i in range(len(publication_list)):
        FilePub.write(userid + ";" + publication_list[i] + ";" + "\n")
#    time.sleep(20)

FileID.close()
FilePub.close()

# количество страниц
# soup.find_all("table",{"border":"0", "cellpadding": "0", "cellspacing":"3", "width":"480"})

# публикации
# soup.find_all("table",{"id": "restab"})


