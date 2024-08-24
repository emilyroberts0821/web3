import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# 解决中文问题（若没有此步骤，表名字及横纵坐标中的汉语将无法显示[具体会显示矩形小方格]）
plt.rcParams['font.sans-serif'] = ['SimHei']

# 将数据从 .csv 格式文件中读取
data = pd.read_csv(r'E:\Code File\Python\pythonProject2\Output.csv', encoding = 'gbk')
# print(data)
# 由于最高气温与最低气温中有 / 分隔，故将其分开，即“气温”列由一列变为两列——“最高气温”和“最低气温”
data['最高温度'] = data['最高温度'].map(lambda x: x.replace('℃', ''))

for year in range(11, 23):
    data['日期'] = data['日期'].map(lambda x: x.replace(f'20{year}-06-', ''))

dates = data['日期']
highs = data['最高温度']

highs_int = []  # 最高温度的列表
for num1 in highs:
    highs_int.append(int(num1))

dates_int = []  # 日期的列表
for num1 in dates:
    dates_int.append(int(num1))

newdates_int = np.array(dates_int)
for i in range(0, len(dates_int)):
    newdates_int[i] = i+1


# 日期(对于单变量，矩阵就是列向量形式)
xTrain = newdates_int[:, np.newaxis]
# 最高气温
yTrain = highs_int

# 创建模型对象
model = LinearRegression()
# 根据训练数据拟合出直线
hypothesis = model.fit(xTrain, yTrain)
# 数据拟合直线截距
print("theta0=", hypothesis.intercept_)
# 数据拟合直线斜率
print("theta1=", hypothesis.coef_)

# 预测2022年6月18日的最高气温
# print(model.predict())
print("预测2022年6月18日的最高气温：", model.predict([[len(highs)]]))

# 假设要预测一星期的天气
nextWeek = [i for i in range(len(highs), len(highs) - 7, -1)]
print(f"next: {nextWeek}")
xNew = np.array(nextWeek)[:, np.newaxis]
yNew = model.predict(xNew)
print("预测新数据：", xNew)
print("预测结果：", yNew)


def initPlot():
    # 先准备好一块画布
    plt.figure()
    # 生成图表的名字
    plt.title('2019-2021年6月最高气温变化趋势')
    # 横坐标名字
    plt.xlabel('日期')
    # 纵坐标名字
    plt.ylabel('当日最高气温')
    # 表内有栅格
    plt.grid(True)
    return plt


plt = initPlot()  # 画图
# k是黑色，.是以点作为图上显示
plt.plot(xTrain, yTrain, )
# 画出通过这些点的连续直线
plt.plot(xNew, yNew, 'g--')
# 将图显示出来
plt.show()
