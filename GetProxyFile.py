'''
Created on 2015-9-25

@author: kiven
'''
# encoding: UTF-8
import threading
import time
import urllib2

from bs4 import BeautifulSoup

import MyThreadPool


def GetProxyAgent(urlstr, nouse):
    request = urllib2.Request(urlstr[0], None, headers)
    try:
        html_doc = urllib2.urlopen(request, None, 15).read()
    except:
        print 'open  error'
        return "error"
    # html_doc = urllib2.urlopen('http://www.xicidaili.com/nn/' + str(page) ).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        ip = tds[2].text.strip()
        port = tds[3].text.strip()
        protocol = tds[6].text.strip()
        if protocol == 'HTTP' or protocol == 'HTTPS':
            lock.acquire()
            of.write('%s=%s:%s\n' % (protocol, ip, port))
            lock.release()
            print '%s=%s:%s' % (protocol, ip, port)
    return urlstr[0]

if __name__ == '__main__':
    
    of = open('proxy.txt' , 'w')
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                            }
      
    lock = threading.Lock()
    tp = MyThreadPool.ThreadPool(20)
     
    for page in range(1, 200):
        time.sleep(0.1)
        tp.add_job(GetProxyAgent, 'http://www.xicidaili.com/nn/' + str(page) , page)
    tp.wait_for_complete()
    of.close()
