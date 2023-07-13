
# transfer str to hex
#!/bin/bash

#hex_string="40 40 0D 00 27 94 82 00 56 30 2E 31 00"

hex_string=$1

# 将十六进制字符串拆分为单独的字节
hex_bytes=($hex_string)
length=${#hex_bytes[@]}

# 遍历每个字节，并添加0x前缀打印
for i in "${!hex_bytes[@]}";do
  byte=${hex_bytes[$i]}
  printf "0x%s" "$byte"
  if ((i != length - 1)); then
    printf ", "
  fi
done

echo ""  # 换行

