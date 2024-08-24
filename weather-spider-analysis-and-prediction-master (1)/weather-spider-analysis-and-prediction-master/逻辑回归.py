import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# 数据可视化
# 解决显示中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 第一步：数据读取
data = pd.read_csv(r'E:\Code File\Python\pythonProject2\Output.csv',encoding='gb2312')
# 第二步：数据处理（由于我们知道文本内容，不存在脏数据，故忽略数据清理步骤）
data['最高温度'] = data['最高温度'].map(lambda x: x.replace('℃', ''))
data['最低温度'] = data['最低温度'].map(lambda x: x.replace('℃', ''))

for year in range(11, 23):
    data['日期'] = data['日期'].map(lambda x: x.replace(f'20{year}-06-', ''))

dates = data['日期']
highs = data['最高温度']
lows = data['最低温度']
print(len(dates))

highs_int=[]      #最高温度的列表
for num1 in highs:
    highs_int.append(int(num1))
lows_int=[]       #最低温度的列表
for num2 in lows:
    lows_int.append(int(num2))
 
dates_int = []      #日期的列表
for num3 in dates:
    dates_int.append(int(num3))


# 要将月份天数转为序列 1~day 的序列值
newdates_int = np.array(dates_int)
for i in range(0, len(dates_int)):
    newdates_int[i] = i+1

DatesAndLows = []     #由日期最低温度组成的列表
for num4 in range(0, len(lows)):
    arr = [newdates_int[num4],lows_int[num4]]
    DatesAndLows.append(arr)


#第三步 训练模型-LogisticRegression
X = DatesAndLows     #日期和最低温度
Y = highs_int    #最高温度

x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.3)
model = LogisticRegression(solver = 'lbfgs')    #使用lbfgs算法,拟牛顿法的一种，利用损失函数二阶导数矩阵即海森矩阵来迭代优化损失函数
model.fit(x_train, y_train)
print('预测结果为:')
print(model.predict(x_test))
y_predict = model.predict(x_test)
print('model.score为：', model.score(x_test, y_test))      #打分
print('r2_score为: ',r2_score(y_test,y_predict))
# 获取Theta计算结果
theta = np.array([model.intercept_[0], model.coef_[0,0],model.coef_[0,1]])
# print(theta)

#设置逻辑回归算法的某些属性
#model = LogisticRegression(solver='lbfgs')
#使用lbfgs算法来执行回归计算。默认使用liblinear。注意，这两种算法的结果并不相同
#执行计算
#model.fit(X, y)
#执行预测
#model.predict(newX)
#返回值是newX矩阵中每行数据所对应的结果。如果是1，则表示passed；如果是0，则表示unpassed
#获得模型参数值
#theta0 = model.intercept_[0] theta1 = model.coef_[0,0] theta2 = model.coef_[0,1]
#决策边界线
#决策边界线可视为两种类别数据点的分界线。在该分界线的一侧，所有数据点都被归为passed类(1)，另一侧的所有数据点都被归为unpassed类(0)
#对于本例来说，决策边界线是一条直线

#第四步 数据可视化
def initPlot():
    plt.figure()
    plt.title('逻辑回归分析')
    plt.xlabel('日期')
    plt.ylabel('最低温度')
    return plt

plt = initPlot()
factor1 = newdates_int     #影响因素1 日期
factor2 = lows_int      #影响因素2 最低气温
plt.plot(factor1,'r--')
plt.plot(factor2,)
plt.legend(['影响因素1 日期', '影响因素2 最低气温'])
plt.ylim(0,40)
boundaryX = np.mat(newdates_int)
boundaryY = -np.mat((theta[1] * np.mat(boundaryX) + theta[0]) / theta[2])       #填充决策线
plt.plot(boundaryX,boundaryY,'b.')

plt.show()


#综上可以观察到，所有数据点并不明显分成两个类别。说明最低温度和日期并不能对最高温度进行分类
#线性回归主要都是针对训练数据和计算结果均为数值的情形。
#而在本例中，结果不是数值而是某种分类：这里分成日期和最低气温两类。
#而且发现，两类并不显示有明显的分界线。这进一步说明最高温度的影响因素不是日期和最低气温
#我们通过数据爬取预测模型最终得出结论：最高温度的影响因素与日期和最低气温毫无关联
