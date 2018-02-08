#coding=utf-8
from obspy import *
from obspy.taup.tau import TauPyModel
from obspy.core import Stream
import time
#a=read("/home/v/YN.201506152046.0002.seed")
#n=a[2].copy()
inv=read_inventory("/home/v/YN.201506152046.0002.seed")
#tr=a[0]
#.remove_response(inventory=inv)
print inv[0][0][0]
inv.write("/home/v/my_inventory.xml", format='STATIONXML')
T=TauPyModel()
print T
#a=T.get_travel_times(10, distance_in_degree=1,receiver_depth_in_km=0)
header=read("/home/v/YN.201506152046.0002.seed",headonly=True)
print header.__str__(extended=True)

