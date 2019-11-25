def dis_decision(event, severity):
    if event == 'TSUNAMI' and severity <= 2:
        dis_no = 1
        dis_pict = 'tsumnami.png'
        dis_audio = 'tsunami-1.mp3'
    elif event == 'TSUNAMI' and severity >= 3:
        dis_no = 2
        dis_pict = 'tsumnami.png'
        dis_audio = 'tsunami-2.mp3'
    elif event == 'EARTHQUAKE' and severity <= 2:
        dis_no = 3
        dis_pict = 'earthquake.png'
        dis_audio = ''
    elif event == 'EARTHQUAKE' and severity == 3:
        dis_no = 4
        dis_pict = 'earthquake.png'
        dis_audio = 'erathquake-4.mp3'
    elif event == 'EARTHQUAKE' and severity == 4:
        dis_no = 5
        dis_pict = 'earthquake.png'
        dis_audio = 'erathquake-5.mp3'
    elif event == 'TYPHOON' and severity <= 2:
        dis_no = 6
        dis_pict = 'typhoon.png'
        dis_audio = ''
    elif event == 'TYPHOON' and 2 < severity <= 3:
        dis_no = 7
        dis_pict = 'typhoon.png'
        dis_audio = 'typhoon-7.mp3'
    elif event == 'TYPHOON' and severity >= 4:
        dis_no = 8
        dis_pict = 'typhoon.png'
        dis_audio = 'typhoon-8.mp3'
    elif event == 'FLOOD' and severity < 2:
        dis_no = 9
        dis_pict = 'flood.png'
        dis_audio = ''
    elif event == 'FLOOD' and 2 <= severity <= 3:
        dis_no = 10
        dis_pict = 'flood.png'
        dis_audio = 'flood-10.mp3'
    elif event == 'FLOOD' and severity >= 4:
        dis_no = 11
        dis_pict = 'flood.png'
        dis_audio = 'flood-11.mp3'
    else:
        dis_no = 'NA'
        dis_pict = 'NA'
        dis_audio = 'NA'

    dis_info = [dis_no, dis_pict, dis_audio]

    return dis_info