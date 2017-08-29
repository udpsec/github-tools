#!/bin/bash

if [ $# -eq 0 ]; then
	echo "$(basename $0) USER"
	exit
fi

curl "https://api.github.com/users/$1/starred" | awk '/^\s+"git_url"/ && $0 = $4' FS='"' | xargs -I {} git clone {}