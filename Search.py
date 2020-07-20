import smtplib
import string
import tkinter.messagebox
import webbrowser
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from random import randint
from tkinter import *
from tkinter.ttk import *
from urllib.parse import quote

window = Tk()
window.title('查询工具')
window.geometry('500x110')
username_Frame = Frame()
pwd_Frame = Frame()
login_and_signup_Frame = Frame()
please_login_first_Label = Label(window, text='请先登录！')
please_login_first_Label.pack()
username_Label = Label(username_Frame, text='用户名：', )
pwd_Label = Label(pwd_Frame, text='密码：', )
username_Entry = Entry(username_Frame)
pwd_Entry = Entry(pwd_Frame, show='*')
login = False


def database_users():
    users_file = open('Users', 'r')
    now = users_file.readline().strip().split('+')
    users_dict = dict()
    while len(now) != 1:
        users_dict[now[0]] = [now[1], now[2]]
        now = users_file.readline().strip().split('+')
    return users_dict


def forgot(email, email_test):
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


def generate():
    email_test = ''
    for m in range(6):
        email_test += str(randint(0, 9))
    return email_test


def send():
    window_forgot = Toplevel(window)
    window_forgot.geometry('300x50')
    window_forgot.title('忘记密码')

    def confirm():
        global password_
        user = database_users()
        emails = list()
        for email in user.values():
            emails.append(email[1])
        if em1.get() not in emails:
            tkinter.messagebox.showerror('警告⚠️', '此邮箱未注册！')
        else:
            def _format_addr(s):
                name, addr = parseaddr(s)
                return formataddr((Header(name, 'utf-8').encode(), addr))

            for key in user.keys():
                if user[key][1] == em1.get():
                    password_ = user[key][0]
            from_addr = 'marioliang0704@qq.com'
            password = 'bfjzclbewveeebii'
            to_addr = em1.get()
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

    em = Label(window_forgot, text='邮箱：', )
    em1 = Entry(window_forgot)
    emts = Button(window_forgot, text='获取', command=confirm)
    em.place(x=33, y=15)
    em1.place(x=75, y=15)
    emts.place(x=250, y=20)


def log():
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
        tkinter.messagebox.showerror('警告⚠️', '️登录失败，请检查用户名或密码是否正确！')
        login = False


def sign_up():
    email_test = generate()

    def confirm():
        user = database_users()
        emails = list()
        for email in user.values():
            emails.append(email[1])
        if u1.get() in user.keys():
            tkinter.messagebox.showerror('警告⚠️', '️此用户名已存在！')
        elif '+' in u1.get():
            tkinter.messagebox.showerror('警告⚠️', '️用户名不能包含加号！')
        elif '+' in p1.get():
            tkinter.messagebox.showerror('警告⚠️', '️密码不能包含加号！')
        elif p1.get() != cp1.get():
            tkinter.messagebox.showerror('警告⚠️', '️请输入正确的密码！')
        elif u1.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '用户名不能为空！')
        elif p1.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '密码不能为空！')
        elif em1.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '邮箱不能为空！')
        elif em1.get() in emails:
            tkinter.messagebox.showerror('警告⚠️', '此邮箱已被其他用户使用！')
        elif '@' not in em1.get() or '.' not in em1.get():
            tkinter.messagebox.showerror('警告⚠️', '请输入正确的邮箱！')
        elif et1.get() != email_test:
            tkinter.messagebox.showerror('警告⚠️', '请输入正确的验证码！')
        else:
            tkinter.messagebox.showinfo('', '注册成功！请您重新登录！')
            users = open('Users', 'a', encoding='utf-8')
            users.write(u1.get() + '+' + p1.get() + '+' + em1.get() + '\n')
            window_sign_up.destroy()

    def get_emts():
        user = database_users()
        emails = list()
        for email in user.values():
            emails.append(email[1])
        if em1.get() is '':
            tkinter.messagebox.showerror('警告⚠️', '邮箱不能为空！')
        elif em1.get() in emails:
            tkinter.messagebox.showerror('警告⚠️', '此邮箱已被其他用户使用！')
        elif '@' not in em1.get():
            tkinter.messagebox.showerror('警告⚠️', '请输入正确的邮箱！')
        else:
            forgot(em1.get(), email_test)

    window_sign_up = Toplevel(window)
    window_sign_up.geometry('300x220')
    window_sign_up.title('注册窗口')
    u = Label(window_sign_up, text='用户名：', )
    p = Label(window_sign_up, text='密码：', )
    cp = Label(window_sign_up, text='确认密码：', )
    em = Label(window_sign_up, text='邮箱：', )
    et = Label(window_sign_up, text='验证码：', )
    u1 = Entry(window_sign_up)
    p1 = Entry(window_sign_up, show='*')
    cp1 = Entry(window_sign_up, show='*')
    button = Button(window_sign_up, text='注册', command=confirm)
    em1 = Entry(window_sign_up)
    emts = Button(window_sign_up, text='获取', command=get_emts)
    et1 = Entry(window_sign_up)
    u.place(x=20, y=15)
    et.place(x=20, y=155)
    p.place(x=33, y=50)
    cp.place(x=7, y=85)
    em.place(x=33, y=120)
    u1.place(x=75, y=15)
    p1.place(x=75, y=50)
    cp1.place(x=75, y=85)
    em1.place(x=75, y=120)
    et1.place(x=75, y=155)
    button.place(x=135, y=190)
    emts.place(x=250, y=160)


def search():
    def search_res():
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
    search_Entry.pack()
    search_Button.pack()
    option.pack()


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

username_Frame.pack()
pwd_Frame.pack()
login_and_signup_Frame.pack()
window.mainloop()
