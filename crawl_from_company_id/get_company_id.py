import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import os
import random


def get_all_company_id():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'all_company_id.txt')
    session = requests.session()
    with open(filename, 'w', encoding='utf-8') as f:
        for page in range(1, 101):
            print("page:", page)
            url = f'https://www.104.com.tw/company/search/?indcat=1001000000&page={page}&order=1&mode=s'
            r = session.get(url)
            sleep(random.uniform(1, 5))

            soup = BeautifulSoup(r.text, 'html.parser')

            joblist = soup.find_all(class_='info-job')

            for job in joblist:
                a_tag = job.find('a')
                company_name = a_tag.text

                link = a_tag['href']
                id = re.search('//www\.104\.com\.tw/company/(.*)\?.*', link).group(1)

                f.write(f'"{company_name}",{id}\n')


def merge_id_file():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'all_company_id.csv')

    m = dict()
    with open(filename, 'r') as f:
        for row in f.readlines():
            row = row.strip()
            name, id = row.rsplit(',', 1)
            m[id] = name

    filename = os.path.join(dirname, 'company_id.csv')
    with open(filename, 'r') as f:
        for row in f.readlines():
            row = row.strip()
            name, id = row.rsplit(',', 1)
            m[id] = m.get(id, name)

    filename = os.path.join(dirname, 'all_company_id.csv')
    with open(filename, 'w') as f:
        for id, name in m.items():
            f.write(f'{name},{id}\n')

if __name__ == '__main__':
    merge_id_file()