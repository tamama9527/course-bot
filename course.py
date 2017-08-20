# -*- coding: UTF-8 -*-
import copy
import json
import random
import re
from datetime import datetime

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
    soup = None
    while True:
        try:
            res = requests.get('https://course.fcu.edu.tw/Login.aspx')
            soup = BeautifulSoup(res.text)
        except:
            print"something error"
        #隨機出一個驗證碼
        captcha = random.randint(1000, 9999)
        #撈出asp.net的預設payload
        for e in soup.findAll('input', {'value': True}):
            post_data[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        #vscode填入產生的驗證碼
        post_data['ctl00$Login1$vcode'] = str(captcha)
        #從config取得帳號密碼填入
        post_data['ctl00$Login1$UserName'] = config[u"account"]
        post_data['ctl00$Login1$Password'] = config[u"passwd"]
        #設定語言
        post_data['ctl00$Login1$RadioButtonList1'] = 'zh-tw'
        #將cookie也填入產生的驗證碼
        cookies = {'CheckCode': str(captcha)}
        #登入
        res = s.post(url=url, data=post_data, headers=header.header_info, cookies=cookies)
        #取得header
        ##有優化的可能！！！！
        header.header_info3['Origin'] = str(res.url[:32]).encode('utf-8')
        header.header_info2['Host'] = str(res.url[7:32]).encode('utf-8')
        header.header_info3['Referer'] = str(res.url).encode('utf-8')
        soup = BeautifulSoup(res.text)
        for test in soup.findAll('form', {'name': 'aspnetForm', 'id': 'aspnetForm'}):
            url_last = test['action']
        #撈出asp.net的預設payload
        for e in soup.findAll('input', {'value': True, 'type': 'hidden'}):
            class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        class_post['ctl00_ToolkitScriptManager1_HiddenField'] = ''
        class_post['ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState'] = 'false'
        class_post['ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
        try:
            choose = res.url.split('?guid=')[0] + url_last
        except:
            msg = soup.find('span', {'class': 'msg B1'})
        if res.text.find(u'驗證碼錯誤') == -1 and res.text.find(u'帳號或密碼錯誤') == -1 and res.text.find(u'重新登入') == -1:
            print '登入成功'
            break
        else:
            print '登入失敗：' + str(msg.contents[0])
            if '目前不是開放時間' == str(msg.contents[0]):
                raise NameError

def check_exist():
    global temp, config, class_post
    class_post = {}
    temp = copy.deepcopy(config[u"firstchoose"])

    print "檢查課程是否已存在"
    for code in temp:
        r = s.get(url=choose, headers=header.header_info)
        r.text.encode('utf-8')
        class_soup = BeautifulSoup(r.text)
        for e in class_soup.findAll('input', {'value': True, 'type': 'hidden'}):
            class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        class_post['ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
        class_post['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub'] = '查詢'
        class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = code
        # class_post['ctl00_ToolkitScriptManager1_HiddenField']=''
        r = s.post(url=choose, headers=header.header_info2, data=class_post)
        class_soup = BeautifulSoup(r.text)
        class_post = {}
        for e in class_soup.findAll('input', {'value': True, 'type': 'hidden'}):
            class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
        class_post['__EVENTARGUMENT'] = 'addCourse$0'
        class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = ''
        r = s.post(url=choose, headers=header.header_info2, data=class_post)
        class_soup = BeautifulSoup(r.text)
        if class_soup.find('p') is not None:
            print "你已經有 " + code.encode('utf-8') + " 這堂課了！"
            temp.pop(temp.index(code))
            # test_login = class_soup.find('span', {'class': 'msg B1'})
    print "檢查完畢"


def getclass():
    global class_post, realcode, temp
    realcode = copy.deepcopy(temp)
    # auto = config[u"autodrop"]
    test_login = None
    class_post = {}
    r = s.get(url=choose, headers=header.header_info)
    class_soup = BeautifulSoup(r.text)
    while len(realcode) != 0:
        for code in realcode:
            for e in class_soup.findAll('input', {'value': True, 'type': 'hidden'}):
                class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
            class_post[
                'ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub'] = '查詢'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = code
            r = s.post(url=choose, headers=header.header_info2, data=class_post)
            # 餘額檢查
            class_post = {}
            class_soup = BeautifulSoup(r.text)
            for e in class_soup.findAll('input', {'value': True, 'type': 'hidden'}):
                class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
            class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
            class_post['__EVENTARGUMENT'] = 'selquota$0'
            class_post['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects'] = '1'
            r = s.post(url=choose, headers=header.header_info3, data=class_post)
            class_post = {}
            class_soup = BeautifulSoup(r.text)
            try:
                number = unicode(class_soup.find('script', text=re.compile("^setTimeout")))
                number = re.search(u'：(\d+)', number).group(1)
                # setTimeout("alert('剩餘名額/開放名額：1  / 78 ')",200);
                a = str(pytz.timezone('Asia/Taipei').fromutc(datetime.utcnow())).split('.')[0].encode('utf-8') + ' '
                b = '選課代碼:' + str(code).encode('utf-8') + ' 剩餘人數:' + number.encode('utf-8') + ' '
                c = '搶課名單:' + str([x.encode('utf-8') for x in realcode])
                print a + b + c
            except:
                test_login = class_soup.find('span', {'class': 'msg B1'})
                print code
                break
            else:
                if int(number) > 0:
                    class_soup = BeautifulSoup(r.text)
                    class_post = {}
                    for e in class_soup.findAll('input', {'value': True, 'type': 'hidden'}):
                        class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
                    class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
                    class_post['__EVENTARGUMENT'] = 'addCourse$0'
                    class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = ''
                    r = s.post(url=choose, headers=header.header_info2, data=class_post)
                    class_soup = BeautifulSoup(r.text)
                    check_msg = class_soup.find('span', {'class': 'msg A1'})
                    if check_msg.contents[0] != u'本科目名額目前已額滿 !':
                        print '你已經選到 ' + code.encode('utf-8') + '，請到課表檢查。'
                        realcode.pop(realcode.index(code))
        if test_login is not None:
            if test_login.contents[0] == '您已經在其它地方登入':
                print '您已經在其它地方登入，嘗試幫你重新登入'
                return False
    return True


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
