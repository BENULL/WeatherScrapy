import time

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import threading


target_year_list = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
target_month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


class Crawler(threading.Thread,):

    def run(self):
        print("%s is running" % threading.current_thread())
        while True:
            # 上锁
            gLock.acquire()
            if len(city_dict) == 0:
                # 释放锁
                gLock.release()
                continue
            else:
                item = city_dict.popitem()
                gLock.release()
                data_ = list()
                urls = self.get_urls(item[0])
                for url in urls:
                    try:
                        data_.extend(self.get_data(url))  # 列表合并，将某个城市所有月份的天气信息写到data_
                    except Exception as e:
                        print(e)
                        pass
                self.saveTocsv(data_, item[1])  # 保存为csv
                if len(city_dict) == 0:
                    end = time.time()
                    print("消耗的时间为：", (end - start))
                    exit()


    # 获取城市历史天气url
    def get_urls(self,city_pinyin):
        urls = []
        for year in target_year_list:
            for month in target_month_list:
                date = year + month
                # url = "http://www.tianqihoubao.com/lishi/beijing/month/201812.html"
                urls.append("http://www.tianqihoubao.com/lishi/{}/month/{}.html".format(city_pinyin, date))
        return urls

    def get_soup(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()  # 若请求不成功,抛出HTTPError 异常
            soup = BeautifulSoup(r.text, "html.parser")
            return soup
        except Exception as e:
            print(e)
            pass

    # 将天气数据保存至xls文件
    def saveTocsv(self,data, city):
        fileName = './weather_data/' + city + '天气.xls'
        result_weather = pd.DataFrame(data, columns=['日期', '天气状况', '气温', '风力风向'])
        # print(result_weather)
        result_weather.to_excel(fileName, index=False)
        print('Save all weather success!')
        print('remain{}'.format(len(city_dict)))


    def get_data(self,url):
        print(url)
        try:
            soup = self.get_soup(url)
            all_weather = soup.find('div', class_="wdetail").find('table').find_all("tr")
            data = list()
            for tr in all_weather[1:]:
                td_li = tr.find_all("td")
                for td in td_li:
                    s = td.get_text()
                    # print(s.split())
                    data.append("".join(s.split()))

            # print(data)
            # print(type(data))
            res = np.array(data).reshape(-1, 4)

            # print(res)
            # print(type(res[0]))
            # print(res[0][1])
            return res

        except Exception as e:
            print(e)
            pass


# 从文件获取城市信息
def get_city_dict(file_path):
    city_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace("\r\n", "")
            city_name = (line.split(" ")[0]).strip()
            city_pinyin = ((line.split(" ")[1]).strip()).lower()
            # 赋值到字典中
            city_dict[city_pinyin] = city_name
    return city_dict


file_path = "./city_pinyin_test.txt"
gLock = threading.Lock()

if __name__ == '__main__':

    # 多线程爬取
    city_dict = get_city_dict(file_path)
    start = time.time()
    #启动10个线程
    for x in range(10):
        Crawler().start()

