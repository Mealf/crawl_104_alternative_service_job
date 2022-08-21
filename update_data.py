import os
from os.path import exists
from datetime import datetime
import shutil

def file_exist()->bool:
    dirname = os.path.dirname(__file__)
    website_dir = os.path.join(dirname, 'website')
    filename = os.path.join(website_dir, '104_jobs.json')

    src_dir = os.path.join(dirname, 'crawl_from_search')
    src = os.path.join(src_dir, '104_jobs.json')

    return  exists(filename) and exists(src)

def rename_file()->None:
    dirname = os.path.dirname(__file__)
    website_dir = os.path.join(dirname, 'website')
    filename = os.path.join(website_dir, '104_jobs.json')

    data_time = os.path.getmtime(filename)
    data_time = datetime.fromtimestamp(data_time).strftime(r"%m%d")
    new_filename = os.path.join(website_dir, f'104_jobs-{data_time}.json')

    os.rename(filename, new_filename)
    print('file rename complete!!')


def copy_file()->None:
    dirname = os.path.dirname(__file__)
    src_dir = os.path.join(dirname, 'crawl_from_search')
    src = os.path.join(src_dir, '104_jobs.json')

    dst_dir = os.path.join(dirname, 'website')
    shutil.copy2(src, dst_dir)
    print('file copy complete!!')

if __name__ == '__main__':
    if file_exist():
        rename_file()
        copy_file()

    else:
        print('file not exist')