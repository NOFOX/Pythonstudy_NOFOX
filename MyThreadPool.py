# coding=gbk
'''
Created on 2015-9-25

@author: kiven
'''

# encoding: UTF-8
import Queue
import sys
import threading
import time
import urllib



class MyThread(threading.Thread):
 def __init__(self, workQueue, resultQueue, timeout=5, **kwargs):
  threading.Thread.__init__(self, kwargs=kwargs)
  # �߳��ڽ���ǰ�ȴ�������ж೤ʱ��
  self.timeout = timeout
  self.setDaemon(True)
  self.workQueue = workQueue
  self.resultQueue = resultQueue
  self.start()

 def run(self):
  while True:
   try:
    # �ӹ��������л�ȡһ������
    callable, args, kwargs = self.workQueue.get(timeout=self.timeout)
    # ����Ҫִ�е�����
    res = callable(args, kwargs)
    # �����񷵻صĽ�����ڽ��������
    self.resultQueue.put(res + " | " + self.getName())    
   except Queue.Empty:  # ������пյ�ʱ��������߳�
    break
   except :
    #print sys.exc_info()
    raise
    
class ThreadPool:
 def __init__(self, num_of_threads=10):
  self.workQueue = Queue.Queue()
  self.resultQueue = Queue.Queue()
  self.threads = []
  self.__createThreadPool(num_of_threads)

 def __createThreadPool(self, num_of_threads):
  for i in range(num_of_threads):
   thread = MyThread(self.workQueue, self.resultQueue)
   self.threads.append(thread)

 def wait_for_complete(self):
  # �ȴ������߳���ɡ�
  while len(self.threads):
   thread = self.threads.pop()
   # �ȴ��߳̽���
   if thread.isAlive():  # �ж��߳��Ƿ񻹴���������Ƿ����join
    thread.join()
    
 def add_job(self, callable, *args, **kwargs):
  self.workQueue.put((callable, args, kwargs))

def test_job(id, sleep=0.001):
 html = ""
 try:
  time.sleep(1)
  conn = urllib.urlopen('http://www.google.com/')
  html = conn.read(20)
 except:
  html = sys.exc_info()
 return  html

def test():
 print 'start testing'
 tp = ThreadPool(10)
 for i in range(50):
  time.sleep(0.2)
  tp.add_job(test_job, i, i * 0.001)
 tp.wait_for_complete()
 # ������
 print 'result Queue\'s length == %d ' % tp.resultQueue.qsize()
 while tp.resultQueue.qsize():
  print tp.resultQueue.get()
 print 'end testing'
if __name__ == '__main__':
 test()
