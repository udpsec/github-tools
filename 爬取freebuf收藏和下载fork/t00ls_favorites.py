import requests
import re
from bs4 import BeautifulSoup
import urllib
import os
def favorites(start_url):
    global headers
    headers = {'Cookie':'Cookie'}
    start_get = requests.get(start_url,headers=headers)
    # soup = BeautifulSoup(start_get.content,'html.parser')
    # body = soup.find_all(cellpadding="0")[0]
    # for a in body.find_all("a"):
        # global favorites_url
        # favorites_url = a.get("href")
        # if 'viewthread.php' in favorites_url:
            # print favorites_url
			
            # articles()
    regex = "\<th\>\<a href\=\"(.*?)\" target\="
    # print start_get.content.decode('utf-8')
    key = re.findall(regex,start_get.content)
    global k
    for k in key:
        print k
        articles()
	
	
def articles():
    url = "https://www.t00ls.net/"
    articles_url = url + k
    articles_get = requests.get(articles_url,headers=headers)
    soup = BeautifulSoup(articles_get.content,'html.parser')
    body = soup.find_all(class_="postmessage")[0]
    # print body.encode('gbk')
    print soup.title.text.encode('gbk')
    try:
        if os.path.exists(soup.title.text.encode('gbk') + '.html') == False:
            save = open(soup.title.text.encode('gbk') + ".html","w+")
            print>>save,body
            # img_regex = "<img src=\"(.*?)\" file=\"(.*?)\""
            # img = re.findall(img_regex,articles_get.content)
            # for i in img:
                # print i[1]
                # img_url = url + i[1]
                # print img_url
                # urllib.urlretrieve(img_url,'1.jpg')
    except:
            # if os.path.exists(str(shuzi) + '.html') == False:
            save = open(str(shuzi) + ".html", "w+")
            print>> save, body
            shuzi+=1

	
	
	
	
	
	
	
	
	
	
if __name__ == '__main__':
    pages = range(1,18)
    for pa in pages:
        favorites('https://www.t00ls.net/my.php?item=favorites&type=thread&page=' + str(pa))
