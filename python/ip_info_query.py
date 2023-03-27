/* 
 * @filename: ip_info_query.py
 * @function: ip_info_query
 * @return: null
 * @author: gmrakari
 * @date: 2023/3/19 01:54
 * 
 */

import requests
import re
import pandas as pd

def _get_ip_list(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        ip_list = []
        for line in lines:
            match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if match:
                ip_list.append(match.group())
    return ip_list

def _ip_info(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    try:
        data = response.json()
    except:
        return None
    if data['status'] == 'success':
        return {'ip_address': ip_address, 'city': data['city']}
    else:
        return None

def _data_output():
    get_ip_list = _get_ip_list('ip_addr.txt')
    ip_data_list = []
    for ip_address in get_ip_list:
        ip_data = _ip_info(ip_address)
        if ip_data is not None:
            ip_data_list.append({'ip_address': ip_address, 'city': ip_data['city']})
    # 将列表转换为DataFrame
    df = pd.DataFrame(ip_data_list)
    # 将DataFrame写入Excel文件
    df.to_excel('ip_data.xlsx', index=False)

if __name__ == '__main__':
    _data_output()

