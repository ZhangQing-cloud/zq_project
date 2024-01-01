import json
import os
class BaseJson:
    # 加载 json 文件中数据
    @staticmethod
    def readJson(file):
        if not os.path.exists(file):    # 文件不存在则直接返回空 list
            return []
        with open(file,mode='r',encoding='utf-8') as f:
            return json.load(f)

    # 添加字典或字典列表到文件
    @staticmethod
    def appendToJson(dicts,file):
        data = BaseJson.readJson(file)  # 读取已有数据
        if type(dicts) is list:
            data.extend(dicts)
        elif type(dicts) is dict:
            data.append(dicts)
        else:
            print(str(dicts)+'is not dict or list!!!')

        with open(file, mode='w+') as f:
            json.dump(data, f)

    @staticmethod
    def saveToJson(data,file):
        with open(file, mode='w+') as f: # w+ 建立新的文件
            json.dump(data, f)