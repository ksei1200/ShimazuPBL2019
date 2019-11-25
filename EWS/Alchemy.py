# Alchemy Data Set設定
data = ['date_time TEXT', 'sat_ID INTEGER', 'lat REAL', 'long REAL', 'event TEXT', 'severity INTEGER',
        'loc_flag TEXT', 'dis_no INTEGER', 'semi_lat REAL', 'semi_long REAL', 'semi_mj_axis REAL',
        'semi_mn_axis REAL', 'semi_angle REAL', 'onset_date_time TEXT', 'near_city TEXT',
        'distance_fm_dis_center INTEGER', 'direction_fm_dis_center TEXT', 'epic_center_lat REAL',
        'epic_center_long REAL', 'magnitude REAL', 'dis_pict TEXT', 'dis_audio TEXT', 'tsunami_hight INTEGER',
        'tsunami_arival_date TEXT', 'typhoon_center_lat REAL', 'typhoon_center_long REAL',
        'typhoon_arival_date TEXT', 'typhoon_name TEXT', 'typhoon_category INTEGER', 'typhoon_wind_rad TEXT',
        'typhoon_direction TEXT', 'typhoon_speed INTEGER']

# Alchemy DB create スクリプト
def create():
    create_ews = 'CREATE TABLE ews (id INTEGER PRIMARY KEY AUTOINCREMENT, {0[0]}, {0[1]}, {0[2]}, {0[3]}, {0[4]}, \
    {0[5]}, {0[6]}, {0[7]}, {0[8]}, {0[9]}, {0[10]}, {0[11]}, {0[12]}, {0[13]}, {0[14]}, {0[15]}, {0[16]}, {0[17]}, \
    {0[18]}, {0[19]}, {0[20]}, {0[21]}, {0[22]}, {0[23]}, {0[24]}, {0[25]}, {0[26]}, {0[27]}, {0[28]}, {0[29]}, \
    {0[30]}, {0[31]}'.format(data) + ")"

    return create_ews


# Alchemy DB insert スクリプト
def insert(table):
    key_i = table.replace(' TEXT', '').replace(' REAL', '').replace(' INTEGER', ''). \
        replace('CREATE TABLE ews (', '').replace(' PRIMARY KEY AUTOINCREMENT', '').replace(')', '')
    key = key_i.replace(' ', '').replace('id,', '')
    key_list = key.split(',')

    # 各Valueセット用SQLスクリプト生成
    sqlstr = "INSERT INTO ews ("
    for para in key_list:
        sqlstr = sqlstr + para + ","
    sqlstr1 = sqlstr.rstrip(",")
    sqlstr2 = sqlstr1 + ')' + ' VALUES(' + "?," * (len(key_list))
    sqlstr3 = sqlstr2.strip(',')
    sqlstr4 = sqlstr3 + ')'

    # 各Valueセット用SQLスクリプト
    insert_ews = [sqlstr4, key_list]

    return insert_ews



