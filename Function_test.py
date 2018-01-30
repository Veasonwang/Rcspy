#coding=utf-8
from multiprocessing import Pool
from threading import Thread

from multiprocessing import Process
def loop(num):
    while True:
        num=num+1
        print num
        pass
class a:
    def __init__(self):
        num=0
        for i in range(3):
            t = Process(target=loop(num))
            t.start()

        while True:
            pass

if __name__ == '__main__':
    a=['0','1','2']
    print a[0:1]

