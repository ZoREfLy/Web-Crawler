import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        html = requests.get(url, timeout=30)
        html.raise_for_status()
        html.encoding = ('utf-8')
        return html.text
    except:
        return 'Something is wrong!'


def get_chapters_link(url):
    # create a list to save all links
    link_list = set()

    # save html to local
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    chapter_link_list = soup.find_all('div', attrs={'class': 'articleCell SG_j_linedot1'})

    for chapter_link in chapter_link_list:
        link = chapter_link.find('span', attrs={'class': 'atc_title'}).a.attrs['href']
        link_list.add(link)
    return link_list


def get_all_chapter(url_list):
    print("Opening url...")
    for url in url_list:
        print("url is opened!")
        download_chapter(url)


def download_chapter(url):
    try:
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        print("Searching for title...")
        title = soup.find('div', attrs={'class': 'articalTitle'}).h2.text
        print("Title is found!\nSearching for content")
        text = soup.find('div', id='sina_keyword_ad_area2').text
        print("Content of is found!")

        with open('{}.text'.format(title), 'a+', encoding='utf-8') as f:
            f.write(text)
        print("Finish downloading!")
    except:
        print("Something is wrong!")


def main():
    base_url = 'http://blog.sina.com.cn/s/articlelist_1776670784_5_1.html'
    print("Downloading all url to local...")
    url_list = list(get_chapters_link(base_url))
    print("All urls are saved!")
    get_all_chapter(url_list)
    print("Starting open urls...")


if __name__ == '__main__':
    main()