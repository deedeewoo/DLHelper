# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import requests
from lxml import html
import sys
import optparse
import csv
reload(sys)
sys.setdefaultencoding('utf8')

# driver = webdriver.Firefox()
# driver.get(home)
# elem = driver.find_element_by_class_name("keywords")
# elem.send_keys('modern family', Keys.RETURN)
# search_results = driver.find_element_by_css_selector('h2.it')
# results = search_results.find_element_by_tag_name('span').text


def get_links(url):
    urls = []
    r = requests.get(url)
    tree = html.fromstring(r.text)
    results = tree.xpath('//li[@class="clearfix"]')
    # results = tree.cssselect('li.clearfix')
    home = "http://btdd.me"
    for i in results:
        link = i.xpath('.//div[@class="fl url"]/a/@href')
        link_url = home + link[0]
        urls.append(link_url)
    return urls

# function to return a list of pages urls


def search_results(keywords):
    home = "http://btdd.me"
    join_key = '+'
    search_url = home + '/?k=' + join_key.join(keywords.split())

    r = requests.get(search_url)
    tree = html.fromstring(r.text)
    res_element = tree.xpath('//h2[@class="it"]/span/text()')
    results_str = res_element[0]
    ss = results_str.rfind('(')
    ee = results_str.rfind(")")
    total = results_str[ss + 1:ee]

    result_this_page = tree.xpath('//li[@class="clearfix"]')
    no_per_page = len(result_this_page)

    page_link = []

    if int(total) == 0:
        return page_link
    else:
        for i in result_this_page:
            link = i.xpath('.//div[@class="fl url"]/a/@href')
            link_url = home + link[0]
            page_link.append(link_url)

        page_count = int(total) // no_per_page + (int(total) % no_per_page > 0)

        if page_count == 1:
            return page_link
        else:
            next_page = home + '/index/index' + \
                '/k/' + join_key.join(keywords.split())
            for i in range(2, page_count + 1):
                url = next_page + '/p/' + str(i)
                page_link2 = get_links(url)
                page_link.extend(page_link2)
            return page_link

# give a url, return a list of id, file name and download link


def get_dl_link(url_list):
    dl_list = []
    if len(url_list) == 0:
        return dl_list
    else:
        for u in url_list:
            r = requests.get(u)
            tree = html.fromstring(r.text)
            dl_sec = tree.xpath('//dl[@class="download-links"]//a/@href')
            dl_url = dl_sec[0]
            file_info = tree.xpath('//span[@class="fn"]/text()')
            file_name = file_info[0].strip()
            dl_list.append([file_name, dl_url])
        return dl_list


def main():
    parser = optparse.OptionParser()
    parser.add_option('-k', '--keywords', dest='key', type='string',
                      action='store', help='Type what you want to download')
    (opts, args) = parser.parse_args()
    if opts.key is None:
        print 'Keywords needed'
        exit(0)
    else:
        target = opts.key
        links = search_results(target)
        movies = get_dl_link(links)
        csv_name = target + '.csv'
        writer = csv.writer(open(csv_name, 'a'))
        for i in movies:
            writer.writerow(i)

if __name__ == '__main__':
    main()
