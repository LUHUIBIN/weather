import requests
import random
import json
from bs4 import BeautifulSoup
import csv

url = 'http://www.weather.com.cn/weather/101010100.shtml' # 数据地址,从浏览器copy
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3226.400 QQBrowser/9.6.11681.400'
}
timeout = random.choice(range(80, 180)) # 超时时间
req = requests.get(url, headers=header, timeout=timeout)
req.encoding = 'utf-8' # 防止中文乱码
code = req.status_code # 返回状态,200代表OK
print(code)

def get_html_text(url):
    """请求获得网页内容"""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问网页")
        return r.text
    except:
        print("访问错误")
        return " "
def get_day1_content(html):
    """处理得到有用信息保存数据文件"""
    final = []  # 初始化一个列表保存数据
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body
    # data = body.find('div', {'id': '7d'})  # 找到div标签且id = 7d
    # 下面爬取当天的数据
    data2 = body.find_all('div', {'class': 'left-div'})
    text = data2[2].find('script').string
    text = text[text.index('=') + 1:-2]  # 移除改var data=将其变为json数据
    jd = json.loads(text)
    dayone = jd['od']['od2']  # 找到当天的数据
    final_day = []  # 存放当天的数据
    count = 0
    for i in dayone:
        temp = []
        if count <= 23:
            if i['od21'] == '00' or i['od21'] == '07' or i['od21'] == '07' or i['od21'] == '12' or i['od21'] == '17' or i['od21'] == '22' :
                temp.append(i['od21']) # 添加时间
                temp.append(i['od22'])  # 添加当前时刻温度
                final_day.append(temp)
        count = count + 1
    return final_day

def write_to_csv(file_name, data, day=14):
    """保存为csv文件"""
    with open(file_name, 'w+', errors='ignore', newline='') as f:
        if day == 14:
            header = ['日期', '天气', '最低气温', '最高气温', '风向1', '风向2', '风级']
        else:
            header = ['小时', '温度']
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(data)
        print('写入csv成功')

def main():
    html1 = get_html_text(url)
    data1 = get_day1_content(html1)
    write_to_csv('weather1.csv', data1, 1)


main()
