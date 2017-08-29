#coding = utf-8
import requests
import re
import urllib
page = range(1,5)
github_username = raw_input('github_username:')
for pg in page:
	url = 'https://github.com/%s?page=%s&tab=repositories' %(github_username,pg)
	get = requests.get(url)
	regex = '\<a href=\"/(.*?)\" itemprop\=\"name codeRepository\"\>'
	key = re.findall(regex,get.content)
	for k in key:
		#print k
		url2 = 'https://github.com/'
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
