'''
使用面向对象的 类来实现

目标：给按钮添加点击事件

1. 触发关联的函数（方法）
2. 给按钮添加命令属性
'''
from tkinter import *
from tkinter import messagebox
from dao import UserDao
from manage_win import ManageWin

class LoginFrame:

    def __init__(self):
        win = Tk()
        win.title('图书管理员登录')
        win.geometry('400x240+500+100')
        win.resizable(height=True, width=False)


        self.root = win

        frame = Frame(win)
        frame.pack()  # 居中显示

        # grid 网格布局
        Label(frame, text='图书管理员登录', foreground='green', font=('黑体', 26, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        # 绑定变量
        self.username = StringVar()
        self.password = StringVar()

        # 用户账号
        Label(frame, text='账号:', font=('黑体', 15, 'bold')).grid(row=1, column=0, pady=10, padx=10)
        Entry(frame,textvariable=self.username, relief="sunken", borderwidth=1).grid(row=1, column=1, pady=10, padx=8)

        # 用户密码
        Label(frame, text='密码:', font=('黑体', 15, 'bold')).grid(row=2, column=0, pady=10, padx=10)
        Entry(frame,textvariable=self.password, show='*').grid(row=2, column=1, pady=10, padx=8)



        # 按钮
        Button(frame, text='点我登录',command=self.login).grid(row=4, column=0, pady=10, ipadx=8, ipady=2)
        Button(frame, text='退出登录',command=self.quit).grid(row=4, column=1, pady=10, ipadx=8, ipady=2)
        # Button(frame, text='用户注册',command=self.quit).grid(row=4, column=2, pady=10, ipadx=8, ipady=2)

        win.mainloop()

    # 登录判断的方法
    def login(self):
        # 获取用户输入的用户名和密码
        username = self.username.get()
        password = self.password.get()

        userDao = UserDao() # 实例化类
        val = userDao.login(username,password)
        if val == True :  # 验证成功
            messagebox.showinfo(title='提示信息',message='登录成功！')
            # 当前窗口关闭
            self.root.destroy()  # 关闭窗口
            # 打开新的管理界面窗体
            ManageWin()  # 实例化管理界面窗体对象
        else:
            messagebox.showerror(title='出意外了哦！！', message='用户名或密码输入错误！！')

    # 取消登录
    def quit(self):
        self.root.destroy() # 关闭窗口

if __name__ == '__main__':
    login = LoginFrame()