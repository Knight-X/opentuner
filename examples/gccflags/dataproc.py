import sqlite3
import os
import dateparser
from datetime import datetime

def connect(name):
    create = not os.path.exists(name)
    conn = sqlite3.connect(name)
    return conn

def query(conn, sid, eid):
    cursor = conn.cursor()
    cursor.execute("SELECT time , collection_date from result where id >= ? and id <= ?", (sid, eid))
    blocks = []
    for fields in cursor:
        if fields[0] != 'Inf':
            blocks.append([str(fields[0]), str(fields[1])])
    return blocks 

def dataprocess(datas):
    temp = cleandata(datas)
    temp = group(temp)
    temp = avg(temp)
    return temp
def output(filename, items):
    text_file = open(filename, "w")
    x = 0
    for i in items:
        text_file.write("%s %s\n" % (x, i))
        x = x + 60
    text_file.close()

def group(items):
    result = []
    oldmin = 'str'
    temp = []
    for t in items:
        newmin = t[0]
        if oldmin == 'str':
            oldmin = newmin
        if oldmin == newmin:
            temp.append(t[1])
        else:
            result.append(temp)
            temp = []
            temp.append(t[1])
            oldmin = newmin
    result.append(temp)
    return result

def min_item(items):
    result = []
    temp = []
    t_min = 400 
    for item in items:
        sinmin = min(item)
        temp.append(sinmin)

    for r in temp:
        if (r < t_min):
            t_min = r
            result.append(r)
        else:
            result.append(t_min)
    return result
def avg(items):
    result = []
    for item in items:
        print(item)
        sinavg = float(sum(item) / float(len(item)))
        result.append(sinavg)
    return result
def cleandata(datas):
    nitems = []
    for i in datas:
        if i[0] != 'inf':
            dat = datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S.%f')
            minute = dat.minute
            nitems.append([minute, float(i[0])])
    
    return nitems
