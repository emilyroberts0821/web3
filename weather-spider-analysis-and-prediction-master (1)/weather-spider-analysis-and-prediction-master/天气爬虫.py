import requests  # py自带常用的网页请求包，用于请求网页源代码模块
import re  # py自带的正则表达式模块，用于匹配网页源代码的标签信息
from bs4 import BeautifulSoup  # py的第三方爬虫库，用于生成网页源代码的代码树
import pandas as pd  # py的第三方信息架构库，用于存储信息格式以及将信息存到文档当中
import pypinyin  # py的第三方拼音库，选用模块，为了保证程序的封装可靠性，我们由用户输入中文城市名，并由该模块转成拼音得到爬取链接
from os import startfile  # py自带的系统文件库的打开文件函数，用于打开导出成功的文件

dateInfo = []  # 日期列表，用于存储日期信息
maxTemper = []  # 最高温度列表，用于存储最高温度信息
minTemper = []  # 最低温度列表，用于存储最低温度信息
weather = []  # 天气列表，用于存储天气信息
windInfo = []  # 风向列表，用于存储风向列表


class URL2Code:
    def __init__(self, cityName: str, year: list = (), month: list = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)):
        self.__city = cityName  # 实例化城市对象
        self.__year = year  # 实例化年份对象
        self.__month = month  # 实例化月份对象

    def GetUrl(self) -> list[str]:
        # 生成链接模板 主域名/[城市名称拼音/月份信息.html
        link = []  # 链接列表，用于存储生成的链接信息
        for year in self.__year:  # 将所有年份元素提取处理，送入循环内
            for month in self.__month:  # 提取当前月份内的所有指定月份表内的数据，送入虚幻内
                if month < 10:  # 如果月份是小于0的，那么它的链接月份前缀需要加上 0
                    url = 'http://lishi.tianqi.com/{}/{}0{}.html'.format(self.__city, year, month)
                else:
                    url = 'http://lishi.tianqi.com/{}/{}{}.html'.format(self.__city, year, month)
                link.append(url)  # 保存生成好的链接
        return link

    def GetUrlText(self, url) -> str or None:
        headers = {  # 请求标头，通过模拟请求标头以此实现仿人类登录进入网站并获取信息
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Cookie'    : 'lianjia_uuid=9d3277d3-58e4-440e-bade-5069cb5203a4;'
                              'UM_distinctid=16ba37f7160390-05f17711c11c3e-454c0b2b-100200-16ba37f716618b;'
                              ' _smt_uid=5d176c66.5119839a;'
                              'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216ba37f7a942a6-0671dfdde0398a-454c0b2b-1049088-16ba37f7a95409%22%2C%22%24device_id%22%3A%2216ba37f7a942a6-0671dfdde0398a-454c0b2b-1049088-16ba37f7a95409%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; '
                              '_ga=GA1.2.1772719071.1561816174; '
                              'Hm_lvt_9152f8221cb6243a53c83b956842be8a=1561822858;'
                              '_jzqa=1.2532744094467475000.1561816167.1561822858.1561870561.3;'
                              'CNZZDATA1253477573=987273979-1561811144-%7C1561865554;'
                              'CNZZDATA1254525948=879163647-1561815364-%7C1561869382;'
                              'CNZZDATA1255633284=1986996647-1561812900-%7C1561866923;'
                              'CNZZDATA1255604082=891570058-1561813905-%7C1561866148;'
                              '_qzja=1.1577983579.1561816168942.1561822857520.1561870561449.1561870561449.1561870847908.0.0.0.7.3;'
                              'select_city=110000; lianjia_ssid=4e1fa281-1ebf-e1c1-ac56-32b3ec83f7ca;'
                              'srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMzQ2MDU5ZTQ0OWY4N2RiOTE4NjQ5YmQ0ZGRlMDAyZmFhO'
                              'DZmNjI1ZDQyNWU0OGQ3MjE3Yzk5NzFiYTY4ODM4ZThiZDNhZjliNGU4ODM4M2M3ODZhNDNiNjM1NzMzNjQ4'
                              'ODY3MWVhMWFmNzFjMDVmMDY4NWMyMTM3MjIxYjBmYzhkYWE1MzIyNzFlOGMyOWFiYmQwZjBjYjcyNmI'
                              'wOWEwYTNlMTY2MDI1NjkyOTBkNjQ1ZDkwNGM5ZDhkYTIyODU0ZmQzZjhjODhlNGQ1NGRkZTA0ZTBlZDFiN'
                              'mIxOTE2YmU1NTIxNzhhMGQ3Yzk0ZjQ4NDBlZWI0YjlhYzFiYmJlZjJlNDQ5MDdlNzcxMzAwMmM1ODBlZDJkNm'
                              'IwZmY0NDAwYmQxNjNjZDlhNmJkNDk3NGMzOTQxNTdkYjZlMjJkYjAxYjIzNjdmYzhiNzMxZDA1MGJlNjBmNzQ'
                              'xMTZjNDIzNFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIzMGJlNDJiN1wifSIsInIiOiJodHRwczovL2'
                              'JqLmxpYW5qaWEuY29tL3p1ZmFuZy9yY28zMS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=='
                }
        html = requests.get(url, headers = headers)  # 尝试连接指定网址并获取数据
        if html.status_code == 200:  # 如果链接成功，并且返回状态码为 200 (200为网页正常访问的状态码)
            html.encoding = html.apparent_encoding  # 初始化网页的编码格式
            return html.text  # 返回该网页源代码
        else:
            return None  # 如果返回的状态码不是200，也就是链接失败，那么返回None，在原函数内提示错误并退出程序


def Spider(cityName: str, year: list, month: list = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)) -> None:
    URL = URL2Code(cityName, year, month)  # 首先需要获取目标城市和年限的链接信息，这里初始化链接生成器
    link = URL.GetUrl()  # 获取指定城市、年限、月份的链接
    for url in link:  # 将所有链接放入循环，一个个处理请求
        html = URL.GetUrlText(url)  # 从链接列表里提取出网址，并送入网页源代码提取方法内提取对应的网页源代码
        if (html is None):  # 如果提取到的网页源代码是空
            print("获取连接失败"), exit(-1)

        bs = BeautifulSoup(html, 'html.parser')  # 构建网页源代码的代码树
        data = bs.find_all(class_ = 'thrui')  # 查找 thrui 标签并存储到data列表内
        date = re.compile('class="th200">(.*?)</')  # 构建正则匹配器，用于匹配日期
        tem = re.compile('class="th140">(.*?)</')  # 构建正则匹配器，用于匹配天气信息

        time = re.findall(date, str(data))  # 将 thrui 标签内的信息送进日期匹配器内
        # 提取出如：'2022-06-01 星期三 '的信息，这个时候我们需要把日期提取出来
        print(time)
        for item in time:  # 使用将时间列表放入循环，循环提取出信息字符串
            findDate = item[:10]  # 使用切片把字符串内的时间提取出来
            dateInfo.append(findDate)  # 将日期信息添加到最终的时间列表内

        temp = re.findall(tem, str(data))  # 把天气信息放入匹配器
        # 此时匹配器提取出该信息表格内所有的信息，内容包括 0~n 记载的n天信息在内的所有天气信息在其中。
        # 如果需要提取出每天的信息，那么需要根据时间来进行计算提取，
        # 例如，我想提取出6月1(n)日的天气，那么我需要从列表的第 n-1 个位置中开始提取, 并往后提取3个序列长度，以此将对应信息提取完全。
        for i in range(len(time)):  # 根据天气时长来进入循环，因为天气与日期长度必定是一致的, 也方便提取操作的进行
            maxTemper.append(temp[i * 4 + 0])  # 从时间序列的第一个位置开始提 最高温度
            minTemper.append(temp[i * 4 + 1])  # 从时间序列的第一个位置开始提 最低温度
            weather.append(temp[i * 4 + 2])  # 从时间序列的第一个位置开始提 天气
            windInfo.append(temp[i * 4 + 3])  # 从时间序列的第一个位置开始提 风向


def OutputData():
    data = pd.DataFrame({  # 使用pandas模块，生成信息框架，将内容列为一个数据框架dataFrame
            '日期'  : dateInfo, '最高温度': maxTemper,
            '最低温度': minTemper, '天气': weather, '风向': windInfo
            }
            )
    data.to_csv('天气数据.csv', encoding = 'gbk', index = False)
    # 导出为csv文档，命名为‘天气数据.csv’; 编码格式设置为gbk，避免用office-Excel打开会乱码; 取消序号列提示(否则会有一列是表示当前数据的排序位置)


def Main():
    # 主函数，如提示所示，这里是由用户输入待爬取的城市信息以及爬取的年份、月份。这里为了减少代码量，使用了生成器OwO,当方法和结果都是一样的
    Spider(cityName = "".join(pypinyin.lazy_pinyin(input("请输入你想查询的城市名称:> "),  # 输入城市中文名，用了pypinyin第三方模块
                                                   style = pypinyin.NORMAL  # 默认的style会返回一个中文拼音带声调的多位数组
                                                   # 修改成NORMAL的style可以直接放回该中文不带声调的拼音的一维数组
                                                   )
                              ),
           year = [year for year in range(int(input("请输入你想查询的 [开始年份] :> ")),  # 输入开始年份，循环生成一个数字序列，从开始年份开始
                                          int(input("请输入你想查询的 [结束年份] :> ")) + 1  # 在循环生成的序列中是一个开区间，所以需要在输入结束年份+1
                                          )],
           month = [month for month in range(int(input("请输入你想查询的 [开始月份] :> ")),  # 输入开始月份，同理年份
                                             int(input("请输入你想查询的 [结束月份] :> ")) + 1  # 输入结束月份，同理
                                             )]
           )
    OutputData()  # 导出数据


if __name__ == '__main__':
    Main()  # 程序由此开始，首先进入主函数
    startfile('天气数据.csv')  # 主函数退出后，打开保存成功的数据文件