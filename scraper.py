from bs4 import BeautifulSoup as bs
import requests
import pprint


res1 = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

hn_resources = res1.text + res2.text

soup = bs(hn_resources, 'html.parser')

links = soup.select('.titlelink')
subtext = soup.select('.subtext')


def sort_by_votes(hn_list):
    return sorted(hn_list, key=lambda k: k['score'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []

    for idx, item in enumerate(links):
        title = item.getText()
        link = item.get('href', None)
        has_score = subtext[idx].select('.score')

        if has_score:
            score = int(has_score[0].getText().replace(' points', ''))
            if score >= 100:
                hn.append({'title': title, 'link': link, 'score': score})
    return hn


filtered_hn = create_custom_hn(links, subtext)

pprint.pprint(sort_by_votes(filtered_hn))
