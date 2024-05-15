import requests
from bs4 import BeautifulSoup
import time


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


def extraction(soup):
    pub_list = list()
    table = soup.find_all('table')[1]
    publications = table.find_all("tr")
    ##    i = 1
    for pub in publications:
        inf = pub.find_all('td')[1]
        inf_text = list(inf.strings)
        if inf.find('i') == None:
            if inf_text[0] == "\n":
                ind = 1
            else:
                ind = 0
            name = inf_text[ind].strip()
            author = "No authors"
            place = inf_text[ind + 1].strip()
        else:
            if inf_text[0] == "\n":
                ind = 1
            else:
                ind = 0
            name = inf_text[ind].strip()
            author = inf_text[ind + 1].strip()
            place = inf_text[ind + 2].strip().replace("\xa0", " ").replace("\r\n", "")
        ##        print(i)
        ##        print(name)
        ##        print(author)
        ##        print(place)
        ##        print()
        ##        i+=1
        pub_list.append({
            "name": name,
            "author": author,
            "place": place
        })
    return pub_list


FileID = open("ID.txt", 'r')
for userid in FileID:
    print(userid)
    soup = connect(userid)
    publication_list = extraction(soup)
    print(publication_list)
FileID.close()

# id155572 - Васильев Денис Юрьевич
# id112663 - Картак Вадим Михайлович

