import requests
def pri(s):
    print s
s=requests.session()
r=s.get('http://ilearn2.fcu.edu.tw')
pri('a')
