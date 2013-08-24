#!/usr/bin/env python

import sys
import time
import pprint
import math
from Tkinter import Tk

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

pp = pprint.PrettyPrinter()

from xml.dom.minidom import parse, parseString

dom = parse(sys.argv[1])

track_points = dom.getElementsByTagName("trkpt")

times = []

for i in range(1, len(track_points)):
    lat1 = track_points[i-1].getAttribute("lat")
    long1 = track_points[i-1].getAttribute("lon")
    lat2 = track_points[i].getAttribute("lat")
    long2 = track_points[i].getAttribute("lon")

    d = distance((float(lat1), float(long1)), (float(lat2), float(long2)))

    # pp.pprint(d)
    time1 = track_points[i-1].getElementsByTagName("time")[0]
    time2 = track_points[i].getElementsByTagName("time")[0]

    #pp.pprint(getText(time1.childNodes))
    t1 = time.mktime(time.strptime(getText(time1.childNodes), "%Y-%m-%dT%H:%M:%SZ"))
    t2 = time.mktime(time.strptime(getText(time2.childNodes), "%Y-%m-%dT%H:%M:%SZ"))

    dt = t2 - t1

    if (dt > 0):
        s = (d / dt) * 3600

        #print s
        times.append(s)

times.sort()
median = round(times[len(times) / 2], 2)

r = Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(median)
r.destroy()
