#coding = utf-8
import requests
import re
import urllib
page = range(1,5)
<strong><font color="#FF0000">github</font></strong>_username = raw_input('<strong><font color="#FF0000">github</font></strong>_username:')
for pg in page:
        url = 'https://<strong><font color="#FF0000">github</font></strong>.com/%s?page=%s&tab=repositories' %(<strong><font color="#FF0000">github</font></strong>_username,pg)
        get = requests.get(url)
        regex = '\<a href=\"/(.*?)\" itemprop\=\"name codeRepository\"\>'
        key = re.findall(regex,get.content)
        for k in key:
                #print k
                url2 = 'https://<strong><font color="#FF0000">github</font></strong>.com/'
                xiangmu_name = url2 + k
                print xiangmu_name
                url3 = '/archive/master.zip'
                download = xiangmu_name + url3
                print download
                filename = urllib.urlopen(download)
                info = filename.info()
                filename_regex = 'Content-Disposition: attachment; filename=(.*)'
                filename_down = re.findall(filename_regex,str(info))
                #print filename_down
                for filename1 in filename_down:
                        print filename1
                        filename2 = filename1.strip()
                        urllib.urlretrieve(download,filename2)