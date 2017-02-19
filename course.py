#-*- coding: UTF-8 -*- 
import header
import re
import pytz
from datetime import datetime
import requests
import copy
import sys
import  random
import getpass
from BeautifulSoup import BeautifulSoup
import time
global class_post
url='https://course.fcu.edu.tw/Login.aspx'
global s
s=requests.session()
realcode=None
temp=None
def login():
    global choose
    class_post={}
    postdata={}
    while True:
        try:
            res=requests.get('https://course.fcu.edu.tw/Login.aspx')
            soup = BeautifulSoup(res.text)
        except :
            print"something error"
        captcha=random.randint(1000,9999)
        for e in soup.findAll('input',{'value': True}):
            postdata[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
        postdata['ctl00$Login1$vcode']=str(captcha)
        postdata['ctl00$Login1$UserName']=header.account
        postdata['ctl00$Login1$Password']=header.passwd
        postdata['ctl00$Login1$RadioButtonList1']='zh-tw'
        cookies={ 'CheckCode':str(captcha)}
        r=s.post(url=url,data=postdata,headers=header.header_info,cookies=cookies)
        header.header_info3['Origin']=str(r.url[:32]).encode('utf-8')
        header.header_info2['Host']=str(r.url[7:32]).encode('utf-8')
        header.header_info3['Referer']=str(r.url).encode('utf-8')
        #print r.text
        #try:
        class_soup=BeautifulSoup(r.text)
        for test in  class_soup.findAll('form',{'name':'aspnetForm','id':'aspnetForm'}):
            url_last=test['action']
        for e in class_soup.findAll('input',{'value':True}):
            class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
        class_post=drop_postdata(class_post)
        class_post['ctl00_ToolkitScriptManager1_HiddenField']=''
        class_post['ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState']='false'
        class_post['ctl00_MainContent_TabContainer1_ClientState']='{"ActiveTabIndex":2,"TabState":[true,true,true]}'
        try:
            choose=r.url.split('?guid=')[0]+url_last
        except:
            class_soup=BeautifulSoup(r.text)
            msg=class_soup.find('span',{'class':'msg B1'})
        '''except:
            print 'server error' '''
        if r.text.find('驗證碼錯誤')==-1 and r.text.find('帳號或密碼錯誤')==-1 and r.text.find('重新登入')==-1:
            print 'login success'
            break;
        else:
            print msg
def check_exist():
    global temp
    class_post={}
    temp=copy.deepcopy(header.firstchoose)
    print "檢查課程是否已存在"
    for code in temp:
        r=s.get(url=choose,headers=header.header_info)
        class_soup=BeautifulSoup(r.text)
        for e in class_soup.findAll('input',{'value': True}):
            if e.has_key('name'):
                class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
        class_post=drop_postdata(class_post)
        class_post['ctl00_MainContent_TabContainer1_ClientState']='{"ActiveTabIndex":2,"TabState":[true,true,true]}'
        class_post['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub']='查詢'
        class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID']=code
        class_post['ctl00_ToolkitScriptManager1_HiddenField']=''
        r=s.post(url=choose,headers=header.header_info2,data=class_post)
        class_soup=BeautifulSoup(r.text)
        class_post.clear()
        for e in class_soup.findAll('input',{'value': True}):
            if e.has_key('name'):
                class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
        class_post=drop_postdata(class_post)
        class_post['__EVENTTARGET']='ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
        class_post['__EVENTARGUMENT']='addCourse$0'
        class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID']=''
        r=s.post(url=choose,headers=header.header_info2,data=class_post)
        r.encoding='utf-8'
        class_soup=BeautifulSoup(r.text)
        if class_soup.find('p') != None:
            print "You already have this "+code
            temp.pop(temp.index(code))
            test_login = class_soup.find('span',{'class':'msg B1'})
    print "檢查完畢"
def getclass():
    realcode=copy.deepcopy(temp)
    auto=header.autodrop
    test_login=None
    count=0
    error=0
    class_post={}
    while len(realcode)!=0:
        for code in realcode:
            r=s.get(url=choose,headers=header.header_info)
            class_soup=BeautifulSoup(r.text)
            for e in class_soup.findAll('input',{'value': True}):
                if e.has_key('name'):
                    class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
            class_post=drop_postdata(class_post)
            class_post['ctl00_MainContent_TabContainer1_ClientState']='{"ActiveTabIndex":2,"TabState":[true,true,true]}'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub']='查詢'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID']=code
            class_post['ctl00_ToolkitScriptManager1_HiddenField']=''
            #print class_post
            r=s.post(url=choose,headers=header.header_info2,data=class_post)
            #餘額檢查
            class_post.clear()
            class_soup = BeautifulSoup(r.text)
            for e in class_soup.findAll('input',{'value': True}):
                if e.has_key('name'):
                    class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
            class_post=drop_postdata(class_post)
            class_post['__EVENTTARGET']='ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
            class_post['__EVENTARGUMENT']='selquota$0'
            class_post['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects']='1'   
            r=s.post(url=choose,headers=header.header_info3,data=class_post)
            r.encoding='utf-8'
            class_post.clear()
            class_soup=BeautifulSoup(r.text)
            try:
                number= class_soup.find('script',text=re.compile("^setTimeout"))
                number=number.split('：')[1].split('/')[0]
                #setTimeout("alert('剩餘名額/開放名額：1  / 78 ')",200);
                print str(pytz.timezone('Asia/Taipei').fromutc(datetime.utcnow())).split('.')[0].encode('utf-8')+' ',
                print str(code).encode('utf-8')+'剩餘人數:',
                print str(number).encode('utf-8'),
                print str(realcode).encode('utf-8')
            except:
                test_login = class_soup.find('span',{'class':'msg B1'})
                print code
                break
            else:
                if int(number) > 0:
                    class_soup=BeautifulSoup(r.text)
                    class_post.clear()
                    for e in class_soup.findAll('input',{'value': True}):
                        if e.has_key('name'):
                            class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
                    class_post=drop_postdata(class_post)
                    class_post['__EVENTTARGET']='ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
                    class_post['__EVENTARGUMENT']='addCourse$0'
                    class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID']=''
                    r=s.post(url=choose,headers=header.header_info2,data=class_post)
                    class_soup=BeautifulSoup(r.text)
                    check_msg=class_soup.find('span',{'class':'msg B1'})
                    if check_msg.contents[0] != u'本科目名額目前已額滿 !':
                        print 'you get the class ,'+code+ ', check it.'
                        realcode.pop(realcode.index(code))
        if test_login != None:
          if test_login.contents[0] == '您已經在其它地方登入':
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
    reload(sys)
    sys.setdefaultencoding('utf-8')

    while True:
        try:
            login()
        except:
            print '連線逾時，嘗試重新登入'
        check_exist()
        if getclass()==True:
            break

