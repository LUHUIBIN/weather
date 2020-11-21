# data1_analysis.py
import matplotlib.pyplot as plt
import pandas as pd
import serial



def usart(tem_data):
    ser = serial.Serial('com2', 115200, timeout=2)
    if ser.isOpen():
        print('串口已打开')
    for item in tem_data:
        if isinstance(item,str):
            print(1)
            ser.write(bytes(item,'gbk'))  # 串口写数据


        elif isinstance(item,int):
            print(2)
            ser.write(bytes(str(item),'utf-8'))  # 串口写数据



    ser.write(b'\r\n')
    print("数据发送成功")

    # while True:
    #     data_read = serial.read(80)  # 串口读20位数据
    #     print(data_read)
    #     if data_read != b'':
    #         break

    # 关闭串口
    ser.close()
    if ser.isOpen():
        print('串口未关闭')
    else:
        print('串口已关闭')

def tem_curve(data):
    """温度曲线绘制"""
    hour = list(data['小时'])
    hour = [str(i) for i in hour]
    print(hour)
    tem = list(data['温度'])
    print(tem)

    usart(tem)# send tem data

    tem_ave = sum(tem)/5

    x = hour
    y = tem
    fig1 = plt.figure(1)
    plt.plot([0,4],[tem_ave,tem_ave],"--")
    plt.plot(x, y, color='red', label='温度')  # 画出温度曲线
    plt.scatter(x, y, color='red')  # 点出每个时刻的温度点

    plt.legend()
    plt.title('一天温度变化曲线图')
    plt.xlabel('时间/h')
    plt.ylabel('摄氏度/℃')
    plt.draw() #若使用plot画图则程序画完后不会继续运行
    plt.pause(3)
    plt.close(fig1)



def main():
    plt.rcParams['font.sans-serif']=['SimHei']	# 解决中文显示问题
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    data1 = pd.read_csv('weather1.csv',encoding='gb2312')
    data1=data1.sort_values(by='小时') # 按时间排序
    print(data1)
    tem_curve(data1)

def flash_window():
    while True:
        main()






