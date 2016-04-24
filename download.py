from bs4 import BeautifulSoup
import urllib2
import StringIO
import gzip
import os
import time

MANGA_FOX = 'http://mangafox.me/manga/doraemon/'


def get(url):
    headers = {'Referer': "http://mangafox.me/manga/doraemon/v12/c222/1.html",
               'User-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    req = urllib2.Request(url, headers=headers)
    res = urllib2.urlopen(req)
    html = res.read()
    if res.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        html = f.read()
    return html


def get_chlist(html):
    soup = BeautifulSoup(html, 'html.parser')
    chapter_html = soup.find("div", {"id": "chapters"})
    chlist = chapter_html.find_all('ul', {'class': 'chlist'})
    my_list = []
    for _list in chlist:
        li = _list.find_all('li')
        for html_li in li:
            href = html_li.find_all('a')[1].get('href')
            title = html_li.find_all('span')[2].text
            comic = (title, href)
            my_list.append(comic)
    return my_list


def get_comic_page(comic):
    title, href = comic
    folder = title.replace(' ', '_')
    if not os.path.isdir(folder):
        os.mkdir(folder)
        print 'Created %s' % folder
        html = get(href)
        soup = BeautifulSoup(html, 'html.parser')
        options = soup.find_all('option')
        total_pages = len(set(options)) - 1
        # Download page
        for i in range(1, total_pages + 1):
            file_name = "%s/%s.jpg" % (folder, i)
            if not os.path.exists(file_name):
                url = href.replace('1.html', str(i) + '.html')
                comic_html = get(url)
                soup2 = BeautifulSoup(comic_html, 'html.parser')
                read_img_div = soup2.find('div', {'class': 'read_img'})
                comic = read_img_div.find('img').get('src')
                try:
                    comic_file = get(comic)
                except:
                    comic = comic.replace(
                        'http://z.mfcdn.net', 'http://c.mfcdn.net')
                    try:
                        comic_file = get(comic)
                    except:
                        comic_file = None
                if comic_file:
                    f = open(file_name, 'wb')
                    f.write(comic_file)
                    f.close()
                    print 'Downloaded %s' % file_name
                time.sleep(1)
    else:
        print 'Existed %s' % folder

html = get(MANGA_FOX)
comics = get_chlist(html)
for comic in comics:
    get_comic_page(comic)
