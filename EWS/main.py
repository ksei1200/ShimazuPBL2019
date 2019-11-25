import threading
# import serial
import datetime
import os
# import math
from sqlalchemy import create_engine
import loc_decision
import dis_decision
import Alchemy
import nmea
import com_ews
from variable import *

''' Main '''
files = open('20190820_terem_afternoon.log', 'r')
lines = files.readlines()

# RAWデータファイル保存スレッド
thread1 = threading.Thread(target=com_ews.raw_file(lines))
thread1.start()

# 変数設定
t_datetime = []
t_loc = []
day = ''

# Mainプログラム
for line in lines:
    if "GPGGA" in line[1:6]:
        t_loc = nmea.gga(line)

    elif "GNZDA" in line[1:6]:
        t_datetime = nmea.zda(line)

    elif "QZQSM" in line[1:6]:
        # 現在位置測位結果
        ns = t_loc[1]
        if ns == 'S':
            lat = -1 * t_loc[0]
        else:
            lat = t_loc[0]
        ew = t_loc[3]
        if ew == 'W':
            long = -1 * t_loc[2]
        else:
            long = t_loc[2]
        location = "Latitude(deg) : {} {} / Longitude(deg) : {} {}".format(lat, ns, long, ew)

        # 現地時間算出/出力フォーマット変換
        tz = long/15
        dtime2 = t_datetime + datetime.timedelta(hours=tz)
        date_time = dtime2.strftime('%d %b %Y %H:%M')

        # EWSデータ抽出
        ews = nmea.mt44(line)
        sat_ID = nmea.sat_id(line)
        if ews != False:
            if ews != 'mt43':
                l_ews = nmea.s_ews(ews)
                mt44b = nmea.str_bin(l_ews)
                event = com_ews.disaster(mt44b)
                severity = com_ews.sev(mt44b)
                semi_lat = com_ews.lat_semi(mt44b)
                semi_long = com_ews.long_semi(mt44b)
                semi_mj_axis = com_ews.semi_major_ln(mt44b) / 1000
                semi_angle = com_ews.semi_major_angle(mt44b)
                semi_mn_axis = com_ews.semi_minor_ln(mt44b) / 1000
                onset_date_time = 'Day {0[0]} Hour {0[1]} Miniute {0[2]}'.format(com_ews.onset(mt44b))

                # 位置判定
                loc_flag = loc_decision.loc_decision(lat, long, semi_lat, semi_long, semi_mj_axis,
                                                     semi_angle, semi_mn_axis)

                # 表示方法判定
                if loc_flag == 'TRUE':
                    display = dis_decision.dis_decision(event, severity)
                    dis_no = display[0]
                    dis_pict = display[1]
                    dis_audio = display[2]

                    # 災害別ews情報抽出
                    if event == 'TSUNAMI':
                        tsu = com_ews.tsunami(mt44b)
                        t_tsunami_height = tsu[0]
                        if t_tsunami_height == 0:
                            tsunami_height = '< 1m'
                        else:
                            tsunami_height = t_tsunami_height

                        t_tsunami_arrival_date = tsu[1]
                        tsunami_arrival_day = 0
                        tsunami_arrival_time = 0
                        if t_tsunami_arrival_date == 0:
                            tsunami_arrival_day = 'NA'
                            tsunami_arrival_time = 'NA'
                        elif t_tsunami_arrival_date <= 24:
                            tsunami_arrival_day = ''
                            tsunami_arrival_time = t_tsunami_arrival_date
                        elif t_tsunami_arrival_date > 24:
                            tsunami_arrival_day = round(t_tsunami_arrival_date/24)
                            if tsunami_arrival_day < 2:
                                day = 'days'
                            else:
                                day = 'day'
                            tsunami_arrival_time = t_tsunami_arrival_date - 24 * tsunami_arrival_day
                        tsunami_arrival_date = '{} {} {} hours'.format(tsunami_arrival_day, day, tsunami_arrival_time)

                        # 近傍都市名表示
                        near_city = 'MANILA'
                        
                        # SQAlchemyからSQliteを指定
                        engine = create_engine('sqlite:///ews.db', echo=True)
                        """
                        DBにValueを挿入、DBファイルが存在しなかった場合は、ファイル・テーブル設定後にvalueを挿入、
                        DBファイルが存在する場合はvalueの追加のみを行う。
                        """
                        create_ews = Alchemy.create()
                        ten_ews = Alchemy.insert(create_ews)
                        insert_ews = ten_ews[0]

                        values = [date_time, sat_ID, lat, long, event, severity, loc_flag, dis_no, semi_lat, semi_long,
                                  semi_mj_axis,
                                  semi_mn_axis, semi_angle, onset_date_time, near_city, distance_fm_dis_center,
                                  direction_fm_dis_center,
                                  epic_center_lat, epic_center_long, magnitude, dis_pict, dis_audio, tsunami_height,
                                  tsunami_arrival_date,
                                  typhoon_center_lat, typhoon_center_long, typhoon_arrival_date, typhoon_name,
                                  typhoon_category,
                                  typhoon_wind_rad, typhoon_direction, typhoon_speed]
                        
                        if os.path.exists('ews.db') == False:
                            with engine.connect() as con:
                                con.execute(create_ews)
                                con.execute(insert_ews, values)
                                con.close()
                        else:
                            with engine.connect() as con:
                                con.execute(insert_ews, values)
                                con.close()

with engine.connect() as con:
    rows = con.execute("select * from ews;")
    for row in rows:
        print(row)

    con.close()
