'''
Created on 2015-9-27

@author: kiven
'''
import os
import sys
import time
from urllib2 import urlopen
import urlparse


def getpicname(path):
    '''    retrive filename of url        '''
    if os.path.splitext(path)[1] == '':
        return None
    pr=urlparse(path)
    path='http://'+pr[1]+pr[2]
    return os.path.split(path)[1]


def saveimgto(path, url):
    '''
    save img of url to local path
    '''
    if not os.path.isdir(path):
        print('path is invalid')
        sys.exit()
    else:
        of=open('G:\\Bak\\' +str(time.time()) + '.jpg', 'w+b')
        q=urlopen(url)
        of.write(q.read())
        q.close()
        of.close()
            
if __name__ == '__main__':
    for i in range(1, 200):
        url = 'https://mail.sina.com.cn/cgi-bin/imgcode.php?t=' + str(int(time.time()))
        saveimgto('G:\\Bak\\', url)
    pass