#!/bin/bash

DATE=`date +%F`
DIR='backup-'$DATE

mkdir $DIR

mv *.zip ./$DIR/

WGET='wget --content-disposition'

# User epositories
#REPOS=`curl -s https://api.github.com/users/chemel/repos | jq -r .[].html_url`

#for REPO in $REPOS
#do
#	$WGET $REPO/archive/master.zip
#done

# Starred repositories
REPOS=`curl -s https://api.github.com/users/chemel/starred | jq -r .[].html_url`

for REPO in $REPOS
do
	$WGET $REPO/archive/master.zip
done
