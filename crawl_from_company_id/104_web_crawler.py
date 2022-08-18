import requests
import random
import json
import os
import math
import time
from static_vars import static_vars
from time import sleep


@static_vars(session=requests.session())
def get_104_ajax(url: str)->str:
    headers = {'referer': 'https://www.104.com.tw/'}
    r = get_104_ajax.session.get(url, headers=headers)

    sleep(random.uniform(1, 5))

    return r.text


def get_company_info(id: str)->dict:
    url = f'https://www.104.com.tw/company/ajax/content/{id}'
    html = get_104_ajax(url)

    data = json.loads(html)

    key = ['custName', 'industryDesc', 'indcat', 'custLink']
    return dict((k, data['data'][k]) for k in key)


def get_job_count(id: str)->str:
    url = f'https://www.104.com.tw/company/ajax/joblist/options/{id}'
    html = get_104_ajax(url)
    
    data = json.loads(html)
    return data['data']['jobCount']


def get_joblist(id: str)->list:
    result = list()

    job_count = get_job_count(id)
    pageSize = 100

    for page in range(1, math.ceil(job_count / pageSize) + 1):
        url = f'https://www.104.com.tw/company/ajax/joblist/{id}?page={page}&pageSize={pageSize}'
        html = get_104_ajax(url)

        j = json.loads(html)

        
        key_list = ['jobName', 'jobUrl', 'jobAddrNoDesc', 'periodDesc', 'edu', 'jobTags']

        job_list = j['data']['list']['topJobs'] + j['data']['list']['normalJobs']
        for job in job_list:
            if "研發替代役" in job['jobName']:
                tmp_job = dict((k, job[k]) for k in key_list)
                result.append(tmp_job)

    return result
    

def get_company_id_list()->list:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'all_company_id.csv')

    id_list = list()

    with open(filename, 'r') as f:
        for row in f.readlines():
            id = row.rsplit(',', 1)[1]
            id = id.strip()
            id_list.append(id)
    
    return id_list


if __name__ == '__main__':
    start_time = time.time()

    data = {'data': []}

    error_list = list()
    id_list = get_company_id_list()
    for i, id in enumerate(id_list, 1):
        try:
            company = get_company_info(id)
            print(f"{i}/{len(id_list)}", id, company)
            
            company['joblist'] = get_joblist(id)
            company['id'] = id
            company['job_count'] = len(company['joblist'])

            data['data'].append(company)
            print(company)
            print()
        except Exception as err:
            print(err)
            error_list.append(id)
        
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '104_jobs.json')
    with open(filename, 'w') as f:
        json.dump(data, f)

    print("error ids:", error_list)
    print(f"--- execute time: {time.time() - start_time} seconds ---")
    