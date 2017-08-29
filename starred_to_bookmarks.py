#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  starred_to_bookmarks.py
#  
#  Copyright 2013 Matthieu Baerts <matttbe _@_ mail -> google>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#  
#  ## How to use it? ##
#  Simply download this script and place your 'starred.json' file in the same directory.
#  Then launch it with this command:
#     $ python starred_to_bookmarks.py
#  
#  ## Notes ##
#  You can modify `bWithContent` to `False` to not add the content in the description and `iLimitContent`
#   to change the maximum number of characters that you want to have in this description.


import json

bWithContent = True
iLimitContent = 500
import re

def main():
	# open starred
	fIn = open ('starred.json', 'r', encoding='utf-8')
	jsonData = json.load(fIn)
	fIn.close()

	# output
	# header
	fOut = open ('starred.json.html', 'w', encoding='utf-8')
	fOut.write ('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
	fOut.write ('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
	mainTitle = jsonData["title"]
	fOut.write ('<TITLE>' + mainTitle + '</TITLE>\n')
	fOut.write ('<H1>' + mainTitle + '</H1>\n')

	# for each item: <DT><A HREF="URL" ADD_DATE="DATE" PRIVATE="1">TITLE</A>
	for item in jsonData["items"]:
		title = item["title"]
		origin = item["origin"]["title"]
		date = item["published"]
		url = item["alternate"][0]["href"]
		fOut.write ('<DT><A HREF="' + url + '" ADD_DATE="' + str (date) + '" PRIVATE="1" TAGS="' + origin.replace(' ', '-') + '">' + title + '</A>\n')
		if bWithContent:
			s = ""
			if "summary" in item:
				s = "summary"
			elif "content" in item:
				s = "content"
			if s:
				# remove html tag and replace <br> and </p> by new lines
				content = re.sub ('<[^<]+?>', '', re.sub('<br>|</p>|\n\n', '\n', item[s]["content"]))
				# remove blank lines
				content = re.sub ('(?imu)^\s*\n', '', content)
				if len (content) > iLimitContent:
					content = content[0:iLimitContent-3] + '...'
				fOut.write ('<DD>' + content + '\n')

	fOut.close()

	return 0

if __name__ == '__main__':
	main()
