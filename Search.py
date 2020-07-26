# 搜索页 OK
# 主页 OK
# 注册页
# 忘记密码页
# 老王牛逼不？
import platform
import string
import webbrowser
from tkinter import *

import jieba

jieba.enable_paddle()
if platform.system() == 'Windows':
    from tkinter.ttk import *

smart_search = False


def smart_search_setting(_=None):
    global smart_search
    smart_search = not smart_search


# from tkinter.ttk import *
from urllib.parse import quote

window = Tk()



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
search()
window.mainloop()
