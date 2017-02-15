# -*- coding: UTF-8 -*-
import header
import re
import pytz
from datetime import datetime
import requests
import copy
import sys
import random
import json
from BeautifulSoup import BeautifulSoup


def login():
    global url_last, config
    class_post = {}
    post_data = {}
    soup = None

    while True:
        try:
            res = requests.get('https://course.fcu.edu.tw/Login.aspx')
            soup = BeautifulSoup(res.text)
        except requests.ConnectionError:
            print"something error"
            break
        captcha = random.randint(1000, 9999)
        for e in soup.findAll('input', {'value': True}):
            post_data[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        post_data['ctl00$Login1$vcode'] = str(captcha)
        post_data['ctl00$Login1$UserName'] = config["account"]
        post_data['ctl00$Login1$Password'] = config["passwd"]
        post_data['ctl00$Login1$RadioButtonList1'] = 'zh-tw'
        cookies = {'CheckCode': str(captcha)}
        r = s.post(url=url, data=post_data, headers=header.header_info, cookies=cookies)
        header.header_info3['Origin'] = str(r.url[:32]).encode('utf-8')
        header.header_info2['Host'] = str(r.url[7:32]).encode('utf-8')
        header.header_info3['Referer'] = str(r.url).encode('utf-8')
        # print r.text
        # try:
        class_soup = BeautifulSoup(r.text)
        for test in class_soup.findAll('form', {'name': 'aspnetForm', 'id': 'aspnetForm'}):
            url_last = test['action']
        for e in class_soup.findAll('input', {'value': True}):
            class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
        class_post = drop_postdata(class_post)
        class_post['ctl00_ToolkitScriptManager1_HiddenField'] = ''
        class_post['ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState'] = 'false'
        class_post['ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
        sample = copy.deepcopy(class_post)
        try:
            choose = r.url.split('?guid=')[0] + url_last
            if r.text.find('驗證碼錯誤') == -1 and r.text.find('帳號或密碼錯誤') == -1 and r.text.find('重新登入') == -1:
                print 'login success'
                break
            else:
                raise Exception
        except Exception:
            class_soup = BeautifulSoup(r.text)
            msg = class_soup.find('span', {'class': 'msg B1'})
            print msg


def get_class():
    global choose, config
    code_list = config["firstchoose"]
    auto = config["autodrop"]
    count = 0
    error = 0
    class_post = {}
    while len(code_list) != 0:
        for code in code_list:
            r = s.get(url=choose, headers=header.header_info)
            class_soup = BeautifulSoup(r.text)
            for e in class_soup.findAll('input', {'value': True}):
                if "name" in e:
                    class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
            class_post = drop_postdata(class_post)
            class_post[
                'ctl00_MainContent_TabContainer1_ClientState'] = '{"ActiveTabIndex":2,"TabState":[true,true,true]}'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub'] = '查詢'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = code
            class_post['ctl00_ToolkitScriptManager1_HiddenField'] = ''
            # print class_post
            r = s.post(url=choose, headers=header.header_info2, data=class_post)
            # print r.text
            class_post.clear()
            class_soup = BeautifulSoup(r.text)
            for e in class_soup.findAll('input', {'value': True}):
                if "name" in e:
                    class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
            # print class_post
            class_post = drop_postdata(class_post)
            class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
            class_post['__EVENTARGUMENT'] = 'selquota$0'
            class_post['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects'] = '1'
            if class_soup.find('input', value='加選') is None:
                print code + ' you have already get it'
                code_list.pop(code_list.index(code))
                break
            # class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID']=''
            r = s.post(url=choose, headers=header.header_info3, data=class_post)
            r.encoding = 'utf-8'
            # print class_post
            class_post.clear()
            class_soup = BeautifulSoup(r.text)
            # print class_soup.findAll('script',text=re.compile("^setTimeout"))
            try:
                number = class_soup.findAll('script', text=re.compile("^setTimeout"))[0]
                number = number.split('：')[1].split('/')[0]
                # setTimeout("alert('剩餘名額/開放名額：1  / 78 ')",200);
                print str(pytz.timezone('Asia/Taipei').fromutc(datetime.utcnow())).split('.')[0].encode('utf-8') + ' ',
                print str(code).encode('utf-8') + '剩餘人數:',
                print str(number).encode('utf-8'),
                print str(code_list).encode('utf-8')
                # number=number.split('：')[1].split('/')[0]
            except:
                print code
            else:
                if int(number) > 0:
                    print "hahahahha"
                    class_soup = BeautifulSoup(r.text)
                    class_post.clear()
                    for e in class_soup.findAll('input', {'value': True}):
                        if e.has_key('name'):
                            class_post[str(e['name'].encode('utf-8'))] = str(e['value'].encode('utf-8'))
                    class_post = drop_postdata(class_post)
                    class_post['__EVENTTARGET'] = 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
                    class_post['__EVENTARGUMENT'] = 'addCourse$0'
                    class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID'] = ''
                    r = s.post(url=choose, headers=header.header_info2, data=class_post)
                    c_info = r.text
                    print r.text
                    if c_info.find('加選成功') != -1 or c_info.find('登記成功') != -1:
                        print 'you get the class ,' + code + ', check it.'
                        code_list.pop(code_list.index(code))
    return True


def drop_postdata(inputdata):
    for i in header.post_pop:
        try:
            inputdata.pop(i)
        except:
            pass
    return inputdata


if __name__ == '__main__':
    reload(sys)
    url = 'https://course.fcu.edu.tw/Login.aspx'
    s = requests.session()
    choose = None
    url_last = None
    config = None
    with open('config.json') as fin:
        config = json.load(fin)
    while True:
        try:
            login()
        except Exception:
            print '連線逾時，嘗試重新登入'
        if get_class():
            break
