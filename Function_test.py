#coding=utf-8
from obspy import *
from obspy.core import Stream
a=read("/home/veason/Desktop/data_for_debug/YN.201506152046.0002.seed")
n=a[2].copy()
inv=read_inventory("/home/veason/Desktop/data_for_debug/YN.201506152046.0002.seed")

#.remove_response(inventory=inv)
c=n.detrend(type='constant')
st=Stream()
print c.std()
print a[2].std()
st.append(a[2])
st.append(c)
st.plot()


