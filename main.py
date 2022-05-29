import grequests
import requests
from lxml import etree
import argparse
from datetime import date


def exception_handler(request, exception):
    print("\033[31mRequest failed \033[0m with status ", request.status_code, request.url)


def format_response(url: str, title: str):
    return '{} [Электронный ресурс]. – URL: {} (дата обращения: {}).' \
        .format(title, url, date.today().strftime('%d.%m.%Y'))


def get_title(html):
    title = html.xpath('//h1//text()')
    if title and title[0]:
        return title[0]
    title = html.xpath('//h2//text()')
    if title and title[0]:
        return title[0]
    return 'Нет заголовка на странице'


def parse_links(urls_list):
    rs = (grequests.get(u) for u in urls_list)
    result = []
    for r in grequests.map(rs, size=16, exception_handler=exception_handler):
        if not r:
            exception_handler(r, '')
            result.append(format_response(r.url, r.url.split('//')[1].split('/')[0].capitalize()))
            continue
        html = etree.HTML(r.text)
        result.append(format_response(r.url, get_title(html)))
    return result


parser = argparse.ArgumentParser(description='application fot generation source links')
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--inter", type=bool, help="turns on interactive mode, type 'inter True' to start it")
group.add_argument("--url", type=str, help="site url to parse, ignored if file specified")
group.add_argument("--file", type=str, help="source file with links, one per line")

args = parser.parse_args()
inter = args.inter
url = args.url
file = args.file

res = []
if inter:
    while True:
        url = input('url сайта (https://habr.com/...)')
        print(parse_links([url])[0])
if url:
    res = parse_links([url])
if file:
    with open(file, 'r') as f:
        urls = [row.strip() for row in f]
        res = parse_links(urls)
for line in res:
    print(line)
