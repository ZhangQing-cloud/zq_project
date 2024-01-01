from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
from jsonutil import BaseJson
from excel_util import ExcelUtil
from tkinter.filedialog import *
import matplotlib
import chineseize_matplotlib  # 导入即可显示中文了
import matplotlib.pyplot as plot
from matplotlib import pylab as plb
from matplotlib import style
import pandas


class ManageWin:
    # 构造方法  初始化
    def __init__(self):
        # 初始化窗体
        win = Tk()
        self.root = win  # 保存实例的属性
        win.title("后台图书管理操作界面")
        win.geometry('500x300+500+100')
        # 初始化菜单
        self.createMenu()
        # 初始化欢迎界面
        # self.createWelcome()
        self.initFrame()

        win.mainloop()  # 阻塞
        # 初始化Frame 把所有的Frame 创建出来

    def initFrame(self):
        self.welcomeFrame = WelcomeFrame(self.root)
        self.listFrame = ListFrame(self.root, self)
        self.aboutFrame = AboutFrame(self.root)
        self.dataFrame = DataFrame(self.root)
        self.addFrame = AddFrame(self.root, self)  # =======================

        self.createWelcome()

    # 初始化菜单
    def createMenu(self):
        menuBar = Menu()  # 菜单栏
        menuBar.add_command(label='图书管理', command=self.showListFrame)
        menuBar.add_command(label='数据分析', command=self.showDataFrame)
        # menuBar.add_command(label='导入导出')

        helpMenu = Menu(tearoff=False)
        helpMenu.add_command(label='关于我', command=self.showAboutFrame)
        helpMenu.add_separator()  # 添加分隔线
        helpMenu.add_command(label='退出系统', command=self.quit)
        menuBar.add_cascade(label='帮助', menu=helpMenu)

        # 添加到菜单栏中
        menuBar.add_command(label='导入', command=self.inport)
        menuBar.add_command(label='导出', command=self.export)

        # self.root['menu'] = menuBar
        self.root.configure(menu=menuBar)  # 把菜单添加到窗口中

    ## 先读入excel --- 合并到 list  ---再写出到json文件
    def inport(self):
        # 打开文件选择器  导入
        filepath = askopenfile(title='打开文件', filetypes=[('Excel文件', '.xlsx')])
        if filepath == None:  # 如果取消了选择
            return
        print(">>>>>>选择的：", filepath)
        # 读取Excel 中数据，并转为 字典格式
        excelData = ExcelUtil.readDict(filepath.name)

        # 再获取原有的json文件中的数据
        # data = self.listFrame.data_dict_list
        data = BaseJson.readJson('books.json')

        # 合并 excel中读入的数据和原有 json 中读入的数据
        data.extend(excelData)

        # 把合并后的数据写出到 books.json 文件中
        BaseJson.saveToJson(data, 'books.json')

    #
    def export(self):
        # 打开文件选择器  导出
        filepath = asksaveasfile(title='保存文件', filetypes=[('Excel文件', '.xlsx')])
        if filepath == None:  # 如果取消了选择
            return
        fliename = filepath.name
        if fliename.endswith('xlsx') == False and fliename.endswith('xls') == False:
            fliename = fliename + '.xlsx'

        print("导出的文件名：", fliename)

        # 读取数据
        data = BaseJson.readJson("books.json")
        ExcelUtil.listToExcel(data, fliename)
        messagebox.showinfo(title="提示信息", message="导出完成！")

    # 退出系统
    def quit(self):
        sel = messagebox.askyesno(title='提示信息', message='您确定退出系统么？')
        if sel == True:
            self.root.destroy()

    # 初始化欢迎界面
    def createWelcome(self):
        self.cur_frame = self.welcomeFrame
        self.cur_frame.pack()

    # 显示列表界面 当点击管理菜单时，调用这里
    def showListFrame(self):
        self.showFrame(self.listFrame)

    def showDataFrame(self):
        self.showFrame(self.dataFrame)

    def showAboutFrame(self):
        self.showFrame(self.aboutFrame)

    def showAddFrame(self):
        self.showFrame(self.addFrame)

    # 切换界面 ===========统一公共的方法========
    def showFrame(self, frame):
        self.cur_frame.pack_forget()
        self.cur_frame = frame  # 当前正在显示的界面
        self.cur_frame.pack()  # 显示现在的当前的界面


# 欢迎界面类
class WelcomeFrame(Frame):  # 继承
    def __init__(self, win):
        super().__init__(win)
        Label(self, text='欢迎进入图书管理系统', foreground='green', font=('黑体', 30, 'bold')).pack(pady=60, ipady=30)


class AboutFrame(Frame):
    def __init__(self, win):
        super().__init__(win)
        Label(self, text='姓名：张庆', foreground='blue', font=('黑体', 20, 'bold')).pack(pady=6, ipady=10)
        Label(self, text='学号：22220055290123', foreground='blue', font=('黑体', 20, 'bold')).pack(pady=6, ipady=10)
        Label(self, text='项目名称：图书管理系统', foreground='blue', font=('黑体', 20, 'bold')).pack(pady=6, ipady=10)
        Label(self, text='所在班级：计算机科学与技术1班', foreground='blue', font=('黑体', 20, 'bold')).pack(pady=6, ipady=10)

class DataFrame(Frame):
    def __init__(self, win):
        super().__init__(win)
        Label(self, text='数据分析界面', foreground='green', font=('黑体', 30, 'bold')).pack(pady=10, ipady=30)
        Button(self, text='出版社发行数量统计', foreground='red', command=self.showPie).pack(ipadx=10)

    # 显示饼图
    def showPie(self):
        matplotlib.use("TkAgg")
        data = BaseJson.readJson('books.json')
        print(data)
        dataFrame = pandas.DataFrame(data)
        v = dataFrame.groupby(['pubcom']).count()  # 按出版社分组统计

        keys = list(v.get('bookname').keys())
        vals = v.get('bookname').values

        # 开始生成饼图
        plot.title('出版社图书数量统计')
        plot.pie(vals, autopct='%.1f%%', labels=keys)
        plot.show()




class ListFrame(Frame):
    def __init__(self, win, manage_win):
        self.manage_win = manage_win  # 保存上一个类 ManageWin 的对象
        super().__init__(win)
        # Label(self, text='列表界面', foreground='green', font=('黑体', 30, 'bold')).pack(pady=60, ipady=30)
        header = ['图书名称', '图书价格', '图书作者', '出版社']

        table = ttk.Treeview(self)
        self.table = table  # ======= 保存到 对象中=======
        table.configure(columns=header, show='headings')

        for item in header:
            table.column(item, width=120, anchor=CENTER)
            table.heading(item, text=item)

        # 加载数据
        self.reload()

        table.grid(row=0, column=0, columnspan=3)

        # ======操作按钮=====
        Button(self, text='添加图书', command=self.manage_win.showAddFrame).grid(row=1, pady=20, column=0)
        Button(self, text='删除图书', command=self.delRow).grid(row=1, column=1)
        Button(self, text='刷新图书', command=self.reload).grid(row=1, column=2)

    def reload(self):
        self.clearAll()
        # 加载数据
        books = BaseJson.readJson('books.json')
        self.data_dict_list = books  # 保存数据
        for book in books:
            lst = list(book.values())
            self.table.insert('', 0, text='', values=lst)

    # 清空表
    def clearAll(self):
        rows = self.table.get_children()
        for row in rows:
            self.table.delete(row)

    # 删除方法
    def delRow(self):
        # 获取选中的记录
        item = self.table.selection()
        if item:
            # 删除
            isok = messagebox.askyesno(title='提醒', message='您确定要删除此记录么？')
            if isok:
                self.delUpdateJson(item)  # 更新文件中数据
                self.table.delete(item)
        else:
            # 未选中
            messagebox.showinfo(title='提示信息', message='请选择一条记录！！！')

    def delUpdateJson(self, item):
        xx = self.table.item(item, 'values')  # 获取选中的记录（列表）
        for x in self.data_dict_list:  # 从存储的数据模型中遍历查找要删除的记录
            print('>>>>====', x)
            if xx[0] == x['bookname']:
                yy = self.data_dict_list.remove(x)
                print('成功了', yy)
        BaseJson.saveToJson(self.data_dict_list, 'books.json')
    # 添加界面


class AddFrame(Frame):
    def __init__(self, win, manage_win):
        super().__init__(win)
        self.manage_win = manage_win
        self.bookname = StringVar()
        self.author = StringVar()
        self.price = DoubleVar()
        self.pubcom = StringVar()

        Label(self, text='添加图书', foreground='green', font=('宋体', 23, 'bold')).grid(row=0, columnspan=2, column=0,
                                                                                       pady=10, ipady=5)

        Label(self, text='图书名称：').grid(row=1, column=0, padx=10)
        Entry(self, width=30, textvariable=self.bookname).grid(row=1, column=1, pady=10)

        Label(self, text='图书作者：').grid(row=2, column=0, padx=10)
        Entry(self, width=30, textvariable=self.author).grid(row=2, column=1, pady=10)

        Label(self, text='图书价格：').grid(row=3, column=0, padx=10)
        Entry(self, width=30, textvariable=self.price).grid(row=3, column=1, pady=10)

        Label(self, text='出 版 社：').grid(row=4, column=0, padx=10)
        Entry(self, width=30, textvariable=self.pubcom).grid(row=4, column=1, pady=10)

        Button(self, text='保存图书', command=self.save).grid(row=5, column=0)
        Button(self, text='取消返回', command=self.manage_win.showListFrame).grid(row=5, column=1)

    def save(self):
        # 保存数据
        # 获取输入框中的值
        bookname = self.bookname.get()
        price = self.price.get()
        author = self.author.get()
        pubcom = self.pubcom.get()
        print(bookname, price)

        book = {}  # 空字典
        book['bookname'] = bookname  # 键值对
        book['price'] = price
        book['author'] = author
        book['pubcom'] = pubcom

        # 第一个参数book 就是一个字典对象，存储了输入的信息  第二个参数是保存的文件名字
        BaseJson.appendToJson(book, 'books.json')
        messagebox.showinfo(title='提示信息', message='保存成功！')

        # 清空
        self.bookname.set('')
        self.price.set(0)
        self.author.set('')
        self.pubcom.set('')


if __name__ == '__main__':
    ManageWin()  # 自动调用构造方法
