#!/bin/bash
##function : search code
##params   : need to search string

if [ $# -lt 1 ]; then
   echo "Usage: $0 待搜索代码"
   echo "eg   : $0 \"libface_hmod\" -A3 -E"
   exit 0
fi

str=$1
shift

path="/home/gmrakari/gitlab"

grep $* "$str" -nR $path --col

#grep $* "libface_hmod" -nR /home/app/gitlab/MF_SDK_v83x/ --col
