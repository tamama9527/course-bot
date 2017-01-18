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
def login():
    global choose
    global sample
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
        try:
            class_soup=BeautifulSoup(r.text)
            for test in  class_soup.findAll('form',{'name':'aspnetForm','id':'aspnetForm'}):
                url_last=test['action']
            for e in class_soup.findAll('input',{'value':True}):
                class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
            class_post=drop_postdata(class_post)
            class_post['ctl00_ToolkitScriptManager1_HiddenField']=''
            class_post['ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState']='false'
            class_post['ctl00_MainContent_TabContainer1_ClientState']='{"ActiveTabIndex":2,"TabState":[true,true,true]}'
            sample=copy.deepcopy(class_post)
            choose=r.url.split('?guid=')[0]+url_last
        except:
            print 'server error'
        if r.text.find('驗證碼錯誤')==-1 and r.text.find('帳號或密碼錯誤')==-1 and r.text.find('重新登入')==-1:
            print 'login success'
            break;
def getclass():
    temp=header.firstchoose
    auto=header.autodrop
    count=0
    error=0
    while len(temp)!=0:
        for code in temp:
            class_post=copy.deepcopy(sample)
            class_post['ctl00$MainContent$TabContainer1$tabSelected$btnGetSub']='查詢'
            class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID']=code
            class_post['ctl00_ToolkitScriptManager1_HiddenField']=''
            r=s.post(url=choose,headers=header.header_info2,data=class_post)
            class_post.clear()
            class_soup=BeautifulSoup(r.text)
            for e in class_soup.findAll('input',{'value': True}):
                if e.has_key('name'):
                    class_post[str(e['name'].encode('utf-8'))]=str(e['value'].encode('utf-8'))
            class_post=drop_postdata(class_post)
            class_post.pop('ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState')
            class_post['__EVENTTARGET']='ctl00$MainContent$TabContainer1$tabSelected$gvToAdd'
            class_post['__EVENTARGUMENT']='selquota$0'
            class_post['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects']='1'   
            if class_soup.find('input',value='加選') == None:
                print code+' you have already get it'
                temp.pop(temp.index(code))
                break
            #class_post['ctl00$MainContent$TabContainer1$tabSelected$tbSubID']=''
            r=s.post(url=choose,headers=header.header_info3,data=class_post)
            r.encoding='utf-8'
            #print class_post
            class_post.clear()
            class_soup=BeautifulSoup(r.text)
            #print class_soup.findAll('script',text=re.compile("^setTimeout"))
            try:
                number= class_soup.findAll('script',text=re.compile("^setTimeout"))[0]
                print number
                print str(pytz.timezone('Asia/Taipei').fromutc(datetime.utcnow())).split('.')[0]+'  '+code+u'剩餘人數:'+str(number.split('：')[1].split('/')[0])    +str(temp[index])
                number=number.split('：')[1].split('/')[0]
            except:
                print code
            else:
                if int(number) > 0:
                    print "hahahahha"
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
                    c_info=r.text
                    checkerror=code
                    if checkerror==code and index:
                        error=error+1
                        if error == 10:
                            temp.pop(temp.index(code))
                            print(code+'  have something error')
                    if c_info.find('加選成功') != -1 or c_info.find('登記成功')!=-1:
                        print 'you get the class ,'+code+ ', check it.'
                        temp.pop(temp.index(code))
    return True
def drop_postdata(inputdata):
    for i in header.post_pop:
        inputdata.pop(i)
    return inputdata
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    while True:
        login()
        try:
            if getclass()==True:
                break
        except:
            print r.text
            pass
