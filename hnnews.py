import sys
from bs4 import BeautifulSoup as bs
import requests
import pprint


def get_hn_resources(num_of_pages):
    hn_res = ''

    for x in range(num_of_pages):
        res = requests.get(f'https://news.ycombinator.com/news?p={x}')

        hn_res += res.text

    return hn_res


def sort_by_votes(hn_list):
    return sorted(hn_list, key=lambda k: k['score'], reverse=True)


def create_custom_hn(links, subtext, num_of_votes):
    hn = []

    for idx, item in enumerate(links):
        title = item.getText()
        link = item.get('href', None)
        has_score = subtext[idx].select('.score')

        if has_score:
            score = int(has_score[0].getText().replace(' points', ''))
            if score >= num_of_votes:
                hn.append({'title': title, 'link': link, 'score': score})
    return hn


num_of_pages = int(sys.argv[1])
num_of_votes = int(sys.argv[2])

hn_resources = get_hn_resources(num_of_pages)

soup = bs(hn_resources, 'html.parser')

links = soup.select('.titlelink')
subtext = soup.select('.subtext')


filtered_hn = create_custom_hn(links, subtext, num_of_votes)

pprint.pprint(sort_by_votes(filtered_hn))
