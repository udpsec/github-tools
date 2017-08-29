#!/usr/bin/env python
import urllib2, json, os, subprocess

# Simple script to git clone each project starred by a user.
# /!\ There is an API rate limit. To increase it, authenticated actions are needed -_-
# http://developer.github.com/v3/#rate-limiting

user = "steeve85"
i = 1 
json_data = None

while json_data != []: 
  json_data = json.loads(urllib2.urlopen("https://api.github.com/users/%s/starred?page=%i" % (user, i)).read())
  for j in range(30):
    try:
      print "Cloning %s" % json_data[j]["full_name"]
      print "\t\t %s" % json_data[j]["description"]
      if os.path.exists(json_data[j]["name"]):
        subprocess.call('cd %s; git pull --recurse-submodules; cd -' % json_data[j]["name"], shell=True)
      else:
        subprocess.call(['git', 'clone', '--recurse-submodules', json_data[j]["clone_url"]])
    except IndexError:
      print "End of starred projects"
      exit(0)
  i+=1
