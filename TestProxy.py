'''
Created on 2015-9-25

@author: kiven
'''
# encoding=gbk

import re
import threading
import time
import urllib2

import MyThreadPool


def getip():
        try:
            myip = visit("http://www.ip138.com/ip2city.asp")
        except:
            try:
                myip = visit("http://www.bliao.com/ip.phtml")
            except:
                try:
                    myip = visit("http://www.whereismyip.com/")
                except:
                    myip = "So sorry!!!"
        return myip

def visit(url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+', str).group(0)
        
def test(linestr, nouse):
    proxy_ip = ""
    protocol, proxystr = linestr[1].split('=')
    headers = {
               # 'Host': 'epassport.meituan.com',
               'Connection': 'keep-alive',
               # 'Content-Length': '29',
                'Cache-Control': 'max-age=0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Upgrade-Insecure-Requests': '1',
               
               # 'Origin': 'https://epassport.meituan.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36',
               # 'Referer': 'https://epassport.meituan.com/account/login?pagetype=mini&service=ecom&continue=http%3A%2F%2Fe.meituan.com%2Fm%2Faccount%2Fsettoken&style=ecommobile&loginsource=2',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Cookie': ''                   
                    }
    try:

        proxy = urllib2.ProxyHandler({protocol.lower(): proxystr})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        request = urllib2.Request('http://city.ip138.com/ip2city.asp')
        request.add_header('Cache-Control', 'no-cache')  
        response = urllib2.urlopen(request, timeout=5)
        html_doc = response.read()
        # print html_doc.encode('gbk')
        if html_doc.find('center') > 0:
            lock.acquire()
            print 'add proxy', proxystr
            outFile.write(proxystr + '\n')
            lock.release()
        else:
            print '.',
    except Exception, e:
        print e
    return proxystr     
            
if __name__ == '__main__':
    inFile = open('proxy.txt', 'r')
    outFile = open('available.txt', 'w')
    lock = threading.Lock()
    tp = MyThreadPool.ThreadPool(20)
    for line in inFile.readlines() :
        tp.add_job(test, 1, line.strip())
    tp.wait_for_complete()
    inFile.close()
    outFile.close()
