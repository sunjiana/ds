import time
import datetime
import concurrent.futures
import requests
import re
import os
import threading
from queue import Queue
import eventlet
eventlet.monkey_patch()


urls = [
    #辽宁的组播126
"http://60.16.18.243:4949",
"http://175.190.127.179:4949",
"http://36.129.204.120:8083",
"http://119.119.65.25:808",
"http://119.119.84.255:808 ",
"http://119.116.120.242:8888",
"http://113.228.41.153:8888",
"http://116.138.153.5:88",
"http://175.146.22.40:88",
"http://175.146.20.89:88",
"http://175.146.17.20:88",
"http://175.167.14.248:88",
"http://60.17.196.134:88",
"http://60.17.181.1:88",
"http://175.167.13.176:88",
"http://123.189.50.71:88",
"http://123.189.53.191:88",
"http://124.94.226.80:88",
"http://60.17.190.207:88",
"http://60.19.183.64:88",
"http://175.167.13.153:88",
"http://119.116.46.63:88",
"http://60.22.88.3:8002",
"http://123.244.72.23:808",
"http://123.244.72.20:808",
"http://123.244.72.114:808",
"http://123.244.72.129:808",
"http://123.244.72.73:808",
"http://123.244.72.100:808",
"http://123.244.72.106:808",
"http://123.244.72.85:808",
"http://123.244.72.86:808",
"http://123.244.72.55:808",
"http://123.244.72.92:808",
"http://123.244.72.126:808",
"http://123.244.72.123:808",
"http://123.244.72.115:808",
"http://123.244.72.124:808",
"http://123.244.72.38:808",
"http://123.244.72.43:808",
"http://123.244.72.39:808",
"http://175.170.20.218:808",
"http://42.84.22.79:808",
"http://113.235.206.84:808",
"http://42.84.212.167:771",
"http://42.84.222.67:771",
"http://60.20.70.252:808",
"http://119.113.105.187:808",
"http://113.234.63.69:808",
"http://175.163.61.148:808",
"http://119.113.248.176:808",
"http://60.20.83.121:808",
"http://175.163.36.175:808",
"http://36.129.204.120:8082",
"http://42.178.94.99:808",
"http://42.57.193.104:808",
"http://42.86.143.179:808",
"http://119.116.147.35:808",
"http://42.56.217.161:808",
"http://42.57.204.5:808",
"http://113.228.76.52:808",
"http://42.57.199.54:808",
"http://124.95.7.5:808",
"http://42.55.223.22:808",
"http://175.151.83.30:808",
"http://42.55.223.143:808",
"http://42.5.236.172:808",
"http://42.55.223.217:808",
"http://42.55.223.243:808",
"http://42.58.222.194:808",
"http://42.55.222.223:808",
"http://42.55.222.203:808",
"http://42.55.222.214:808",
"http://175.175.166.190:808",
"http://175.175.164.121:808",
"http://42.58.222.54:808",
"http://175.151.82.92:808",
"http://42.178.53.24:808",
"http://42.178.89.169:808",
"http://124.95.14.74:808",
"http://124.95.29.178:808",
"http://113.239.107.230:808",
"http://42.55.216.220:808",
"http://42.55.217.187:808",
"http://175.175.171.224:808",
"http://175.175.186.179:808",
"http://42.5.237.58:808",
"http://42.5.239.197:808",
"http://42.5.237.58:808",
"http://42.5.239.197:808",
"http://42.4.96.42:808",
"http://42.57.198.240:808",
"http://42.55.218.13:808",
"http://42.55.218.95:808",
"http://42.57.199.174:808",
"http://42.55.223.90:808",
"http://42.57.198.50:808",
"http://42.5.239.130:808",
"http://42.58.223.172:808",
"http://42.52.28.187:808",
"http://42.58.223.190:808",
"http://113.231.117.20:808",
"http://42.55.216.87:808",
"http://113.231.109.187:808",
"http://175.151.82.165:808",
"http://42.57.193.131:808",
#北京组播29
"http://113.45.171.28:465",
"http://8.130.21.200:880",
"http://103.72.172.253:8040",
"http://81.70.248.163:8888",
"http://47.93.113.151:80",
"http://49.7.234.13:808",
"http://49.7.234.2:808",
"http://49.7.234.98:808",
"http://49.7.234.2:80",
"http://49.7.234.98:80",
"http://49.7.234.13:80",
"http://123.118.156.146:8888",
"http://114.253.72.39:8888",
"http://123.121.85.12:8888",
"http://114.243.181.154:8089",
"http://49.7.234.13:8888",
"http://114.251.13.196:443",
"http://114.251.13.203:443",
"http://114.251.13.196:80",
"http://123.114.209.150:8089",
"http://120.244.126.209:8089",
"http://120.244.126.241:8089",
"http://49.7.234.3:80",
"http://1.203.120.115:8089",
"http://49.7.234.5:80",
"http://101.254.208.170:80",
"http://101.254.185.170:80",
"http://101.254.208.174:80",
"http://101.254.185.171:80",
# 保定72
"http://101.19.151.139:808",
"http://101.19.151.161:808",
"http://101.19.150.20:808",
"http://101.19.151.71:808",
"http://101.19.149.191:808",
"http://101.19.149.140:808",
"http://101.19.151.157:808",
"http://101.19.151.62:808",
"http://101.19.151.194:808",
"http://101.19.149.91:808",
"http://101.19.148.235:808",
"http://101.19.150.42:808",
"http://101.19.151.170:808",
"http://101.19.151.167:808",
"http://101.19.151.111:808",
"http://101.19.150.237:808",
"http://101.19.148.207:808",
"http://101.19.149.144:808",
"http://101.19.150.131:808",
"http://101.19.151.12:808",
"http://101.19.151.12:808",
"http://101.19.151.193:808",
"http://101.19.148.97:808",
"http://101.19.151.155:808",
"http://101.19.148.127:808",
"http://101.19.149.168:808",
"http://101.19.151.11:808",
"http://101.19.150.4:808",
"http://101.19.149.224:808",
"http://101.19.151.87:808",
"http://101.19.149.172:808",
"http://101.19.148.19:808",
"http://101.19.149.170:808",
"http://101.19.149.155:808",
"http://101.19.148.8:808",
"http://101.19.149.75:808",
"http://101.19.151.169:808",
"http://101.19.150.216:808",
"http://101.19.151.155:808",
"http://101.19.150.178:808",
"http://101.18.25.106:808",
"http://101.19.148.244:808",
"http://101.19.149.203:808",
"http://101.19.150.62:808",
"http://101.19.148.237:808",
"http://101.19.148.53:808",
"http://101.19.151.250:808",
"http://101.19.149.139:808",
"http://101.19.149.85:808",
"http://101.19.148.119:808",
# 邯郸421
"http://101.26.42.41:808",
"http://101.26.42.86:808",
"http://101.26.42.250:808",
"http://183.196.87.176:880",
"http://106.115.24.169:8088",
"http://101.23.216.69:8090",
"http://106.117.129.245:808",
"http://121.24.98.238:8090",
"http://121.24.99.25:8090",
"http://121.24.99.169:8090",
"http://121.24.99.41:8090",
"http://121.24.98.232:8090",
"http://121.24.99.190:8090",
"http://121.24.98.151:8090",
"http://121.24.99.44:8090",
"http://121.24.98.250:8090",
"http://121.24.99.99:8090",
"http://121.24.99.213:8090",
"http://123.181.1.172:808",
"http://121.24.98.236:8090",
"http://121.24.99.131:8090",
"http://121.24.98.226:8090",
"http://121.24.98.15:8090",
"http://121.24.98.40:8090",
"http://121.24.98.184:8090",
"http://121.24.98.96:8090",
"http://121.24.98.139:8090",
"http://121.24.99.229:8090",
"http://121.24.98.102:8090",
"http://121.24.98.229:8090",
"http://121.24.98.106:8090",
"http://121.24.98.136:8090",
"http://121.24.99.68:8090",
"http://121.24.99.10:8090",
"http://121.24.98.79:8090",
"http://121.24.99.239:8090",
"http://121.24.98.85:8090",
"http://121.24.98.252:8090",
"http://121.24.98.100:8090",
"http://121.24.99.197:8090",
"http://121.24.98.134:8090",
"http://121.24.98.123:8090",
"http://121.24.98.224:8090",
"http://121.24.99.181:8090",
"http://121.24.98.66:8090",
"http://121.24.98.55:8090",
"http://121.24.98.182:8090",
"http://121.24.99.226:8090",
"http://106.117.130.11:808",
"http://106.117.134.232:808",
#东北附近githu
"http://60.16.18.243:4949",
"http://120.211.62.180:8000",
"http://123.182.247.236:8092",
"http://116.3.67.48:777",
"http://42.86.255.218:777",
#fofa liaoning
"http://119.116.41.199:88",
"http://42.86.255.218:777",
"http://119.116.120.242:8888",
"http://116.3.67.48:777",
"http://113.227.0.35:777",
"http://124.94.225.126:8888",
"http://116.3.68.151:777",
"http://175.171.197.54:777",
"http://175.171.197.70:777",
"http://119.114.51.247:88",


    ]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/ZHGXTV/Public/json/live_interface.txt"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls


def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.2)
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
            print(result)

#for url in valid_urls:
#    print(url)

#now_today = datetime.date.today()
#with open("ip.txt", 'a', encoding='utf-8') as file:
#    file.write(f"{now_today}更新\n")
#    for url in valid_urls:
#        file.write(url + "\n")

# 遍历网址列表，获取JSON文件并解析
for url in valid_urls:
    try:
        # 发送GET请求获取JSON文件，设置超时时间为0.5秒
        json_url = f"{url}"
        response = requests.get(json_url, timeout=1)
        json_data = response.content.decode('utf-8')
        try:
            # 按行分割数据
            lines = json_data.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    name, channel_url = line.split(',')
                    urls = channel_url.split('/', 3)
                    url_data = json_url.split('/', 3)
                    if len(urls) >= 4:
                        urld = (f"{urls[0]}//{url_data[2]}/{urls[3]}")
                    else:
                        urld = (f"{urls[0]}//{url_data[2]}")
                    print(f"{name},{urld}")
                    if name and urld:
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

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

error_channels = []


# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
            lines = requests.get(channel_url, timeout = 1).text.strip().split('\n')  # 获取m3u8文件内容
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
            ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

            # 多获取的视频数据进行5秒钟限制
            with eventlet.Timeout(5, False):
                start_time = time.time()
                content = requests.get(ts_url, timeout = 1).content
                end_time = time.time()
                response_time = (end_time - start_time) * 1

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)  # 写入文件
                file_size = len(content)
                # print(f"文件大小：{file_size} 字节")
                download_speed = file_size / response_time / 1024
                # print(f"下载速度：{download_speed:.3f} kB/s")
                normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                #print(f"标准化后的速率：{normalized_speed:.3f} MB/s")

                # 删除下载的文件
                os.remove(ts_lists_0)
                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                results.append(result)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 10
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)  # 将工作线程设置为守护线程
    t.start()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))


result_counter = 8  # 每个频道需要的个数

with open("ZHGXTV1.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

with open("itvlist.m3u", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('#EXTM3U\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    #file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    #file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
