import requests
import random
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re
import sys
from PyQt5.QtWidgets import *
from UI import *
from PyQt5.QtCore import QTimer
import create_day1_csv
import data1_analysis
import current_weather
#1.python访问潍坊天气服务，发给下位机，下位机保存每天0:00、7:00、12:00、17:00、22:00的数据。
#2.LCD：两个功能，通过按键切换实现：1）动态刷新显示实时天气，2）显示温度曲线（第一条中记录的五个时间点数据，超过14天则只显示最近前14天的数据）
#3.上位机显示和下位机LCD显示相同的内容
hTemList = []
lTemList = []
dataList = []
weaList = []
winList = []

url = 'http://www.weather.com.cn/weather/101120601.shtml' # 数据地址,从浏览器copy
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

soup = BeautifulSoup(req.text, 'html.parser')

def get_day7_weather():
    # 分析得 <ul class="t clearfix"> 标签下记录了我们想要的数据,因此只需要解析这个标签即可
    ul_tag = soup.find('ul', 't clearfix')  # 利用 css 查找
    # print(ul_tag)
    # print("tem: ",soup.find_all('div','tem'))
    li_tag = ul_tag.find_all('li')
    for tag in li_tag:
        data = tag.find('h1').string
        # print(data)  # 时间
        # print(dataList)
        wea = tag.find('p', 'wea').string
        # print(wea)  # wea
        weaList.append(wea)
        # print(weaList)
        # 温度的tag格式不统一,做容错
        try:
            hTemStr = tag.find('p', 'tem').find('span').string
            lTemStr = tag.find('p', 'tem').find('i').string
            # print(hTemStr)
            # print(lTemStr)

            hTemStr = re.findall(r'\d+|-\d+', hTemStr)
            for i in hTemStr:
                if i != '':
                    hTemInt = int(i)
                    hTemList.append(hTemInt)  # 高温

            lTemStr = re.findall(r'\d+|-\d+',lTemStr)
            for i in lTemStr:
                if i != '':
                    lTemInt = int(i)
                    lTemList.append(lTemInt)  # 低温

            data = re.findall(r'\d+', data)
            for i in data:
                if i != '':
                    dataList.append(int(i))
        except:
            print('没有高温或低温数据')

        win = tag.find('p', 'win').find('i').string # win
        # print(win)
        winList.append(win)
        # print(winList)

        # print("_______________ 分割线 ____________________")

    print(dataList)
    print(hTemList)
    print(lTemList)
    print(weaList)
    print(winList)

def plot_day7_hal_tem():
    fig2 = plt.figure(2)
    plt.plot(dataList,hTemList,color='red',label = "最高温")
    plt.plot(dataList,lTemList,color = 'orange',label = "最低温")
    plt.scatter(dataList, hTemList, color='red')  # 点出每个时刻的温度点
    plt.scatter(dataList, lTemList, color='orange')  # 点出每个时刻的温度点
    plt.rcParams['font.sans-serif']=['SimHei']	# 解决中文显示问题
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.title('未来七天最高温和最低温温度变化曲线')
    plt.xlabel('时间/日')
    plt.ylabel('摄氏度/℃')
    for a, b in zip(dataList,hTemList):
        plt.text(a, b, b, verticalalignment ='bottom', horizontalalignment = 'center',color='red', fontsize=10)
    for a, b in zip(dataList,lTemList):
        plt.text(a, b, b, verticalalignment ='bottom', horizontalalignment = 'center',color='orange', fontsize=10)
    plt.legend()
    # plt.ion()#让pLt.show()之后程序不会暂停住
    plt.show()


class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.uiWea()
        self.uiHTem()
        self.uiWin()
        self.uiLTem()
        self.pushButton.clicked.connect(self.upload)
        self.timer1 = QTimer(self)  # 初始化一个定时器
        self.timer1.timeout.connect(self.upload)  # 计时结束调用operate()方法
        self.timer1.start(3000)  # 设置计时间隔并启动

        # self.timer2 = QTimer(self)  # 初始化一个定时器
        # self.timer2.timeout.connect(self.update_current_weather)  # 计时结束调用operate()方法
        # self.timer2.start(2000)  # 设置计时间隔并启动

    def uiWea(self):
        for i in range(len(weaList)):
            weather = QTableWidgetItem(weaList[i])
            self.tableWidget.setItem(0,i,weather)
    def uiHTem(self):
        for i in range(len(hTemList)):
            htem = QTableWidgetItem(str(hTemList[i]))
            self.tableWidget.setItem(1, i, htem)
    def uiLTem(self):
        for i in range(len(lTemList)):
            ltem = QTableWidgetItem(str(lTemList[i]))
            self.tableWidget.setItem(2, i, ltem)
    def uiWin(self):
        for i in range(len(winList)):
            win = QTableWidgetItem(winList[i])
            self.tableWidget.setItem(3, i, win)

    # def update_current_weather():
    #     # 发送串口信息
    #     current_weather.main()

    def upload(self):
        plt.close()
        hTemList.clear()
        lTemList.clear()
        dataList.clear()
        weaList.clear()
        winList.clear()
        get_day7_weather()
        self.uiWea()
        self.uiHTem()
        self.uiLTem()
        self.uiWin()
        plot_day7_hal_tem()

if __name__ == '__main__':
    get_day7_weather()

    app = QApplication(sys.argv)
    myWin = MyWindow()

    myWin.show()
    #生成csv文件
    create_day1_csv.main()
    #画今天五个时刻的温度曲线
    data1_analysis.flash_window()

    # 7天的天气信息
    plot_day7_hal_tem()

    sys.exit(app.exec_())

