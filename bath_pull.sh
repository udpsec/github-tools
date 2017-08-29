#!/bin/sh
for dir in $(ls -d */)
do {
    gitrepo=$(basename $dir)
    gitname=${gitrepo%.*}
    echo git pulliing $gitname...
    cd $dir && git pull && cd ..
}&
done
find . -maxdepth 1 -type d -exec sh -c '(cd {} && git pull)' ';'
DOSKEY gitup=D:\develop_tools\Python27\python.exe D:\develop_tools\Python27\Scripts\gitup $*