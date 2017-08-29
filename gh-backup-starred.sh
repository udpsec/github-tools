#!/bin/bash
 
user="CHANGEME"
pages=$(curl -I https://api.github.com/users/$user/starred | sed -nr 's/^Link:.*page=([0-9]+).*/\1/p')

for page in $(seq 0 $pages); do
    curl "https://api.github.com/users/$user/starred?page=$page&per_page=100" | jq -r '.[].html_url' |
    while read rp; do
      git clone $rp
    done
done