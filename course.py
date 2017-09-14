# -*- coding: UTF-8 -*-
import copy
import json
import random
import re
from datetime import datetime
from lxml import html
import pytz
import requests
from BeautifulSoup import BeautifulSoup
import header


def login():
    global choose, class_post, config
    class_post = {}
    post_data = {}
    url_last = None
    msg = None
    class_soup = None
    while True:
        try:
            res = requests.get('https://course.fcu.edu.tw/Login.aspx')
            tree=html.fromstring(res.text)
        except:
            print"something error"
        # 隨機出一個驗證碼
        captcha = random.randint(1000, 9999)
        # 撈出asp.net的預設payload
        #class_post=Search_Pattern(class_soup)
        for i in tree.xpath('//input[@value]'):
            class_post[i.get('name')]=i.get('value')
        # vscode填入產生的驗證碼
        class_post['ctl00$Login1$vcode'] = str(captcha)
        # 從config取得帳號密碼填入
        class_post['ctl00$Login1$UserName'] = config[u"account"]
        class_post['ctl00$Login1$Password'] = config[u"passwd"]
        # 設定語言
        class_post['ctl00$Login1$RadioButtonList1'] = 'zh-tw'
        # 將cookie也填入產生的驗證碼
        cookies = {'CheckCode': str(captcha)}
        # 登入
        res = s.post(url=url, data=class_post, headers=header.header_info, cookies=cookies)
        # 取得header
        header.header_info2['Host'] = str(res.url[7:32]).encode('utf-8')
        tree = html.fromstring(res.text)
        for i in tree.xpath('//form[@name="aspnetForm"][@id="aspnetForm"]'):
            url_last=i.get('action')
        #撈出asp.net的預設payload
        class_post=Search_Pattern(res.text)
        class_post['ctl00_ToolkitScriptManager1_HiddenField'] = ''
        class_post['ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState'] = 'false'
        class_post['ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
        try:
            choose = res.url.split('?guid=')[0] + url_last
        except:
            msg = tree.xpath('//span[@class="msg B1"]/text()')
            #msg = soup.find('span', {'class': 'msg B1'})
        if res.text.find(u'驗證碼錯誤') == -1 and res.text.find(u'帳號或密碼錯誤') == -1 and res.text.find(u'重新登入') == -1:
            print '登入成功'
            break
        else:
            print u'登入失敗：' + msg[0]
            if u'目前不是開放時間' == msg[0]:
                raise NameError


'''
這個function是用來做第一次的確認使用者填入的課程代碼是否已經有了
'''
def check_exist():
    global temp, config, class_post
    class_post = {}
    #取得要搶課的課程代碼
    temp = copy.deepcopy(config[u"firstchoose"])
    print "檢查課程是否已存在"
    for code in temp:
        #先取的當前頁面的資料
        r = s.get(url=choose, headers=header.header_info)
        r.text.encode('utf-8')
        class_post = Search_Pattern(r.text)
        html_str = Search_Class(session=s,search_url=choose,search_header=header.header_info2,post_data=class_post,code=code)
        class_post = {}
        class_post = Search_Pattern(html_str)
        html_str = Add_Class(session=s,add_url=choose,add_header=header.header_info2,post_data=class_post)
        tree = html.fromstring(html_str)
        #檢查是否有已經有這堂課了
        if len(tree.xpath('//p')) != 0 :
            print "你已經有 " + code.encode('utf-8') + " 這堂課了！"
            temp.pop(temp.index(code))
            # test_login = class_soup.find('span', {'class': 'msg B1'})
    print "檢查完畢"


def getclass():
    global class_post, realcode, temp
    realcode = copy.deepcopy(temp)
    #realcode = copy.deepcopy(config[u'firstchoose'])
    # auto = config[u"autodrop"]
    test_login = None
    class_post = {}
    r = s.get(url=choose, headers=header.header_info)
    while len(realcode) != 0:
        for code in realcode:
            class_post=Search_Pattern(r.text)
            html_str = Search_Class(session=s,search_url=choose,search_header=header.header_info2,post_data=class_post,code=code)
            # 餘額檢查
            class_post = {}
            class_post = Search_Pattern(html_str)
            html_str = Number_Class(session=s,num_url=choose,num_header=header.header_info2,post_data=class_post)
            class_soup = BeautifulSoup(html_str)
            try:
                number = unicode(class_soup.find('script', text=re.compile("^setTimeout")))
                number = re.search(u'：(\d+)', number).group(1)
                # setTimeout("alert('剩餘名額/開放名額：1  / 78 ')",200);
                Time_Message = str(pytz.timezone('Asia/Taipei').fromutc(datetime.utcnow())).split('.')[0].encode('utf-8') + ' '
                Code_Message = '選課代碼:' + str(code).encode('utf-8') + ' 剩餘人數:' + number.encode('utf-8') + ' '
                Code_List = '選課名單:' + str([x.encode('utf-8') for x in realcode])
                print Time_Message + Code_Message + Code_List
            except:
                test_login = class_soup.find('span', {'class': 'msg B1'})
                print test_login
                return False
            
            else:
                if int(number) > 0:
                    class_post = {}
                    class_post=Search_Pattern(class_soup)
                    html_str=Add_Class(session=s,add_url=choose,add_header=header.header_info2,post_data=class_post)
                    class_soup = BeautifulSoup(html_str)
                    check_msg = class_soup.find('span', {'class': 'msg A1'})
                    if check_msg is not None:
                        # 如果沒有加選成功 error message在msg B1
                        if check_msg.contents[0] == u'加選成功':
                            print '你已經選到 ' + code.encode('utf-8') + '，請到課表檢查。'
                            realcode.pop(realcode.index(code))
                    else:
                        check_msg = class_soup.find('span', {'class': 'msg B1'})
                        print check_msg.content[0]
    return True

def Search_Pattern(html_text):
    tree = html.fromstring(html_text)
    post={}
    for e in tree.xpath('//input[@value][@type="hidden"]'):
            post[e.get('name')] = e.get('value')
    return post

def Search_Class(session,search_url,search_header,post_data,code):
    post_data['ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
    post_data['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub'] = '查詢'
    post_data['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = code
    r = session.post(url=search_url, headers=search_header, data=post_data)
    return r.text

def Add_Class(session,add_url,add_header,post_data):
    post_data['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
    post_data['__EVENTARGUMENT'] = 'addCourse$0'
    post_data['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = ''
    r = session.post(url=add_url, headers=add_header, data=post_data)
    return r.text

def Number_Class(session,num_url,num_header,post_data):
    class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
    class_post['__EVENTARGUMENT'] = 'selquota$0'
    class_post['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects'] = '1'
    r = s.post(url=num_url, headers=num_header, data=post_data)
    return r.text

if __name__ == '__main__':
    class_post = None
    url = 'https://course.fcu.edu.tw/Login.aspx'
    s = requests.session()
    choose = None
    sample = None
    config = None
    realcode = None
    temp = None
    with open('config.json') as fin:
        config = json.load(fin)
    if config is None:
        print "Error: 請依據安裝教學建立 config.json"
    else:
        while True:
            try:
                login()
            except KeyboardInterrupt:
                print "Bye"
                break
            except NameError:
                break
            except:
                print '連線逾時，嘗試重新登入'
            else:
                try:
                    check_exist()
                    if getclass():
                        break
                except KeyboardInterrupt:
                    print "Bye"
                    break
                else:
                    print '選課完畢！'
