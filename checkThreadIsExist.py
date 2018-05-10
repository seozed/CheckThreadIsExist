# -*- coding:utf-8 -*-
"""
DATE: 2018/4/27
"""

import ggrequests as grequests

keywords = (line.strip() for line in open('keywords.txt', encoding='utf8').readlines())

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
}


def read_urls(path):
    with open(path) as file:
        return [line.strip() for line in file.readlines() if line.startswith('http')]


def vaild(response):
    if response['status_code'] in (404,):
        return False

    global keywords

    for key in keywords:
        if key in response['text']:
            return False

    return True


def save(items):
    import csv
    with open('result.csv', 'w', newline='', encoding='utf8') as csvfile:
        fieldnames = items[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)


def exception_handler(request, exception):
    item = grequests.extract_item(request)
    return item

def main():

    rs = (grequests.get(u) for u in read_urls('urls.txt'))
    response_list = grequests.map(rs, gtimeout=10)
    for response in response_list:
        response['is_exist'] = vaild(response)
        del response['text']
        print("响应码：[{0[status_code]}]\t{0[url]}\t{0[is_exist]}".format(response))

    save(response_list)

if __name__ == '__main__':
    main()


rs = (grequests.get(u) for u in read_urls('urls.txt'))
response_list = grequests.map(rs, gtimeout=10)
for response in response_list:
    response['is_exist'] = vaild(response)
    del response['text']
    print("响应码：[{0[status_code]}]\t{0[url]}\t{0[is_exist]}".format(response))