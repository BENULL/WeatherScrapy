import os
import shutil

file_path = "./province_city.txt"
data_path = "/Users/null/Documents/PythonProject/WeatherCrawler/weather_data"
province_city_dict = {}

# 获取城市省份字典
def get_city_dict(file_path):

    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace("\r\n", "")
            spilts = line.split(" ")
            if len(spilts) > 3:
                province_name = (spilts[2]).strip()
                city_name = ((spilts[3]).strip())
                # 赋值到字典中
                province_city_dict[city_name] = province_name
    return province_city_dict


def file_process():
    os.chdir("{0}".format(str(data_path)))  # 将解释器的工作路径切换到要处理的文件夹的路径
    names = os.listdir("{0}".format(data_path))  # 获取当前目录下所有要批量处理的文件名names
    for name in names:  # 遍历所有的文件名
        print(name)
        city_name = name[:name.find("天气")]+"市"
        try:
            province_name = province_city_dict[city_name]
            origin = data_path+"/"+name
            to = data_path+"/"+province_name+"/"+name
            if not os.path.exists(data_path+"/"+province_name):
                os.mkdir(data_path+"/"+province_name)
            shutil.move(origin, to)  # 进行文件移动 原来的路径--> 目标路径
            print("Done {} to {}".format(origin,to))
        except Exception as e:
            print(e)
            pass


# 将城市名文件 按省份归档
if __name__ == "__main__":
    get_city_dict(file_path)
    file_process()

