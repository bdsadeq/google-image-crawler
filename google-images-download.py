
import time
import sys
import os

import urllib.request

search_keyword = ['Australia']

keywords = ['high resolution']


def download_page(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(str(e))


def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line+1)
        end_content = s.find(',"ow"', start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)
            time.sleep(0.1)
            page = page[end_content:]
    return items


def main(search_keyword):
    t0 = time.time()  # start the timer
    i = 0

    items = []
    iteration = "Item no.: " + \
        str(i+1) + " -->" + " Item name = " + str(search_keyword)
    print(iteration)
    print("Evaluating...")
    search_keywords = search_keyword
    search = search_keywords.replace(' ', '%20')

    try:
        os.makedirs(search_keywords)
    except:
        pass

    j = 0
    while j < len(keywords):
        pure_keyword = keywords[j].replace(' ', '%20')
        url = 'https://www.google.com/search?q=' + search + pure_keyword + \
            '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html = (download_page(url))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        j = j + 1

    print("Total Image Links = "+str(len(items)))
    print("\n")

    info = open(str(search_keyword) + '.txt', 'a')
    info.write(str(i) + ': ' + str(search_keyword) +
               ": " + str(items) + "\n\n\n")
    info.close()

    t1 = time.time()
    total_time = t1-t0
    print("Total time taken: "+str(total_time)+" Seconds")
    print("Starting Download...")

    k = 0
    errorCount = 0
    while(k < len(items)):
        try:
            req = urllib.request.Request(items[k], headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urllib.request.urlopen(req, None, 15)
            output_file = open(search_keywords+"/"+str(k+1)+".jpg", 'wb')

            data = response.read()
            output_file.write(data)
            response.close()

            print(str(k+1) + ". Downloaded")

        except:
            print(str(k+1) + ". Problem Downloading")
        k = k+1

    print("\n")
    print("Everything downloaded!")
    print("\n"+str(errorCount)+" ----> total Errors")


if __name__ == "__main__":
    main(sys.argv[1])
