#coding=utf-8
from obspy import *
from obspy.core import Stream
a=read("/home/veason/Desktop/data_for_debug/YN.201506152046.0002.seed")
n=a[0].copy()
inv=read_inventory("/home/veason/Desktop/data_for_debug/YN.201506152046.0002.seed")
inv.plot(projection="ortho", label=False,
         color_per_network=True)
#.remove_response(inventory=inv)
n.plot()


