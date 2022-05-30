import grequests
from lxml import etree
import argparse
import datetime
import validators
import random
from banner import banner

print(banner)


def exception_handler(request, exception):
    print("\033[31mRequest failed \033[0m with status ", request.status_code, request.url)


def not_valid_handler(url):
    print("\033[31mURL not valid \033[0m", url)


def format_response(url: str, title: str):
    application_date = (datetime.datetime.today() - datetime.timedelta(random.randint(0, span))).strftime('%d.%m.%Y')
    return '{} [Электронный ресурс]. – URL: {} (дата обращения: {}).' \
        .format(title, url, application_date)


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


def valid_filter(url):
    if not validators.url(url):
        not_valid_handler(url)
    return validators.url(url)


parser = argparse.ArgumentParser(description='application for generation source links')
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-i", "--inter", action='store_true', help="turns on interactive mode")
group.add_argument("-u", "--url", type=str, help="site url to parse, ignored if file specified")
group.add_argument("-f", "--file", type=str, help="source file with links, one per line")

parser.add_argument("-s", "--span", type=int, default=0, help="time-span to flash-back date of the application")

args = parser.parse_args()
inter = args.inter
url = args.url
file = args.file
span = args.span
if span < 0:
    span *= -1

res = []
if inter:
    while True:
        url = input('url сайта (https://habr.com/...): ')
        if not validators.url(url):
            not_valid_handler(url)
            continue
        print(parse_links([url])[0])
if url:
    if not validators.url(url):
        not_valid_handler(url)
    else:
        res = parse_links([url])
if file:
    with open(file, 'r') as f:
        urls = [row.strip() for row in f]
        urls = filter(valid_filter, urls)
        res = parse_links(urls)

print("\033[32mResult: \033[0m")
for line in res:
    print(line)
