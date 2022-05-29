from time import sleep

import requests
from lxml import etree
import argparse
from datetime import date


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


def parse_link(url: str):
    headers = {'Content-Type': 'text/html'}
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    return format_response(url, get_title(html))


parser = argparse.ArgumentParser(description='A tutorial of argparse!')
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--inter", type=bool, help="turns on interactive mode, type 'inter True' to start it")
group.add_argument("--url", type=str, help="site url to parse, ignored if file specified")
group.add_argument("--file", type=str, help="source file with links, one per line")

args = parser.parse_args()
inter = args.inter
url = args.url
file = args.file

print('Inter: ', inter)
print('Link: ', url)
print('File: ', file)

if inter:
    while True:
        url = input('url сайта (https://habr.com/...)')
        print(parse_link(url))
if url:
    print(parse_link(url))
if file:
    with open(file, 'r') as f:
        for line in f:
            print(parse_link(line))

