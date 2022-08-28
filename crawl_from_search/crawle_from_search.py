import requests
import random
import os
import re
import json
from time import sleep
from static_vars import static_vars
from bs4 import BeautifulSoup
from os.path import exists


@static_vars(session=requests.session())
def get_session():
    return get_session.session


def get_104_ajax(url: str)->str:
    headers = {'referer': 'https://www.104.com.tw/'}
    r = get_session().get(url, headers=headers)

    sleep(random.uniform(0.1, 2))

    return r.text


def get_search_html(keyword, page)->str:
    url = f'https://www.104.com.tw/jobs/search/?ro=0&keyword={keyword}&expansionType=area,spec,com,job,wf,wktm&page={page}&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'
    r = get_session().get(url)

    sleep(random.uniform(0.1, 2))

    return r.text


@static_vars(company_list=None)
def get_company_info(id: str)->dict:
    if get_company_info.company_list is None:
        get_company_info.company_list = load_company_info()
    
    
    # search in file data
    for company in get_company_info.company_list['data']:
        if company['id'] == id:
            return company

    # not find in file, search website    
    url = f'https://www.104.com.tw/company/ajax/content/{id}'
    html = get_104_ajax(url)

    data = json.loads(html)

    key = ['custName', 'industryDesc', 'indcat', 'custLink']
    company_info = dict((k, data['data'][k]) for k in key)
    company_info['id'] = id

    
    add_company_info(company_info)
    get_company_info.company_list['data'].append(company_info)

    return company_info

def load_company_info() -> dict:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'company_info.json')

    if not exists(filename):
        data = {'data': []}
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    return data


def add_company_info(company_info: dict) -> None:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'company_info.json')

    # load file
    with open(filename, 'r') as f:
        data = json.load(f)

    # updata data
    data['data'].append(company_info)

    # save file
    with open(filename, 'w') as f:
        json.dump(data, f)



def get_total_page(keyword) -> int:
    html = get_search_html(keyword, 1)
    return int(re.search('\"totalPage\":([0-9]+),', html).group(1))
    

def add_job_to_company(id: str, job:dict, data: dict) -> None:
    for company_info in data['data']:
        if id == company_info['id']:
            company_info['joblist'].append(job)
            return
    
    # not in data
    company_info = get_company_info(id)
    company_info['joblist'] = [job]

    data['data'].append(company_info)


def get_job_list(html: str, data: dict) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    job_list_tag = soup.find_all('article', class_='job-list-item')
    for job_container in job_list_tag:
        job = dict()
        link = job_container.find('a', class_='js-job-link')
        job['jobName'] = link.text
        job['jobUrl'] = link['href']

        company_info = job_container.find('ul', class_='b-list-inline')
        company_url = company_info.find('a')['href']
        company_id = re.search('//www.104.com.tw/company/(.*)\?jobsource', company_url).group(1)
        print(company_id)
        
        
        job_intro = job_container.find('ul', class_='job-list-intro')
        job_intro_list = job_intro.find_all('li')
        job['jobAddrNoDesc'] = job_intro_list[0].text
        job['periodDesc'] = job_intro_list[1].text
        job['edu'] = job_intro_list[2].text
        job['jobTags'] = job_container.find('div', class_='job-list-tag').find('span').text

        add_job_to_company(company_id, job, data)

        print(job)
        print()


def add_job_count(data: dict) -> None:
    for company in data['data']:
        company['job_count'] = len(company['joblist'])


if __name__ == '__main__':
    keyword = '研發替代役'
    total_page = get_total_page(keyword)

    data = {'data': list()}

    for page in range(1, total_page+1):
        print(f'page: {page}/{total_page}')
        html = get_search_html(keyword, page)
        get_job_list(html, data)
    
    add_job_count(data)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '104_jobs.json')
    with open(filename, 'w') as f:
        json.dump(data, f)