import math


def loc_decision(lat, long, semi_lat, semi_long, semi_major, major_angle, semi_minor):
    pi = math.pi
    sin = math.sin
    cos = math.cos
    sqrt = math.sqrt

    # azimuth angleのradian変換
    sma = math.radians(major_angle)

    # 楕円パラメーター計算
    p = semi_major ** 2 * cos(sma) ** 2 + semi_minor ** 2 * sin(sma) ** 2
    q = semi_major ** 2 - semi_minor ** 2
    r = semi_major ** 2 * sin(sma) ** 2 + semi_minor ** 2 * cos(sma) ** 2

    # 回転楕円のx範囲の算出
    xmax = sqrt(-semi_major ** 2 * semi_minor ** 2 * p / (sin(sma) ** 2 * cos(sma) ** 2 * q ** 2 - p * r))
    xmin = -sqrt(-semi_major ** 2 * semi_minor ** 2 * p / (sin(sma) ** 2 * cos(sma) ** 2 * q ** 2 - p * r))

    # 楕円範囲の経度範囲算出
    earth_radius = 6378.137
    earth_circum = 2 * pi * earth_radius
    dis_one_deg = earth_circum / 360
    long_delta = xmax / dis_one_deg
    long_min = semi_long - long_delta
    long_max = semi_long + long_delta

    if long_min <= long <= long_max:
        # 楕円中心と現在位置の経度差をx（距離）に変換
        def_long_deg = long - semi_long
        def_long = dis_one_deg * def_long_deg

        # 現在位置での楕円緯度範囲の算出
        semi_lat_min = (-sin(sma) * cos(sma) * def_long * q - sqrt(sin(sma) ** 2 * cos(sma) ** 2 * def_long ** 2 * q ** 2 \
                                                - def_long ** 2 * p * r + semi_major ** 2 * semi_minor ** 2 * p)) / p

        semi_lat_max = (-sin(sma) * cos(sma) * def_long * q + sqrt(sin(sma) ** 2 * cos(sma) ** 2 * def_long ** 2 * q ** 2 \
                                                - def_long ** 2 * p * r + semi_major ** 2 * semi_minor ** 2 * p)) / p
        # 緯度範囲計算
        lat_min = semi_lat + semi_lat_min / dis_one_deg
        lat_max = semi_lat + semi_lat_max / dis_one_deg

        if lat_min <= lat <= lat_max:
            loc_flag = 'TRUE'
            # print('Here is within area !!')
        else:
            loc_flag = 'FALSE'
            # print('Here is not within area !!')
    else:
        loc_flag = 'FALSE'
        # print('Here is not within area !!')

    return loc_flag
