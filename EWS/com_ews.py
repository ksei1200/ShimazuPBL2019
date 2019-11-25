import datetime

# EWSデータ内のevent(災害）種別抽出と変換
def disaster(ews):
    event_ews = ews[18:24]
    # print(event_ews)
    if event_ews == '000000':
        dis = 'EARTHQUAKE'
    elif event_ews == '000001':
        dis = 'TSUNAMI'
    elif event_ews == '010000':
        dis = 'TYPHOON'
    elif event_ews == '011001':
        dis = 'FLOOD'
    elif event_ews == '001010':
        dis = 'VOLCANO'
    elif event_ews == '101001':
        dis = 'Ballistic Missile Attack'
    elif event_ews == '001111':
        dis = 'Error'
    else:
        dis = 'NA'
    return dis


# EWSデータ内のsevirity(重要度）抽出と変換
def sev(ews):
    sev_ews = ews[24:26]
    sev_raw = int(sev_ews, 2)
    severity = 4 - sev_raw
    return severity

# EWSデータ内の楕円中心緯度抽出と変換
def lat_semi(ews):
    lat_s_b = ews[54:69]
    lat_s_d = int(lat_s_b, 2)
    lat_s = -90 + ((180 / ((2 ** 15) - 1)) * lat_s_d)
    return lat_s


# EWSデータ内の楕円中心経度抽出と変換
def long_semi(ews):
    long_s_b = ews[69:85]
    long_s_d = int(long_s_b, 2)
    long_s = -180.0 + ((360/((2 ** 16)-1)) * long_s_d)
    return long_s


# EWSデータ内の楕円長半径抽出と変換
def semi_major_ln(ews):
    semi_major_ln_b = ews[85:89]
    semi_major_ln_d = int(semi_major_ln_b, 2)
    semi_major_ln = 10**(2+semi_major_ln_d/3)
    return semi_major_ln


# EWSデータ内の楕円長半径角度抽出と変換
def semi_major_angle(ews):
    semi_major_angle_b = ews[93:100]
    # print('smja= ' + semi_major_angle_b)
    semi_major_angle_d = int(semi_major_angle_b, 2)
    # print('smja_int= ' + str(semi_major_angle_d))
    # EWS Message azimuth angle計算式より
    semi_major_angle = semi_major_angle_d * (180/(2**7 - 1))
    return semi_major_angle


# EWSデータ内の楕円短半径抽出と変換
def semi_minor_ln(ews):
    semi_minor_ln_b = ews[89:93]
    semi_minor_ln_d = int(semi_minor_ln_b, 2)
    semi_minor_ln = 10**(2+semi_minor_ln_d/3)
    return  semi_minor_ln


# EWSデータ内の発災時間抽出と変換
def onset(ews):
    day_bin = ews[26:31]
    hour_bin = ews[31:36]
    min_bin = ews[36:42]
    day = int(day_bin, 2)
    hour = int(hour_bin, 2)
    min = int(min_bin, 2)
    onset_dt = [day, hour, min]
    return onset_dt


def raw_file(lines):
    dt = datetime.datetime.now()
    dtstr = str(dt)[0:19].replace(' ', '_')
    fn = "nmea_{}.txt".format(dtstr)
    f = open(fn, 'a')
    for line in lines:
        f.write(line)
    f.close()

def tsunami(ews):
    #if ews[100:103] == '101':
    tsunami_ht_b = ews[103:106]
    tsunami_ht = int(tsunami_ht_b, 2)
    tsunami_arv_date_b = ews[106:118]
    tsunami_arv_date = int(tsunami_arv_date_b, 2)
    tsunami_info = [tsunami_ht, tsunami_arv_date]
    return tsunami_info
