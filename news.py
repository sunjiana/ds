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
"http://110.40.43.24:5678",
"http://114.254.82.142:88",
"http://114.254.95.12:88",
"http://114.254.93.41:88",
"http://114.254.80.92:88",
"http://114.254.95.217:88",
"http://114.254.92.42:88",
"http://114.254.82.125:88",
"http://114.254.85.245:88",
"http://114.254.80.219:88",
"http://114.254.83.81:88",
"http://114.254.81.136:88",
"http://114.254.86.250:88",
"http://114.254.95.100:88",
"http://114.254.89.195:88",
"http://114.254.89.81:88",
"http://114.254.82.129:88",
"http://114.254.87.139:88",
"http://114.254.85.239:88",
"http://114.254.81.93:88",
"http://114.254.93.105:88",
"http://114.254.81.227:88",
"http://101.18.24.248:808",
"http://101.18.30.19:808",
"http://121.19.134.14:808",
"http://121.19.134.222:808",
"http://121.19.134.200:808",
"http://101.18.29.28:808",
"http://101.18.24.147:808",
"http://120.211.222.13:12345",
"http://121.19.134.139:808",
"http://101.72.127.38:808",
"http://121.19.134.227:808",
"http://111.225.112.50:808",
"http://124.238.110.12:9999",
"http://111.225.115.122:808",
"http://111.225.112.74:808",
"http://121.19.134.82:808",
"http://121.19.134.192:808",
"http://121.19.134.225:808",
"http://111.225.114.49:808",
"http://111.225.114.109:808",
"http://121.19.134.46:808",
"http://111.225.113.44:808",
"http://111.225.113.109:808",
"http://124.238.110.59:9999",
"http://111.225.113.171:808",
"http://111.225.115.193:808",
"http://123.183.26.57:6666",
"http://123.182.209.50:8088",
"http://124.238.110.101:9999",
"http://121.19.134.13:808",
"http://121.19.134.150:808",
"http://124.238.110.15:9999",
"http://121.19.134.142:808",
"http://121.19.134.140:808",
"http://124.238.110.130:9999",
"http://123.183.27.120:6666",
"http://123.182.212.170:8088",
"http://123.183.24.193:6666",
"http://123.182.215.248:8088",
"http://121.19.134.190:808",
"http://123.183.25.176:6666",
"http://124.238.110.140:9999",
"http://123.183.24.27:6666",
"http://123.182.208.248:8088",
"http://111.225.114.162:808",
"http://121.19.134.189:808",
"http://124.237.5.9:9999",
"http://123.183.26.233:6666",
"http://111.225.115.31:808",
"http://123.182.211.96:8088",
"http://122.138.32.222:9999",
"http://59.44.203.42:9901",
"http://218.24.43.46:9901",
"http://39.152.171.140:9901",
"http://119.114.235.30:9902",
"http://124.94.207.48:9902",
"http://175.148.29.98:9902",
"http://119.114.238.244:9902",
"http://175.190.127.180:9901 ",
"http://59.44.10.113:9901",
"http://39.152.170.32:9901",   
"http://60.22.88.3:8002",
"http://113.7.229.136:9000",
"http://122.159.168.193:9000",
"http://122.159.168.83:9000",
"http://1.188.69.150:9000",
"http://113.7.229.45:9000",
"http://112.103.141.253:8083",
"http://112.103.141.251:8083",
"http://112.103.141.109:8083",
"http://112.103.141.178:8083",
"http://112.103.141.250:8083",
"http://112.103.141.247:8083",
"http://112.103.141.68:8083",
"http://112.103.141.221:8083",
"http://112.103.141.174:8083",
"http://112.103.141.205:8083",
"http://112.103.141.191:8083",
"http://112.103.141.176:8083",
"http://112.103.141.188:8083",
"http://112.103.141.189:8083",
"http://113.7.229.136:9000",
"http://122.159.168.83:9000",
"http://1.188.69.150:9000",
"http://113.7.229.45:9000",


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
with open("news.txt", 'w', encoding='utf-8') as file:
    for result in results:
        if result:
            file.write(result + "\n")
