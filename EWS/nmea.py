import datetime
import math

# GNZDAから現在時刻抽出
def zda(line):
    t_time = line
    yr = t_time[-10:-6]
    mo = t_time[-13:-11]
    dy = t_time[-16:-14]
    l_hour= t_time[7:9]
    mn = t_time[9:11]
    sc = t_time[11:13]
    time_str= [yr, mo, dy, l_hour, mn, sc]
    dt = "{0[0]}/{0[1]}/{0[2]} {0[3]}:{0[4]}:{0[5]}".format(time_str)
    dtime = datetime.datetime.strptime(dt,'%Y/%m/%d %H:%M:%S')
    return dtime


# GPGGAから現在位置の測位情報抽出
def gga(line):
    t_loc = line
    lat_str = t_loc[17:26]
    lat_d = math.modf(float(lat_str)/100)
    lat = lat_d[1] + (lat_d[0]*6000/3600)
    ns = t_loc[27:28]
    long_str = t_loc[29:39]
    long_d = math.modf(float(long_str)/100)
    long = long_d[1] + (long_d[0]*6000/3600)
    ew = t_loc[40:41]
    location = [lat, ns, long, ew]
    return location


# QZQSMから衛星ID抽出
def sat_id(nmea):
    if "QZQSM" in nmea[1:6]:
        id = int(nmea[7:9])
        st_id = str(id + 128)
        return st_id
    else:
        st_id = "Not Available"
        return st_id


# QZQSMからMT44抽出
def mt44(nmea):
    if "QZQSM" in nmea and nmea[12:13] == 'B':
        mt44 = nmea[10:].rstrip('\n')
        # print('mt44_raw : ' +mt44)
        return mt44[0:61]
    elif "QZQSM" in nmea and nmea[12:13] == 'A':
        return 'mt43'
    else:
        return False


# MT44のHEXを１文字ずつリストに格納
def s_ews(mt44):
    split_ews =list(mt44)
    return split_ews


# MT44のHEXをDEC-Binaryに変換し、連結、EWSとして必要部分のみ抽出
def str_bin(mt44_s):
    mt44_hex = [int(i, 16) for i in mt44_s]
    mt44_bin_l = [format(j, '04b') for j in mt44_hex]
    # print('mt44_bin_l= ' )
    # print(mt44_bin_l)
    mt44_bin = ''.join(mt44_bin_l)
    mt44_bin = mt44_bin[35:214]
    # print('mt44_bin: ' + mt44_bin)
    return mt44_bin