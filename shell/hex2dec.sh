#!/bin/bash
##function: 十六进制转成十进制
##author  : gmrakari
##connect : gmrakari@outlook.com
##params  : 待转换的十六进制数
##example:

if [ $# -lt 1 ]; then
    echo "Usage input you need to convert base16 number to base10"
    echo "eg : A" 
    echo "output 10"
    exit 0
fi
    echo "ibase = 16;$1" | bc

