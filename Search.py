# 搜索页 OK
# 主页 OK
# 注册页
# 忘记密码页
# 老王牛逼不？
import platform
import smtplib
import string
import time
import tkinter.messagebox
import webbrowser
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from tkinter import *

import jieba

if platform.system() == 'Windows':
    from tkinter.ttk import *

smart_search = False


def smart_search_setting(_=None):
    global smart_search
    smart_search = not smart_search


signup_time_global = None
forget_time_global = None
signup_wait = 60
forget_wait = 60

# from tkinter.ttk import *
from urllib.parse import quote

window = Tk()
window.title('查询工具')
username_Frame = Frame()
pwd_Frame = Frame()
login_and_signup_Frame = Frame()
please_login_first_Label = Label(window, text='请先登录！')
please_login_first_Label.pack()
username_Label = Label(username_Frame, text='账号：', )
pwd_Label = Label(pwd_Frame, text='密码：', )
username_Entry = Entry(username_Frame)
pwd_Entry = Entry(pwd_Frame, show='*')
login = False


def database_users():
    users_file = open('Users', 'r', encoding='utf-8')
    users_file_read = users_file.read().strip().split("\n")
    users_dict = dict()
    for x in users_file_read:
        now = x.strip().split('+')
        if len(now) == 3:
            if "#" in now[0]:
                continue
            if "//" in now[0]:
                continue
            users_dict[now[0]] = [now[1], now[2]]
    return users_dict


def forgot(email, email_test):
    global signup_time_global
    if signup_time_global is None or signup_time_global - time.time() > signup_wait:
        signup_time_global = time.time()
    else:
        tkinter.messagebox.showerror('警告⚠️', '你太快了！\n爪巴！')
        return False

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    from_addr = 'marioliang0704@qq.com'
    password = 'bfjzclbewveeebii'
    to_addr = email
    smtp_server = 'smtp.qq.com'
    msg = MIMEText('您的验证码为{}'.format(str(email_test)), 'plain', 'utf-8')
    msg['From'] = _format_addr('验证码<%s>' % from_addr)
    msg['To'] = _format_addr('<%s>' % to_addr)
    msg['Subject'] = Header('验证码', 'utf-8').encode()
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    tkinter.messagebox.showinfo('', '验证码已发送！')


def generate(email):
    return str(abs(hash(email)))[int(str(abs(hash(email)))[0])] + \
           str(abs(hash(email)))[int(str(abs(hash(email)))[1])] + \
           str(abs(hash(email)))[int(str(abs(hash(email)))[2])] + \
           str(abs(hash(email)))[int(str(abs(hash(email)))[3])] + \
           str(abs(hash(email)))[int(str(abs(hash(email)))[4])] + \
           str(abs(hash(email)))[int(str(abs(hash(email)))[5])]


def send(_=None):
    window_forgot = Toplevel(window)
    window_forgot.geometry('300x50')
    window_forgot.title('忘记密码')

    def confirm(_=None):
        global forget_time_global, password_
        user = database_users()
        emails = list()
        for email in user.values():
            emails.append(email[1])
        if email_forget_Entry.get() not in emails:
            tkinter.messagebox.showerror('警告⚠️', '此邮箱未注册！')
        else:
            if forget_time_global is None or forget_time_global - time.time() > forget_wait:
                forget_time_global = time.time()
            else:
                tkinter.messagebox.showerror('警告⚠️', '你太快了！\n爪巴！')
                return False

            def _format_addr(s):
                name, addr = parseaddr(s)
                return formataddr((Header(name, 'utf-8').encode(), addr))

            for key in user.keys():
                if user[key][1] == email_forget_Entry.get():
                    password_ = user[key][0]
            from_addr = 'marioliang0704@qq.com'
            password = 'bfjzclbewveeebii'
            to_addr = email_forget_Entry.get()
            smtp_server = 'smtp.qq.com'
            msg = MIMEText('您的密码为{}'.format(password_), 'plain', 'utf-8')
            msg['From'] = _format_addr('密码<%s>' % from_addr)
            msg['To'] = _format_addr('<%s>' % to_addr)
            msg['Subject'] = Header('密码', 'utf-8').encode()
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
            server.quit()
            tkinter.messagebox.showinfo('', '您的密码已发送到您的邮箱中！')
            window_forgot.destroy()

    email_forget_Label = Label(window_forgot, text='邮箱：', )
    email_forget_Entry = Entry(window_forgot)
    email_forget_Entry.bind("<Return>", confirm)
    forget_Button = Button(window_forgot, text='获取', command=confirm)
    email_forget_Label.pack(side=LEFT)
    email_forget_Entry.pack(side=LEFT)
    forget_Button.pack(side=LEFT)


def log(_=None):
    global login
    user = database_users()
    if username_Entry.get() in user.keys() and pwd_Entry.get() == user[username_Entry.get()][0]:
        tkinter.messagebox.showinfo('', '登录成功！')
        login = True
        if login is True:
            please_login_first_Label.pack_forget()
            username_Label.pack_forget()
            pwd_Label.pack_forget()
            username_Entry.pack_forget()
            pwd_Entry.pack_forget()
            login_Button.pack_forget()
            signup_Button.pack_forget()
            pwd_forget_Button.pack_forget()
            search()
    else:
        tkinter.messagebox.showerror('警告⚠️', '️登录失败，请检查账号或密码是否正确！')
        login = False


def sign_up(_=None):
    def confirm(_=None):
        user = database_users()
        emails = list()
        for email in user.values():
            emails.append(email[1])
        if username_reg_Entry.get() in user.keys():
            tkinter.messagebox.showerror('警告⚠️', '️此账号已存在！')
        elif '+' in username_reg_Entry.get():
            tkinter.messagebox.showerror('警告⚠️', '️账号不能包含加号！')
        elif '+' in pwd_reg_Entry.get():
            tkinter.messagebox.showerror('警告⚠️', '️密码不能包含+！')
        elif '#' in pwd_reg_Entry.get():
            tkinter.messagebox.showerror('警告⚠️', '️密码不能包含#！')
        elif '/' in pwd_reg_Entry.get():
            tkinter.messagebox.showerror('警告⚠️', '️密码不能包含/！')
        elif pwd_reg_Entry.get() != pwd_twice_reg_Entry.get():
            tkinter.messagebox.showerror('警告⚠️', '️请输入正确的密码！')
        elif username_reg_Entry.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '账号不能为空！')
        elif pwd_reg_Entry.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '密码不能为空！')
        elif email_reg_Entry.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '邮箱不能为空！')
        elif email_reg_Entry.get() in emails:
            tkinter.messagebox.showerror('警告⚠️', '此邮箱已被其他用户使用！')
        elif '@' not in email_reg_Entry.get() or '.' not in email_reg_Entry.get():
            tkinter.messagebox.showerror('警告⚠️', '请输入正确的邮箱！')
        elif captcha_Entry.get() != generate(email_reg_Entry.get()):
            tkinter.messagebox.showerror('警告⚠️', '请输入正确的验证码！')
        else:
            tkinter.messagebox.showinfo('', '注册成功！请您重新登录！')
            users = open('Users', 'a', encoding='utf-8')
            users.write(username_reg_Entry.get() + '+' + pwd_reg_Entry.get() + '+' + email_reg_Entry.get() + '\n')
            window_sign_up.destroy()

    def get_emts(_=None):
        user = database_users()
        emails = list()
        for email in user.values():
            emails.append(email[1])
        if email_reg_Entry.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '邮箱不能为空！')
        elif email_reg_Entry.get() in emails:
            tkinter.messagebox.showerror('警告⚠️', '此邮箱已被其他用户使用！')
        elif '@' not in email_reg_Entry.get() or '.' not in email_reg_Entry.get():
            tkinter.messagebox.showerror('警告⚠️', '请输入正确的邮箱！')
        else:
            forgot(email_reg_Entry.get(), generate(email_reg_Entry.get()))

    window_sign_up = Toplevel(window)
    window_sign_up.geometry('300x220')
    window_sign_up.title('注册窗口')
    username_reg_Frame = Frame(window_sign_up)
    pwd_reg_Frame = Frame(window_sign_up)
    pwd_twice_reg_Frame = Frame(window_sign_up)
    email_reg_Frame = Frame(window_sign_up)
    captcha_reg_Frame = Frame(window_sign_up)
    username_reg_Label = Label(username_reg_Frame, text='账号：')
    pwd_reg_Label = Label(pwd_reg_Frame, text='密码：')
    pwd_twice_reg_Label = Label(pwd_twice_reg_Frame, text='确认：')
    email_reg_Label = Label(email_reg_Frame, text='邮箱：', )
    captcha_Label = Label(captcha_reg_Frame, text='验证码：', )
    username_reg_Entry = Entry(username_reg_Frame)
    pwd_reg_Entry = Entry(pwd_reg_Frame, show='*')
    pwd_twice_reg_Entry = Entry(pwd_twice_reg_Frame, show='*')
    reg_Button = Button(window_sign_up, text='注册', command=confirm)
    email_reg_Entry = Entry(email_reg_Frame)
    captcha_get_Button = Button(window_sign_up, text='获取验证码', command=get_emts)
    captcha_Entry = Entry(captcha_reg_Frame)
    # username_reg_Label.place(x=20, y=15)
    # captcha_Label.place(x=20, y=155)
    # pwd_reg_Label.place(x=33, y=50)
    # pwd_twice_reg_Label.place(x=7, y=85)
    # email_reg_Label.place(x=33, y=120)
    # username_reg_Entry.place(x=75, y=15)
    # pwd_reg_Entry.place(x=75, y=50)
    # pwd_twice_reg_Entry.place(x=75, y=85)
    # email_reg_Entry.place(x=75, y=120)
    # captcha_Entry.place(x=75, y=155)
    # reg_Button.place(x=135, y=190)
    # captcha_get_Button.place(x=250, y=160)

    username_reg_Label.pack(side=LEFT)
    username_reg_Entry.pack(side=LEFT)
    captcha_Label.pack(side=LEFT)
    captcha_Entry.pack(side=LEFT)
    pwd_reg_Label.pack(side=LEFT)
    pwd_reg_Entry.pack(side=LEFT)
    pwd_twice_reg_Label.pack(side=LEFT)
    pwd_twice_reg_Entry.pack(side=LEFT)
    email_reg_Label.pack(side=LEFT)
    email_reg_Entry.pack(side=LEFT, fill="x")

    username_reg_Frame.pack(anchor="w")
    pwd_reg_Frame.pack(anchor="w")
    pwd_twice_reg_Frame.pack(anchor="w")
    email_reg_Frame.pack(anchor="w")
    captcha_get_Button.pack(anchor="w", fill="x")

    captcha_reg_Frame.pack(anchor="w")
    reg_Button.pack(anchor="w", fill="x")
    username_reg_Entry.bind("<Return>", confirm)
    pwd_reg_Entry.bind("<Return>", confirm)
    pwd_twice_reg_Entry.bind("<Return>", confirm)
    email_reg_Entry.bind("<Return>", get_emts)
    captcha_Entry.bind("<Return>", confirm)
def search():
    def search_res(_=None):
        global url
        s = var.get()
        if s == 'Baidu':
            url = 'https://www.baidu.com/s?ie=UTF-8&wd='
        if s == 'Google':
            url = 'https://www.google.com/search?newwindow=1&safe=active&sxsrf=ALeKk01Rbl78lS2qKRulGUqbsPsvAwyrmw' \
                  '%3A1594884595904&source=hp&ei=8wEQX4voNMu3ggejsJKIDQ&q='
        if s == 'Bing(China)' or s == 'Bing(International)':
            url = 'https://cn.bing.com/search?q='
        if s == 'Baidubaike':
            url = 'https://baike.baidu.com/search?word='
        if s == 'Wikipedia':
            url = 'https://wikipedia.org/w/index.php?search='
        if s == 'DuckDuckGo':
            url = 'https://duckduckgo.com/?q='
        if s == 'Youtube':
            url = 'https://www.youtube.com/results?search_query='
        if s == 'Facebook':
            url = 'https://www.facebook.com/search/top/?q='
        if s == 'Weibo':
            url = 'https://s.weibo.com/weibo?q='
        if s == 'CSDN':
            url = 'https://so.csdn.net/so/search/s.do?q='
        if s == 'Amazon':
            url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='
        if s == 'Taobao':
            url = 'https://s.taobao.com/search?q='
        if smart_search:
            words = str(" ".join(jieba.cut_for_search(search_Entry.get(), HMM=True))).split()
        else:
            words = str(search_Entry.get()).split()
        for w in words:
            url += w
            if len(words) > 1:
                url += '+'
        if s == 'Google':
            url += '&gs_lcp' \
                   '=CgZwc3ktYWIQAzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzI' \
                   'HCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJ1DLBlihEmDtE2gBcAB4AIABAIgBAJIBAJgBAKABAao' \
                   'BB2d3cy13aXqwAQo&sclient=psy-ab&ved=0ahUKEwjLra2OoNHqAhXLm-AKHSOYBNEQ4dUDCAk&uact=5'
        if s == 'Bing(China)':
            url += '&FORM=BESBTB&ensearch=0'
        if s == 'Bing(International)':
            url += '&FORM=BESBTB&ensearch=1'
        web = quote(url, safe=string.printable)
        webbrowser.open_new(web)
        url = ''

    var = StringVar(window)
    var.set("Baidu")
    search_tips_Label = Label(window, text='请输入您要搜寻的内容：')
    search_tips_Label.pack()
    search_Entry = Entry(window, width=50)
    search_Button = Button(window, text='搜索', command=search_res)
    option = OptionMenu(window, var, 'Baidu', 'Baidubaike', 'Bing(China)',
                        'Bing(International)', 'Google', 'Taobao',
                        'DuckDuckGo', 'Wikipedia', 'CSDN',
                        'Youtube', 'Facebook', 'Weibo', 'Amazon')
    smart_search_Checkbutton = Checkbutton(text="智能搜索", command=smart_search_setting)
    search_Entry.pack()
    search_Button.pack()
    option.pack()
    smart_search_Checkbutton.pack()
    search_Entry.bind("<Return>", search_res)

    # menu = Menu(window)
    # special_method = Menu(menu, tearoff=0)
    # menu.add_cascade(label="功能", menu=special_method)
    #
    # special_method.add_checkbutton(label="启用智能搜索", command=smart_search_setting)
    # window.config(menu=menu)
login_Button = Button(login_and_signup_Frame, text='登录', command=log)
pwd_forget_Button = Button(login_and_signup_Frame, text='忘记密码？', command=send)
signup_Button = Button(login_and_signup_Frame, text='注册', command=sign_up)
login_Button.pack(side=LEFT)
pwd_forget_Button.pack(side=LEFT)
signup_Button.pack(side=RIGHT)
username_Entry.pack(side=RIGHT)
username_Label.pack(side=LEFT)
pwd_Entry.pack(side=RIGHT)
pwd_Label.pack(side=LEFT)
username_Entry.bind("<Return>", log)
pwd_Entry.bind("<Return>", log)
username_Frame.pack()
pwd_Frame.pack()
login_and_signup_Frame.pack()
window.mainloop()
