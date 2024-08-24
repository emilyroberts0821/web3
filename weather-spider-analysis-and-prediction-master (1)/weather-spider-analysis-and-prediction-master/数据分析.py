import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
path = "天气数据.csv"

frame = pd.read_csv(path, encoding = 'gbk')

weather = list((set(frame['天气'])))
weatherDict = (dict(zip(weather, range(1, len(weather)+1))))
frame['最高温度'] = frame['最高温度'].map(lambda x: x.replace('℃', '')).map(int)

# 对 天气情况 进行统计并分析 【条形图】
plt.figure(figsize=(15,10))
frame['天气'].value_counts().head(20).plot(kind='bar')
plt.title('2011-2022年 情况统计')
plt.show()

# 对 风向 进行统计并分析 【条形图】
plt.figure(figsize=(15,10))
frame['风向'].value_counts().head(20).plot(kind='bar')
plt.title('2011-2022年 风力统计')
plt.show()

# 对 最高温度 进行统计并分析 【直方图】
plt.figure(figsize=(15, 10))
sns.distplot(frame['最高温度'],bins=[i for i in range(0,61,5)], kde=False)
plt.title("2011-2022年 最高温度直方图分析")
plt.grid()


def get_year(x):
  return x[0:4]

def get_day(x):
  return x[8:]

frame["Year"] = frame['日期'].apply(lambda x:get_year(str(x))).map(int)       # 分类出年限
frame["day"] = frame['日期'].apply(lambda x:get_day(str(x))).map(int)         # 分类出日期
temp_year = pd.crosstab(frame['Year'], frame['day'], values=frame['最高温度'], aggfunc='mean')  # 绘制热力图
plt.figure(figsize=(15, 10))
sns.heatmap(temp_year, cmap='coolwarm', annot=True)
plt.title("2011-2022年最高温度热力图分析")
plt.show()