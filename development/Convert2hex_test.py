import sys

def mt44(nmea):
    if "QZQSM" in nmea and nmea[12:13] == 'B':
        mt44 = nmea[10:].rstrip('\n')
        print('mt44_raw : ' +mt44)
        return mt44[0:61]

    elif "QZQSM" in nmea and nmea[12:13] == 'A':
        return 'mt43'
    else:
        return False

def sat_id(nmea):
    if "QZQSM" in nmea:
        id = int(nmea[7:9])
        sat_id = id + 128
        return sat_id
    else:
        return False

def s_ews(mt44):
    split_ews =list(mt44)
    return split_ews

def str_bin(mt44_s):
    mt44_hex = [int(i, 16) for i in mt44_s]
    mt44_bin_l = [format(j, '04b') for j in mt44_hex]
    print('mt44_bin_l= ' )
    print(mt44_bin_l)
    mt44_bin = ''.join(mt44_bin_l)

    mt44_bin = mt44_bin[35:214]
    print('mt44_bin: ' + mt44_bin)
    return mt44_bin

def event(ews):
    event_ews = ews[18:24]
    print(event_ews)
    if event_ews == '000000':
        disaster = 'EARTHQUAKE'
    elif event_ews == '000001':
        disaster = 'TSUNAMI'
    elif event_ews == '010000':
        disaster = 'TYPHOON'
    elif event_ews == '011001':
        disaster = 'FLOOD'
    elif event_ews == '001010':
        disaster = 'VOLCANO'
    elif event_ews == '101001':
        disaster = 'Ballistic Missile Attack'
    else :
        disaster = 'NA'
    return disaster

def severity(ews):
    sev_ews = ews[24:26]
    severity = int(sev_ews, 2)
    return severity

def semi_lat(ews):
    lat_b = ews[54:69]
    lat_d = int(lat_b, 2)
    lat = -90 + ((180 / ((2 ** 15) - 1)) * lat_d)
    return lat

def semi_long(ews):
    long_b = ews[69:85]
    long_d = int(long_b, 2)
    long = -180.0 + ((360/((2 ** 16)-1)) * long_d)
    return long

def semi_major_ln(ews):
    semi_major_ln_b = ews[85:89]
    semi_major_ln_d = int(semi_major_ln_b, 2)
    semi_major_ln = 10**(2+semi_major_ln_d/3)
    return semi_major_ln

def semi_major_angle(ews):
    semi_major_angle_b = ews[93:100]
    print('smja= ' + semi_major_angle_b)
    semi_major_angle_d = int(semi_major_angle_b, 2)
    print('smja_int= ' + str(semi_major_angle_d))
    semi_major_angle = semi_major_angle_d * (180/(2**7 - 1))
    return semi_major_angle

def semi_minor_ln(ews):
    semi_minor_ln_b = ews[89:93]
    semi_minor_ln_d = int(semi_minor_ln_b, 2)
    semi_minor_ln = 10**(2+semi_minor_ln_d/3)
    return  semi_minor_ln

def onset(ews):
    day_bin = ews[26:31]
    hour_bin = ews[31:36]
    min_bin = ews[36:42]
    day = int(day_bin, 2)
    hour = int(hour_bin, 2)
    min = int(min_bin, 2)
    return day ,hour ,min



####### Main #######
files = open('20190820_terem_afternoon.log', 'r')
lines = files.readlines()

for line in lines:
    #print(line)
    ews = mt44(line)
    satid = sat_id(line)

    if ews != False:
        if ews != 'mt43':
            print(line)
            l_ews = s_ews(ews)
            mt44b = str_bin(l_ews)
            dis = event(mt44b)
            lat_semi = semi_lat(mt44b)
            long_semi = semi_long(mt44b)
            major_semi_ln = semi_major_ln(mt44b)
            major_semi_axis = semi_major_angle(mt44b)
            minor_semi_ln = semi_minor_ln(mt44b)
            ddhhmm = onset(mt44b)

            print("********************************************")
            print(satid)
            print(l_ews)
            print(mt44b)
            print(dis)
            print(severity(mt44b))
            print(lat_semi)
            print(long_semi)
            print(major_semi_ln)
            print(major_semi_axis)
            print(minor_semi_ln)
            print(ddhhmm)
        else:
            continue
    else:
        continue



files.close()

