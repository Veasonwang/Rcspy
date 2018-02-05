#coding=utf-8
from obspy import *
from obspy.core import Stream
import time
a=read("/home/v/YN.201506152046.0002.seed")
n=a[2].copy()
inv=read_inventory("/home/v/YN.201506152046.0002.seed")
tr=a[0]
#.remove_response(inventory=inv)
time_start=time.time()
tr.attach_response(inv)
tr.remove_response()
time_end1=time.time()
n.remove_response(inv)
time_end2=time.time()
print time_start
print time_end1
print time_end2


