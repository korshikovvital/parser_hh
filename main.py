from bs4 import BeautifulSoup
import requests
import lxml
import csv

headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}

# получаем html
# def data(url):
#     response=requests.get(url,headers=headers)
#     return response.text
#
# html=data('https://spb.hh.ru/search/vacancy?text=django&from=suggest_post&fromSearchLine=true&area=2')
#
# # запишем html,чтоб постоянно не отправлять  запрос
#
# with open('index.html','w') as file:
#     file.write(html)

with open('index.html') as file:
    file = file.read()


def parser():
    soup = BeautifulSoup(file, 'lxml')
    all_vacan = soup.find('div', class_="vacancy-serp-content").find_all(class_="vacancy-serp-item")
    for num,item in enumerate(all_vacan):
        if num==0:

            # Забираем название и ссылку вакансии
            title = item.find('h3').text
            href = item.find('h3').find('span', class_='g-user-content').find('a').get('href')
            # Забираем описание
            rez = requests.get(href, headers=headers)
            soup = BeautifulSoup(rez.text,'lxml')
            # работадатель
            work=soup.find('div',class_="bloko-columns-row").find('div',class_="vacancy-company-top").text
            # Описание вакансии
            description=soup.find_all('div',class_="bloko-columns-row").find('div',class_="bloko-columns-row")[2].text
            print(work,description)

            with open('vacan.csv','a') as f:
                writer=csv.writer(f)
                writer.writerow(
                    (
                        title,
                        href,
                        work,
                        description
                    )
                )




parser()
