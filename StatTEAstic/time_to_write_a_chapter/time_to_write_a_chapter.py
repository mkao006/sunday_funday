from lxml import html
import requests
import urllib2
import re
from datetime import datetime


def extract_time_stamp(string):
    time_stamp_char = re.search("[0-9]{4}\-[0-9]+\-[0-9]+.[0-9]{2}:[0-9]{2}", 
                           string).group()
    time_stamp = datetime.strptime(time_stamp_char, '%Y-%m-%d %H:%M')
    return(time_stamp)

def get_post_time_stamps(page):
    ## This is required to read the protected page.
    ##
    ## Source:
    ## http://stackoverflow.com/questions/3336549/pythons-urllib2-why-do-i-get-error-403-when-i-urlopen-a-wikipedia-page
    ##
    ## NOTE (Michael): Some times the connection breaks, so we have to
    ##                 catch the error until it successed.
    while True:
        try:
            req = urllib2.Request(page, headers={'User-Agent' : "Magic Browser"}) 
            response = urllib2.urlopen(req)
            tree = html.fromstring(response.read())
            post_time_stamps = tree.xpath('//span[@class="postDateLine"]/text()')
            extracted_time_stamps = [extract_time_stamp(post_time_stamp) for
                                     post_time_stamp in post_time_stamps]
            return(extracted_time_stamps)
        except urllib2.HTTPError:
            continue
        break

def get_max_page_num(url):
    while True:
        try:
            req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
            response = urllib2.urlopen(req)
            tree = html.fromstring(response.read())
            last_page = int(re.sub("[^0-9]", "", 
                                   tree.xpath('//a[@class="last"]/text()')[0]))
            return(last_page)
        except urllib2.HTTPError:
            continue
        break


def get_catino_thread_time_stamps(thread):
    time_stamps = []
    url = 'http://ck101.com/thread-' + thread + '-%s-1.html'
    current_last_page = get_max_page_num(url % ('1'))
    for i in range(1, current_last_page + 1):
        current_link = url % (str(i))
        print("Extracting page " + str(i) + " from " + current_link)
        time_stamps.extend(get_post_time_stamps(current_link))
    return(time_stamps)


def calculate_hour_diff(time_stamps):
    ## Calculate time difference from first point
    time_diff = [new - old for (new, old) in 
                 zip(time_stamps[1:], time_stamps[:-1])]
    hour_diff = [time.days * 24 + time.seconds/60/60 for time in time_diff]
    return(hour_diff)




## Current novel in the serie
da_zhu_zai_time_stamp = get_catino_thread_time_stamps('2762483')
da_zhu_zai_time_diff = calculate_hour_diff(da_zhu_zai_time_stamp)

## Plot the differenced time series
import matplotlib.pyplot as plt
plt.plot(range(len(da_zhu_zai_time_diff)), da_zhu_zai_time_diff)
plt.show()


## First in the serie
do_puo_time_stamp = get_catino_thread_time_stamps('1455308')
do_puo_time_diff = calculate_hour_diff(do_puo_time_stamp)
## Delete those updates that are longer to 1 month, this is due to the
## special chapters. Further, as this was the first book in the
## series, it was not frequently updated due to low repulation.
do_puo_time_diff = [entry for entry in do_puo_time_diff if entry < 720]

## Plot the differenced time series
import matplotlib.pyplot as plt
plt.plot(range(len(do_puo_time_diff)), do_puo_time_diff)
plt.show()

## Second in the serie
wu_dong_time_stamp = get_catino_thread_time_stamps('1979168')
wu_dong_time_diff = calculate_hour_diff(wu_dong_time_stamp)

## Plot the differenced time series
import matplotlib.pyplot as plt
plt.plot(range(len(wu_dong_time_diff)), wu_dong_time_diff)
plt.show()

full_series_time_diff = do_puo_time_diff + wu_dong_time_diff + da_zhu_zai_time_diff
import matplotlib.pyplot as plt
plt.plot(range(len(full_series_time_diff)), full_series_time_diff)
plt.show()
