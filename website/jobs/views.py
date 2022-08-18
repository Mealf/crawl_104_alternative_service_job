from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import os
import json


def index(request):
    dirname = os.path.abspath('')
    filename = os.path.join(dirname, '104_jobs.json')
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    data_time = os.path.getmtime(filename)
    data_time = datetime.fromtimestamp(data_time).strftime(r"%Y-%m-%d %H:%M:%S")
    
    return render(request, 'jobs/index.html', {'company_list': data, 'data_time': data_time})