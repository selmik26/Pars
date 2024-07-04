import requests
from bs4 import BeautifulSoup
import time
import math
import random

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
                    time.sleep(random.randint(5,15))
                    continue
                if soup.title.text == 'Тест Тьюринга':
                    print("Зайдите на сайт и пройдите Тест Тьюринга")
                    input("Нажмите enter чтобы продолжить\n")
                    i = 1
                    time.sleep(random.randint(5,15))
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
            time.sleep(random.randint(5,15))


def extract_pub(soup):
    pub_list = list()
    table = soup.find("table",{"id": "restab"})
    pub = table.find_all('tr', {"valign": "middle"})[1:]
    for i in range(len(pub)):
        if pub[i]["id"][0] == "a":
            id_pub = pub[i]["id"][3:]
        else:
            continue
        inf = pub[i].find_all('td')[1]
        inf_text = list(filter(lambda a: a != "", map(lambda x: x.replace("\xa0", " ").replace("\r", "").replace("\n", "").strip(), inf.strings)))
        name = inf_text[0]
        if inf.find('i') == None:
            author = "нет автора"
            information = " ".join(inf_text[1:])
        else:
            author = inf_text[1]
            information = " ".join(inf_text[2:])
        if "Версии:" in information:
            information = information[:information.find("Версии:") - 1]
        while "  " in information:
            information = information.replace("  ", " ")
        information = information.replace(";",".")
        resource = ""
        tom = ""
        number = ""
        data = ""
        page = ""
        if information[:13] == "Свидетельство":
            data = information[information.find(",") + 8 : information.find(",") + 12]
            resource = information.replace(information[information.find(","):information.find(",") + 12], "")
        else:
            information = information.split(".")
            information = list(filter(lambda a: a != "", map(lambda x: x.strip(), information)))
            if len(information) > 2 and information[-2] == "С":
                page = information[-1]
                information = information[:-2]
            if "№" in information[-1]:
                number = "".join(information[-1].split()[1:])
                information = information[:-1]
            if len(information) > 2 and information[-2] == "Т":
                tom = information[-1]
                information = information[:-2]
            data = information[-1].split()[-1]
            if len(information[-1]) != 4:
                if "/" in information[-1]:
                    information = information[:-1] + [information[-1][:information[-1].find("/")].strip()]
                elif "," not in information[-1]:
                    information = information[:-1] + [information[-1][:-4].strip()]
                else:
                    information = information[:-1]
            else:
                information = information[:-1]
            resource = ". ".join(information)
        pub_list.append({
            "id": id_pub,
            "name": name,
            "author": author,
            "resource": resource,
            "tom": tom,
            "number": number,
            "data": data,
            "page": page,
        })
    return pub_list


def extraction(soup):
    pub_list = list()
    page = soup.find("table",{"border":"0", "cellpadding": "0", "cellspacing":"3", "width":"480"})
    page = int(page.find('td',{"class": "redref"}).b.text)
    print("страница 1 из ", math.ceil(page/20) ,"\n")
    pub_list += extract_pub(soup)
    for i in range(2, math.ceil(page/20) + 1):
        print("страница ", i, " из ", math.ceil(page/20) ,"\n")
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
FilePub = open("ID_pub.csv", 'w')
FilePub.close()
FilePub = open("ID_pub.csv", 'a+')
FilePub.write("id пользователя;id публикации;название;авторы;источник;том;номер;год;страницы;\n")
FilePub.close()



for userid in FileID:
    userid = userid.strip()
    print(userid)

    payload = {
        "authorid": userid,
        "pagenum": "1",
        "show_option": "1",
    }

    url = "https://www.elibrary.ru/author_items.asp"
    soup = connect(payload, url)
    publication_list = extraction(soup)
    FilePub = open("ID_pub.csv", 'a+')
    for inf in publication_list:
        FilePub.write(userid + ";" + inf["id"] + ";" + inf["name"] + ";" + inf["author"] + ";" + inf["resource"] + ";" + inf["tom"] + ";" + inf["number"] + ";" + inf["data"] + ";" + inf["page"] + ";" + "\n")
    FilePub.close()
    time.sleep(random.randint(5,15))

FileID.close()
