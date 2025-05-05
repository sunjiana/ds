import time
import datetime
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
import threading
from queue import Queue
import eventlet
eventlet.monkey_patch()

urls = [
"https://60.16.18.243:4949",
"https://175.190.127.179:4949",
"https://36.129.204.120:8083",
"https://119.119.65.25:808",
"https://119.119.84.255:808 ",
"https://119.116.120.242:8888",
"https://113.228.41.153:8888",
"https://116.138.153.5:88",
"https://175.146.22.40:88",
"https://175.146.20.89:88",
"https://175.146.17.20:88",
"https://175.167.14.248:88",
"https://60.17.196.134:88",
"https://60.17.181.1:88",
"https://175.167.13.176:88",
"https://123.189.50.71:88",
"https://123.189.53.191:88",
"https://124.94.226.80:88",
"https://60.17.190.207:88",
"https://60.19.183.64:88",
"https://175.167.13.153:88",
"https://119.116.46.63:88",
"https://60.22.88.3:8002",
"https://123.244.72.23:808",
"https://123.244.72.20:808",
"https://123.244.72.114:808",
"https://123.244.72.129:808",
"https://123.244.72.73:808",
"https://123.244.72.100:808",
"https://123.244.72.106:808",
"https://123.244.72.85:808",
"https://123.244.72.86:808",
"https://123.244.72.55:808",
"https://123.244.72.92:808",
"https://123.244.72.126:808",
"https://123.244.72.123:808",
"https://123.244.72.115:808",
"https://123.244.72.124:808",
"https://123.244.72.38:808",
"https://123.244.72.43:808",
"https://123.244.72.39:808",
"https://175.170.20.218:808",
"https://42.84.22.79:808",
"https://113.235.206.84:808",
"https://42.84.212.167:771",
"https://42.84.222.67:771",
"https://60.20.70.252:808",
"https://119.113.105.187:808",
"https://113.234.63.69:808",
"https://175.163.61.148:808",
"https://119.113.248.176:808",
"https://60.20.83.121:808",
"https://175.163.36.175:808",
"https://36.129.204.120:8082",
"https://42.178.94.99:808",
"https://42.57.193.104:808",
"https://42.86.143.179:808",
"https://119.116.147.35:808",
"https://42.56.217.161:808",
"https://42.57.204.5:808",
"https://113.228.76.52:808",
"https://42.57.199.54:808",
"https://124.95.7.5:808",
"https://42.55.223.22:808",
"https://175.151.83.30:808",
"https://42.55.223.143:808",
"https://42.5.236.172:808",
"https://42.55.223.217:808",
"https://42.55.223.243:808",
"https://42.58.222.194:808",
"https://42.55.222.223:808",
"https://42.55.222.203:808",
"https://42.55.222.214:808",
"https://175.175.166.190:808",
"https://175.175.164.121:808",
"https://42.58.222.54:808",
"https://175.151.82.92:808",
"https://42.178.53.24:808",
"https://42.178.89.169:808",
"https://124.95.14.74:808",
"https://124.95.29.178:808",
"https://113.239.107.230:808",
"https://42.55.216.220:808",
"https://42.55.217.187:808",
"https://175.175.171.224:808",
"https://175.175.186.179:808",
"https://42.5.237.58:808",
"https://42.5.239.197:808",
"https://42.5.237.58:808",
"https://42.5.239.197:808",
"https://42.4.96.42:808",
"https://42.57.198.240:808",
"https://42.55.218.13:808",
"https://42.55.218.95:808",
"https://42.57.199.174:808",
"https://42.55.223.90:808",
"https://42.57.198.50:808",
"https://42.5.239.130:808",
"https://42.58.223.172:808",
"https://42.52.28.187:808",
"https://42.58.223.190:808",
"https://113.231.117.20:808",
"https://42.55.216.87:808",
"https://113.231.109.187:808",
"https://175.151.82.165:808",
"https://42.57.193.131:808",
"https://113.45.171.28:465",
"https://8.130.21.200:880",
"https://103.72.172.253:8040",
"https://81.70.248.163:8888",
"https://47.93.113.151:80",
"https://49.7.234.13:808",
"https://49.7.234.2:808",
"https://49.7.234.98:808",
"https://49.7.234.2:80",
"https://49.7.234.98:80",
"https://49.7.234.13:80",
"https://123.118.156.146:8888",
"https://114.253.72.39:8888",
"https://123.121.85.12:8888",
"https://114.243.181.154:8089",
"https://49.7.234.13:8888",
"https://114.251.13.196:443",
"https://114.251.13.203:443",
"https://114.251.13.196:80",
"https://123.114.209.150:8089",
"https://120.244.126.209:8089",
"https://120.244.126.241:8089",
"https://49.7.234.3:80",
"https://1.203.120.115:8089",
"https://49.7.234.5:80",
"https://101.254.208.170:80",
"https://101.254.185.170:80",
"https://101.254.208.174:80",
"https://101.254.185.171:80",
"https://101.19.151.139:808",
"https://101.19.151.161:808",
"https://101.19.150.20:808",
"https://101.19.151.71:808",
"https://101.19.149.191:808",
"https://101.19.149.140:808",
"https://101.19.151.157:808",
"https://101.19.151.62:808",
"https://101.19.151.194:808",
"https://101.19.149.91:808",
"https://101.19.148.235:808",
"https://101.19.150.42:808",
"https://101.19.151.170:808",
"https://101.19.151.167:808",
"https://101.19.151.111:808",
"https://101.19.150.237:808",
"https://101.19.148.207:808",
"https://101.19.149.144:808",
"https://101.19.150.131:808",
"https://101.19.151.12:808",
"https://101.19.151.12:808",
"https://101.19.151.193:808",
"https://101.19.148.97:808",
"https://101.19.151.155:808",
"https://101.19.148.127:808",
"https://101.19.149.168:808",
"https://101.19.151.11:808",
"https://101.19.150.4:808",
"https://101.19.149.224:808",
"https://101.19.151.87:808",
"https://101.19.149.172:808",
"https://101.19.148.19:808",
"https://101.19.149.170:808",
"https://101.19.149.155:808",
"https://101.19.148.8:808",
"https://101.19.149.75:808",
"https://101.19.151.169:808",
"https://101.19.150.216:808",
"https://101.19.151.155:808",
"https://101.19.150.178:808",
"https://101.18.25.106:808",
"https://101.19.148.244:808",
"https://101.19.149.203:808",
"https://101.19.150.62:808",
"https://101.19.148.237:808",
"https://101.19.148.53:808",
"https://101.19.151.250:808",
"https://101.19.149.139:808",
"https://101.19.149.85:808",
"https://101.19.148.119:808",
"https://101.26.42.41:808",
"https://101.26.42.86:808",
"https://101.26.42.250:808",
"https://183.196.87.176:880",
"https://106.115.24.169:8088",
"https://101.23.216.69:8090",
"https://106.117.129.245:808",
"https://121.24.98.238:8090",
"https://121.24.99.25:8090",
"https://121.24.99.169:8090",
"https://121.24.99.41:8090",
"https://121.24.98.232:8090",
"https://121.24.99.190:8090",
"https://121.24.98.151:8090",
"https://121.24.99.44:8090",
"https://121.24.98.250:8090",
"https://121.24.99.99:8090",
"https://121.24.99.213:8090",
"https://123.181.1.172:808",
"https://121.24.98.236:8090",
"https://121.24.99.131:8090",
"https://121.24.98.226:8090",
"https://121.24.98.15:8090",
"https://121.24.98.40:8090",
"https://121.24.98.184:8090",
"https://121.24.98.96:8090",
"https://121.24.98.139:8090",
"https://121.24.99.229:8090",
"https://121.24.98.102:8090",
"https://121.24.98.229:8090",
"https://121.24.98.106:8090",
"https://121.24.98.136:8090",
"https://121.24.99.68:8090",
"https://121.24.99.10:8090",
"https://121.24.98.79:8090",
"https://121.24.99.239:8090",
"https://121.24.98.85:8090",
"https://121.24.98.252:8090",
"https://121.24.98.100:8090",
"https://121.24.99.197:8090",
"https://121.24.98.134:8090",
"https://121.24.98.123:8090",
"https://121.24.98.224:8090",
"https://121.24.99.181:8090",
"https://121.24.98.66:8090",
"https://121.24.98.55:8090",
"https://121.24.98.182:8090",
"https://121.24.99.226:8090",
"https://106.117.130.11:808",
"https://106.117.134.232:808",
    ]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls


def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


results = []

x_urls = []
for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
    url = url.strip()
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    ip_dot_start = url.find(".") + 1
    ip_dot_second = url.find(".", ip_dot_start) + 1
    ip_dot_three = url.find(".", ip_dot_second) + 1
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_dot_three]
    port = url[ip_end_index:]
    ip_end = "1"
    modified_ip = f"{ip_address}{ip_end}"
    x_url = f"{base_url}{modified_ip}{port}"
    x_urls.append(x_url)
urls = set(x_urls)  # 去重得到唯一的URL列表

valid_urls = []
#   多线程获取可用url
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for url in urls:
        url = url.strip()
        modified_urls = modify_urls(url)
        for modified_url in modified_urls:
            futures.append(executor.submit(is_url_accessible, modified_url))

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            valid_urls.append(result)

for url in valid_urls:
    print(url)
    
now_today = datetime.date.today()
with open("ip.txt", 'a', encoding='utf-8') as file:
    file.write(f"{now_today}更新\n")
    for url in valid_urls:
        file.write(url + "\n")
        
# 遍历网址列表，获取JSON文件并解析
for url in valid_urls:
    try:
        # 发送GET请求获取JSON文件，设置超时时间为0.5秒
        ip_start_index = url.find("//") + 2
        ip_dot_start = url.find(".") + 1
        ip_index_second = url.find("/", ip_dot_start)
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_index_second]
        url_x = f"{base_url}{ip_address}"

        json_url = f"{url}"
        response = requests.get(json_url, timeout=0.5)
        json_data = response.json()

        try:
            # 解析JSON文件，获取name和url字段
            for item in json_data['data']:
                if isinstance(item, dict):
                    name = item.get('name')
                    urlx = item.get('url')
                    if ',' in urlx:
                        urlx=f"aaaaaaaa"
                    #if 'http' in urlx or 'udp' in urlx or 'rtp' in urlx:
                    if 'http' in urlx:
                        urld = f"{urlx}"
                    else:
                        urld = f"{url_x}{urlx}"

                    if name and urlx:
                        # 删除特定文字
                        name = name.replace("cctv", "CCTV")
                        name = name.replace("中央", "CCTV")
                        name = name.replace("央视", "CCTV")
                        name = name.replace("高清", "")
                        name = name.replace("超高", "")
                        name = name.replace("HD", "")
                        name = name.replace("标清", "")
                        name = name.replace("频道", "")
                        name = name.replace("-", "")
                        name = name.replace(" ", "")
                        name = name.replace("PLUS", "+")
                        name = name.replace("＋", "+")
                        name = name.replace("(", "")
                        name = name.replace(")", "")
                        name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                        name = name.replace("CCTV1综合", "CCTV1")
                        name = name.replace("CCTV2财经", "CCTV2")
                        name = name.replace("CCTV3综艺", "CCTV3")
                        name = name.replace("CCTV4国际", "CCTV4")
                        name = name.replace("CCTV4中文国际", "CCTV4")
                        name = name.replace("CCTV4欧洲", "CCTV4")
                        name = name.replace("CCTV5体育", "CCTV5")
                        name = name.replace("CCTV6电影", "CCTV6")
                        name = name.replace("CCTV7军事", "CCTV7")
                        name = name.replace("CCTV7军农", "CCTV7")
                        name = name.replace("CCTV7农业", "CCTV7")
                        name = name.replace("CCTV7国防军事", "CCTV7")
                        name = name.replace("CCTV8电视剧", "CCTV8")
                        name = name.replace("CCTV9记录", "CCTV9")
                        name = name.replace("CCTV9纪录", "CCTV9")
                        name = name.replace("CCTV10科教", "CCTV10")
                        name = name.replace("CCTV11戏曲", "CCTV11")
                        name = name.replace("CCTV12社会与法", "CCTV12")
                        name = name.replace("CCTV13新闻", "CCTV13")
                        name = name.replace("CCTV新闻", "CCTV13")
                        name = name.replace("CCTV14少儿", "CCTV14")
                        name = name.replace("CCTV15音乐", "CCTV15")
                        name = name.replace("CCTV16奥林匹克", "CCTV16")
                        name = name.replace("CCTV17农业农村", "CCTV17")
                        name = name.replace("CCTV17农业", "CCTV17")
                        name = name.replace("CCTV5+体育赛视", "CCTV5+")
                        name = name.replace("CCTV5+体育赛事", "CCTV5+")
                        name = name.replace("CCTV5+体育", "CCTV5+")
                        results.append(f"{name},{urld}")
        except:
            continue
    except:
        continue


channels = []

for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',')
        channels.append((channel_name, channel_url))
    print(result)
with open("tvlist.txt", 'w', encoding='utf-8') as file:
    for result in results:
        if result:
            file.write(result + "\n")
