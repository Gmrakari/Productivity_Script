#!/bin/bash
# 2023-03-27
# mqtt 模拟发送消息测试

usage() {
  echo "Usage: $0 [-h] -H <host> -M <mac> [-u <user>] [-p <password>] -T <type> -I <item> -C <cmd>"
  echo "Send a message to MQTT broker"
  echo ""
  echo "Options:"
  echo "  -h, --help         Show this help message and exit"
  echo "  -H, --host <host>  MQTT broker host"
  echo "  -M, --mac <mac>    MAC address of the device"
  echo "  -u, --user <user>  MQTT broker username"
  echo "  -p, --pass <pass>  MQTT broker password"
  echo "  -T, --type <type>  Type of the message"
  echo "  -I, --item <item>  Item of the message"
  echo "  -C, --cmd <cmd>    Command of the message"
  echo ""
  echo "Usage case:"
  echo " $BASH_SOURCE -H 192.168.1.1 -M 18:6f:d3:2a:cf:0e -u root -p passwd -T auth -I person -C sync"
}

# 支持的选项,h--help, H--host, M--mac, u--user, p--passwd, T--type, T--item, C--cmd
while getopts ":hH:M:u:p:T:I:C:" opt; do
  case ${opt} in
    h )
      usage
      exit 0
      ;;
    H )
      host=${OPTARG}
      ;;
    M )
      mac=${OPTARG}
      ;;
    u )
      user=${OPTARG}
      ;;
    p )
      passwd=${OPTARG}
      ;;
    T )
      type=${OPTARG}
      ;;
    I )
      item=${OPTARG}
      ;;
    C )
      cmd=${OPTARG}
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      usage
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." 1>&2
      usage
      exit 1
      ;;
  esac
done

# 检查入参
if [ -z "${host}" ] || [ -z "${mac}" ] || [ -z "${type}" ] || [ -z "${item}" ] || [ -z "${cmd}" ]; then
  echo "Error: missing required arguments." 1>&2
  usage
  exit 1
fi

topic="/808/device/${mac}"
message="{\"src\":\"server\",\"dst\":\"${mac}\",\"tick\":\"$(date +%s)\",\"status\":\"send\",\"type\":\"${type}\",\"item\":\"${item}\",\"cmd\":\"${cmd}\",\"args\":0}"

# 如果没有使用user和passwd将采用匿名的方式发送消息
if [ -n "${user}" ] && [ -n "${passwd}" ]; then
  mosquitto_pub -h "${host}" -t "${topic}" -u "${user}" -P "${passwd}" -m "${message}"
else
  mosquitto_pub -h "${host}" -t "${topic}" -m "${message}"
fi

