#!/bin/bash
# gen llvn-objdump file

if [ $# -eq 0 ]; then
  echo "请指定错误类型参数，例如：$0 lv_err"
  exit 1
fi

cd /home/gmrakari/gitlab/bl808/bl_iot_sdk/customer_app/bl808_demo_c906/build_out

elf=bl808_demo_c906.elf

filename="device_$1_$(date +'%m-%d_%H_%M').asm"

llvm-objdump -S $elf > $filename

echo "生成了文件: $filename" 
