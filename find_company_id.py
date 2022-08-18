import requests
import re
import os
import random
from bs4 import BeautifulSoup
from time import sleep



def find_id(name, session=None)->str:
    url = f'https://www.104.com.tw/company/search/?keyword={name}&jobsource=cs_custlist&mode=s'
    if session is None:
        r = requests.get(url)
    else:
        r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    companys = soup.find_all(class_='info-job__text')
    for company in companys:
        # 可能還會括號簡稱，不能只靠完全匹配去判斷
        if name in company['title']:
            return re.search('//www\.104\.com\.tw/company/(.*)\?.*', company['href']).group(1)
    
    return 'no_find'


if __name__ == '__main__':
    company_list = []

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'company_list.txt')
    with open(filename, 'r', encoding='utf-8') as f:
        for name in f.readlines():
            company_list.append(name.strip())

    filename = os.path.join(dirname, 'company_id.txt')
    session = requests.session()
    with open(filename, 'w', encoding='utf-8') as f:
        for company in company_list:
            id = find_id(company, session)

            print(f"{company}: {id}")
            f.write(f"{company},{id}\n")

            sleep(random.uniform(1, 5))
    