#!/bin/sh
for dir in $(ls -d */)
do
  cd $dir
  echo "into $dir"
  if [ -d ".git" ]; then
     git pull
  elif [ -d ".svn" ]; then
     svn update
  fi
  cd ..
done