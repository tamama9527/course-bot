# -*- coding: UTF-8 -*-
import json

import header
import re
import pytz
from datetime import datetime
import requests
import copy
import random
import sys
from BeautifulSoup import BeautifulSoup


def login():
    global choose, sample, class_post, config
    class_post = {}
    postdata = {}
    soup = None
    while True:
        try:
            res = requests.get('https://course.fcu.edu.tw/Login.aspx')
            soup = BeautifulSoup(res.text)
        except:
            print "something error"
        captcha = random.randint(1000, 9999)
        for e in soup.findAll('input', {'value': True}):
            postdata[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        postdata['ctl00$Login1$vcode'] = str(captcha)
        postdata['ctl00$Login1$UserName'] = config[u"account"].encode('utf-8')
        postdata['ctl00$Login1$Password'] = config[u"passwd"].encode('utf-8')
        postdata['ctl00$Login1$RadioButtonList1'] = 'zh-tw'
        cookies = {'CheckCode': str(captcha)}
        r = s.post(url=url, data=postdata, headers=header.header_info, cookies=cookies)
        header.header_info3['Origin'] = str(r.url[:32]).encode('utf-8')
        header.header_info2['Host'] = str(r.url[7:32]).encode('utf-8')
        header.header_info3['Referer'] = str(r.url).encode('utf-8')
        # print r.text
        # try:
        class_soup = BeautifulSoup(r.text)
        url_last = None
        for test in class_soup.findAll('form', {'name': 'aspnetForm', 'id': 'aspnetForm'}):
            url_last = test['action']
        for e in class_soup.findAll('input', {'value': True}):
            class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        class_post = drop_postdata(class_post)
        class_post['ctl00_ToolkitScriptManager1_HiddenField'] = ''
        class_post['ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState'] = 'false'
        class_post['ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
        sample = copy.deepcopy(class_post)
        msg = None
        try:
            choose = r.url.split('?guid=')[0] + url_last
            pass
        except AttributeError:
            class_soup = BeautifulSoup(r.text)
            msg = class_soup.find('span', {'class': 'msg B1'})
        if r.text.find(u'驗證碼錯誤') == -1 and r.text.find(u'帳號或密碼錯誤') == -1 and r.text.find(u'重新登入') == -1:
            print '登入成功'
            break
        else:
            print '登入失敗'
            print msg


def getclass():
    global class_post, config
    temp = copy.deepcopy(config[u"firstchoose"])
    test_login = None
    class_post = {}
    while len(temp) != 0:
        for i in temp:
            code = i.encode('utf-8')
            r = s.get(url=choose, headers=header.header_info)
            class_soup = BeautifulSoup(r.text)
            for e in class_soup.findAll('input', {'value': True}):
                if 'name' in e:
                    class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
            class_post = drop_postdata(class_post)
            class_post[
                'ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub'] = '查詢'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = code
            class_post['ctl00_ToolkitScriptManager1_HiddenField'] = ''
            r = s.post(url=choose, headers=header.header_info2, data=class_post)
            class_post.clear()
            class_soup = BeautifulSoup(r.text)
            for e in class_soup.findAll('input', {'value': True}):
                if 'name' in e:
                    class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
            class_post = drop_postdata(class_post)
            class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
            class_post['__EVENTARGUMENT'] = 'selquota$0'
            class_post['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects'] = '1'
            if class_soup.find('input', value=u'加選') is None:
                print '你已經有 ' + code + ' 這堂課了！'
                temp.pop(temp.index(code))
                test_login = class_soup.find('span', {'class': 'msg B1'})
                break
            r = s.post(url=choose, headers=header.header_info3, data=class_post)
            r.encoding = 'utf-8'
            class_post.clear()
            class_soup = BeautifulSoup(r.text)
            try:
                number = class_soup.findAll('script', text=re.compile("^setTimeout"))[0]
                number = number.split('：')[1].split('/')[0]
                print str(pytz.timezone('Asia/Taipei').fromutc(datetime.utcnow())).split('.')[0].encode('utf-8') + ' ',
                print str(code).encode('utf-8') + '剩餘人數:',
                print str(number).encode('utf-8'),
                print str(temp).encode('utf-8')
            except:
                print code
            else:
                if int(number) > 0:
                    class_soup = BeautifulSoup(r.text)
                    class_post.clear()
                    for e in class_soup.findAll('input', {'value': True}):
                        if 'name' in e:
                            class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
                    class_post = drop_postdata(class_post)
                    class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
                    class_post['__EVENTARGUMENT'] = 'addCourse$0'
                    class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = ''
                    r = s.post(url=choose, headers=header.header_info2, data=class_post)
                    c_info = r.text
                    print r.text
                    if c_info.find(u'加選成功') != -1 or c_info.find(u'登記成功') != -1:
                        print '你已經選到 ' + code + '，請到課表檢查。'
                        temp.pop(temp.index(code))
    if test_login is not None:
        if test_login.contents[0] == u'您已經在其它地方登入':
            print '您已經在其它地方登入，嘗試幫你重新登入'
            return False
    return True


def drop_postdata(inputdata):
    for i in header.post_pop:
        try:
            inputdata.pop(i)
        except:
            pass
    return inputdata


if __name__ == '__main__':
    class_post = None
    url = 'https://course.fcu.edu.tw/Login.aspx'
    s = requests.session()
    choose = None
    sample = None
    config = None
    with open('config.json') as fin:
        config = json.load(fin)
    if config is None:
        print "Error: 請依據安裝教學建立 config.json"
    else:
        while True:
            try:
                login()
            except:
                print '連線逾時，嘗試重新登入'
            if getclass():
                break
    print '選課完畢！'