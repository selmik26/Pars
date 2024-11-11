import requests
from bs4 import BeautifulSoup
import time
import math
import random

sl_tm = 15
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    "Connection": "close",
}


def connect(payload):
    url = "https://www.elibrary.ru/author_items.asp"

    i = 1
    while True:
        try:
            req = s.get(url, data=payload, headers=headers)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'lxml')
                if soup.title == None:
                    print("Ваш IP-адрес забанили. Поменяйте IP")
                    input("Нажмите enter чтобы продолжить\n")
                    i = 1
                    time.sleep(sl_tm)
                    continue
                if soup.title.text == 'Тест Тьюринга':
                    print("Зайдите на сайт и пройдите Тест Тьюринга")
                    input("Нажмите enter чтобы продолжить\n")
                    i = 1
                    time.sleep(sl_tm)
                    continue
            else:
                print("Ошибка подключения", req.status_code)
                buf = input("Прододжить? (y/n)")
                while (not (buf == "y" or buf == "n")):
                    buf = input("Прододжить? (y/n)")
                if (buf == "y"):
                    continue
                else:
                    exit()
            return soup
        except Exception as error:
            print("Попытка", i)
            print("Ошибка")
            print(error)
            print()
            i += 1
            time.sleep(sl_tm)


def pub_extract(soup):
    pub_list = list()
    table = soup.find("table", {"id": "restab"})
    pub = table.find_all('tr', {"valign": "middle"})[1:]
    for i in range(len(pub)):
        if pub[i]["id"][0] == "a":
            id_pub = pub[i]["id"][3:]
        else:
            continue
        inf = pub[i].find_all('td')[1]
        inf_text = list(filter(lambda a: a != "",
                               map(lambda x: x.replace("\xa0", " ").replace("\r", "").replace("\n", "").strip(),
                                   inf.strings)))
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
        information = information.replace(";", ".")
        resource = ""
        tom = ""
        number = ""
        data = ""
        page = ""
        if information[:13] == "Свидетельство":
            data = information[information.find(",") + 8: information.find(",") + 12]
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
            "BAK": "не включен",
        })
    return pub_list


def extraction(soup, payload):
    pub_list = list()
    page = soup.find("table", {"border": "0", "cellpadding": "0", "cellspacing": "3", "width": "480"})
    if (page == None): return pub_list
    page = int(page.find('td', {"class": "redref"}).b.text)
    print("страница 1 из ", math.ceil(page / 20), "\n")
    pub_list += pub_extract(soup)
    for i in range(2, math.ceil(page / 20) + 1):
        print("страница ", i, " из ", math.ceil(page / 20), "\n")
        payload["pagenum"] = i
        soup = connect(payload)
        pub_list += pub_extract(soup)
    return pub_list


def BAK_extract(soup):
    BAK_list = list()
    table = soup.find("table", {"id": "restab"})
    pub = table.find_all('tr', {"valign": "middle"})[1:]
    for i in range(len(pub)):
        if pub[i]["id"][0] == "a":
            BAK_list.append(pub[i]["id"][3:])
        else:
            continue
    return BAK_list


def BAK(payload, pub_list):
    BAK_list = list()
    print("нахождение статьей вкюченных в BAK\n")
    payload["show_option"] = "5"
    soup = connect(payload)
    page = soup.find("table", {"border": "0", "cellpadding": "0", "cellspacing": "3", "width": "480"})
    if (page == None): return BAK_list
    page = int(page.find('td', {"class": "redref"}).b.text)
    print("страница 1 из ", math.ceil(page / 20), "\n")
    BAK_list += BAK_extract(soup)
    for i in range(2, math.ceil(page / 20) + 1):
        print("страница ", i, " из ", math.ceil(page / 20), "\n")
        payload["pagenum"] = i
        soup = connect(payload)
        BAK_list += BAK_extract(soup)
    j = 0
    print("Обработка\n")
    for i in range(len(BAK_list)):
        while (BAK_list[i] != pub_list[j]["id"]):
            j += 1
        pub_list[j]["BAK"] = "включен"
    return pub_list


FileID = open("ID.txt", 'r')
FilePub = open("ID_pub.csv", 'w', encoding='utf-8')
FilePub.close()
FilePub = open("ID_pub.csv", 'a+', encoding='utf-8')
FilePub.write("id пользователя;id публикации;название;авторы;источник;том;номер;год;страницы;ВАК\n")
FilePub.close()

years = []
res = input("Включит фильтр по годам? (y/n)\n").lower()
while res != 'y' and res != 'n':
    res = input("Включит фильтр по годам? (y/n)\n").lower()
if res == 'y':
    print("Введите года через пробел, без лишних символов")
    years = input().strip().split()
    while True:
        try:
            years = list(map(int, years))
            assert (len(list(filter(lambda x: x < 3000, years))) == len(years))
            break
        except Exception:
            print("Введите года через пробел, без лишних символов")
            years = input().strip().split()

payload = {
    "pagenum": "1",
    "show_option": "1",
}

if res == "y":
    payload["year_order"] = "1"
    for i in range(len(years)):
        payload["years_" + str(years[i])] = "on"

global s
print("Настройка")
i = 1
while True:
    try:
        s = requests.Session()
        r = s.get("https://www.elibrary.ru/defaultx.asp", headers=headers)
        break
    except Exception as e:
        print("Попытка", i)
        print(e)
        print()
        i += 1
        s.close()
        time.sleep(10)

for userid in FileID:
    userid = userid.strip()
    payload["authorid"] = userid
    print(userid)
    soup = connect(payload)
    publication_list = extraction(soup, payload)
    if publication_list != []:
        publication_list = BAK(payload, publication_list)

        FilePub = open("ID_pub.csv", 'a+', encoding='utf-8')

        for inf in publication_list:
            FilePub.write(userid + ";" + inf["id"] + ";")
            FilePub.write(inf["name"] + ";" + inf["author"] + ";")
            FilePub.write(inf["resource"] + ";" + inf["tom"] + ";")
            FilePub.write(inf["number"] + ";" + inf["data"] + ";")
            FilePub.write(inf["page"] + ";" + inf["BAK"] + ";" + "\n")
        FilePub.close()
    time.sleep(sl_tm)
FileID.close()
input("Нажмите Enter чтобы завершить")

