#coding = utf-8
import re,sys
import requests
import os
from bs4 import BeautifulSoup
import urllib
i = range(11)
shuzi = 1
for a in i:
	url = "http://www.freebuf.com/user/myfavorites/page/%s" %a
	headers = {"cookie":"zhelishicookie"}
	get1 = requests.get(url,headers=headers)
	regex = "\<a href=\'(.*?)\' title=\'(.*?)\'\>(.*?)\<\/a\>\<\/div\>"
	key = re.findall(regex,get1.content)
	try:
		for k in key:
			print get1.url
			print k[0]
			get2 = requests.get(k[0])
			print get2.url
			if os.path.exists(k[1].decode('utf-8') + '.html') ==False:
				print 'meiyou'*50
				bc = open(k[1].decode('utf-8') + '.html','w+')
				bc.write(get2.content)
				neirong2 = get2.content
				soup = BeautifulSoup(neirong2,from_encoding='gbk')
				img = soup.findAll('img')
				print img
				for m in img:
					g = m.get('src')
					print g
					try:
						
						imgg = g.split('/')[-1]
						print imgg	
						print 'a'*20
						local = os.path.join('images',imgg)
						urllib.urlretrieve(g,local)
					except:
						
						break

	except:
		for k in key:
			print get1.url
			print k[0]
			get2 = requests.get(k[0])
			print get2.url
			if os.path.exists(str(shuzi) + '.html') ==False:
				print 'meiyou'*50
				bc = open(str(shuzi) + '.html','w+')
				bc.write(get2.content)
				shuzi+=1
				print shuzi
				neirong2 = get2.content
				soup = BeautifulSoup(neirong2,from_encoding='gbk')
				img = soup.findAll('img')
				print img
				for m in img:
					g = m.get('src')
					print g
					try:
						
						imgg = g.split('/')[-1]
						print imgg	
						print 'a'*20
						local = os.path.join('images',imgg)
						urllib.urlretrieve(g,local)
					except:
					
						break



//爬取的是http://www.freebuf.com/user/myfavorites这里freebuf个人中心收藏的文章，如果你收藏的比较多，按需修改第七行代码处的“i = range(11)”。由于windows下文件名不能出现特殊符号，所以如果有特殊符号，则保存的文件名为数字.html。
如果不小心把爬取下载的窗口关了也没事，可重新运行，会判断文件是否存在，只会下载没下载过的。
图片没有分类，全部下载同一个目录里的，全部下载完了，记得把<img src>中的图片路径改成相对路径。
//遇到很多坑，比如首先cookie不一定是字典形式的，比如{'xxx':'xxx','aaaa':'bbbbb'},那样太累了，如果cookie N多，你把cookie抓下来，不得一个一个改成字典形式，得累死，那么可以像11行代码那样，利用headers头，headers = {"cookie":"zhelishicookie"},
这样的话，就可以把cookie一次性用引号引起来了。
//还有就是保存文件名中文的问题，本来想直接以数字.html来保存文件名，但是那样太不规范了，想找资料都不好找，但是以文件名作为文件名保存的话，中文又是乱码，后来用decode解决，在23行代码处，open(k[1].decode('utf-8') + '.html','w+')
//还有解析图片的问题，利用beautifulsoup可以解析出图片，但是有的图片是中文的，比如是QQ图片这样，图片这两个中文又是乱码，最后利用26行代码处soup = BeautifulSoup(neirong2,from_encoding='gbk')解决。
//最后下载图片，beautifulsoup解析出来的图片是这样的形式，http://www.baidu.com/images/20110111/xxxx.jpg，当初一直想用正则取出xxxx.jpg作为下载回来保存的文件名，一直用正则不行，后来发现可以用split切出来，在63行代码处，以“/”进行切割，然后取最后一一个值，imgg = g.split('/')[-1]
//利用os.path.join把图片全部下载到images文件夹中
