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


#            time.sleep(20)


def extraction(soup):
    pub_list = list()
    table = soup.find_all('table')[1]
    publications = table.find_all("tr")
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
        pub_list.append({
            "name": name,
            "author": author,
            "place": place
        })
    return pub_list


FileID = open("ID.txt", 'r')
FilePub = open("publications.txt", 'w')
for userid in FileID:
    userid = userid.strip()
    print(userid)
    soup = connect(userid)
    while soup.title.text == 'Тест Тьюринга':
        print("Зайдите на сайт и пройдите Тест Тьюринга")
        input("Нажмите enter чтобы продолжить\n")
        soup = connect(userid)
        time.sleep(20)
    publication_list = extraction(soup)
    FilePub.write('_' * 50 + userid + '_' * 50 + '\n')
    FilePub.write(str(len(publication_list)) + " публикаций\n")
    for i in range(len(publication_list)):
        FilePub.write(str(i + 1) + " " + publication_list[i]['name'] + "\n")
        FilePub.write(publication_list[i]['author'] + "\n")
        FilePub.write(publication_list[i]['place'] + "\n")

FileID.close()
FilePub.close()

# id155572 - Васильев Денис Юрьевич
# id112663 - Картак Вадим Михайлович

