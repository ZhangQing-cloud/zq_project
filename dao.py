'''
数据访问模块
json.load(file)      : 参数为文件
json.loads(jsonstr)  : 参数为json格式的字符串

json.dump(dict_data,file) :把字典对象保存到json文件中
json.dumps(dict_data) : dumps是将dict转化成str格式

封装实现解析文件数据和登录逻辑判断的一个类
验证登录信息的
'''
import json
from jsonutil import BaseJson
from openpyxl import Workbook,load_workbook
import pymysql

#第一种方法
class UserDao:
    # 传入用户名和密码，验证成功与否
    def login(self,username,password):
        f = open('config.json',mode='r')
        data = json.load(f) # 解析json文件中所有的数据
        for user in data:
            uname = user['username']
            pwd = user['password']
            if uname==username and pwd == password:
                return True
        return False
#第二种方法
# class UserDao:
#     def login(self,username,password):
#         # 传入用户名和密码，验证成功与否
#         # 1.连接MYSQL
#         conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', password="zhangqing", charset='utf8',
#                                db='book')
#         cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 需要一个指令来收取数据
#
#         sql = "select * from book_secret"
#         cursor.execute(sql)
#         data_list = cursor.fetchall()
#         for user in data_list:
#             uname = user['username']
#             pwd = user['password']
#             if uname==username and pwd == password:
#                 return True
#         return False
#         # 3.关闭连接
#         cursor.close()
#         conn.close()

class BookDao(BaseJson):
    def list(self):
        return super().readJson('books.json')

class ExcelDao:

    def export(self,filepath):
        # 获取数据
        books = BaseJson.readJson('books.json')

        wb = Workbook()
        sheet = wb.active
        header = ['图书名称', '价格', '作者', '出版社']
        sheet.append(header)
        for book in books:
            print('******', list(book.values()))
            sheet.append(list(book.values()))
        print("===========1=============")
        wb.save(filepath)
        print("===========2=============")
        wb.close()
        print('导出成功！保存在: %s' % (filepath))


