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
"http://111.40.34.181:9902",
"http://112.99.193.34:9901",
"http://112.101.78.50:9901",
"http://222.169.85.8:9901",
"http://61.138.128.226:19901",
"http://58.245.255.34:9998",
"http://36.49.51.154:9902",
"http://119.48.202.89:9902",
"http://36.49.52.140:9902",
"http://124.234.179.254:9901",
"http://175.16.151.198:9901",
"http://119.50.5.156:9901",
"http://222.169.41.80:9901",
"http://119.53.27.173:9902",
"http://211.141.56.169:9901",
"http://222.169.70.166:9901",
"http://119.48.197.11:9902",
"http://36.49.51.94:9902",
"http://119.53.25.136:9902",
"http://119.53.27.196:9902",
"http://122.141.60.245:9901",
"http://119.50.3.76:9901",
"http://175.16.149.197:9901",
"http://221.9.97.148:9901",
"http://222.163.9.101:9901",
"http://139.212.77.165:9902",
"http://139.212.77.82:9902",
"http://139.212.78.255:9902",
"http://139.212.79.129:9902",
"http://139.212.77.181:9902",
"http://139.212.77.45:9902",
"http://139.212.79.156:9902",
"http://222.169.41.94:9901",
"http://119.51.64.108:9901",
"http://124.234.198.187:9901",
"http://122.138.32.222:9999",
"http://175.16.180.250:9901",
"http://139.209.39.206:9901",
"http://221.9.97.31:9901",
"http://58.245.99.42:9901",
"http://175.16.250.155:9901",
"http://222.169.41.90:9901",
"http://124.234.179.191:9901",
"http://122.139.47.206:9901",
"http://119.51.63.63:9901",
"http://175.16.184.213:9901",
"http://175.16.151.135:9901",
"http://125.32.120.209:9901",
"http://58.245.97.28:9901",
"http://175.18.189.238:9902",
"http://175.16.155.51:9901",
"http://124.234.199.122:9901",
"http://175.16.155.232:9901",
"http://175.16.149.189:9901",
"http://175.16.153.143:9901",
"http://222.169.41.11:9901",
"http://175.16.151.183:9901",
"http://119.51.52.185:9901",
"http://175.16.198.17:9901",
"http://222.162.195.165:9901",
"http://119.51.62.18:9901",
"http://59.44.203.42:9901",
"http://218.24.43.46:9901",
"http://39.152.171.140:9901",
"http://119.114.235.30:9902",
"http://124.94.207.48:9902",
"http://175.148.29.98:9902",
"http://119.114.238.244:9902",
"http://175.190.127.180:9901",
"http://59.44.10.113:9901",
"http://39.152.170.32:9901",
"http://59.44.135.122:9901",
"http://42.53.32.247:9902",
"http://60.16.18.243",
"http://116.3.67.48",
"http://58.245.255.38:9998",
"http://61.138.128.226:19901",
"http://39.152.171.140:9901",
"http://222.169.41.80:9901",
"http://59.44.10.113:990",
"http://59.44.203.42:9901",
"http://122.141.60.245:9901",
"http://60.16.18.243:4949",
"http://120.211.62.180:8000",
"http://123.182.247.236:8092",
"http://116.3.67.48:777",
"http://42.86.255.218:777",
"http://119.116.120.242:8888",
"http://119.116.41.199:88",

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
