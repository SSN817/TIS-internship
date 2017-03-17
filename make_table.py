from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time as tm
import json
from pprint import pprint
from slackclient import SlackClient
import textwrap


font = ImageFont.truetype('osaka.unicode.ttf',20, encoding='unic')
mini_font = ImageFont.truetype('osaka.unicode.ttf',12, encoding='unic')

slack_token = "XXX"
sc = SlackClient(slack_token)

user_data = sc.api_call(
"users.list",
)

ymargin = 50 
sec_per_pix = 40
name_heigth = 50

def id_to_name(ID):

    if(not user_data['ok']):
        return 'error1'
    else:
        for l in user_data['members']:
            print(l['id']+':::'+ID)
            if(l['id'] == ID):
                return l['name']
    return 'error2'



class DrawLog:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 200
        self.name_heigth = name_heigth
        self.sec_per_pix = sec_per_pix

        self.name = ""
        self.logs = []
        self.now_time = 0

    def set_info(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def set_now_time(self,time):
        self.now_time = time

    def set_log(self,start_time,time,comment,opinion):
        log = [start_time,time,comment,opinion]
        self.logs.append(log)

    def draw_time(self,start_time,time):
        draw.text((self.x,self.y + self.name_heigth+ start_time/self.sec_per_pix),str(int(time/60.0)), font=font, fill='#000')

    def draw_comment(self,start_time,comment, opinion):
        buf = textwrap.wrap(comment,12)
        obuf = textwrap.wrap(opinion,24)

        for i in range(len(buf)):
            draw.text((self.x,self.y + self.name_heigth+  start_time/self.sec_per_pix + 20*(i+1)),buf[i], font=font, fill='#000')
        for i in range(len(obuf)):
            draw.text((self.x,self.y + self.name_heigth+  start_time/self.sec_per_pix + (len(buf)+1)*20 + 10*(i+1)),obuf[i], font=mini_font, fill='#000')

    def draw_log_rect(self,start_time,time,color):
        end_time = int(start_time) + int(time)
        start_y = start_time / self.sec_per_pix
        end_y = end_time / self.sec_per_pix
        draw.rectangle(((self.x,self.y + self.name_heigth + start_y),(self.x + self.width,self.y + self.name_heigth + end_y)),outline = (0,0,0),fill = color)

    def draw_log_red(self,start_time,time):
        end_time = time
        start_y = start_time / self.sec_per_pix
        end_y = end_time / self.sec_per_pix
        draw.rectangle(((self.x,self.y + self.name_heigth + start_y),(self.x + self.width,self.y + self.name_heigth + end_y)),outline = (0,0,0),fill = 'red')

    

    def draw_log(self):
        draw.rectangle(((self.x,self.y),(self.x + self.width,self.y + self.name_heigth)),outline = (0,0,0),fill = 'white')
        draw.text((self.x,self.y),id_to_name(self.name), font=font, fill='#000')
        self.draw_log_red(self.logs[0][0],self.now_time)
        for log in self.logs:
            self.draw_log_rect(log[0],log[1],'white')
            self.draw_comment(log[0],log[2],log[3])
            self.draw_time(log[0],log[1])
        end_y =  self.now_time / self.sec_per_pix
        draw.line((0,self.y + self.name_heigth + end_y, 2400, self.y + self.name_heigth + end_y), fill=128)



while True: 


    f = open('log.txt','r')
    logs = []
    for row in f:
        row = row.strip()
        row = row.split('|')
        print(len(row))
        if(len(row)==12):
            logs.append(row)
    f.close()

    name_to_log = {}
    for log in logs:
        name_to_log[log[0]] =[]
    for log in logs:
        name_to_log[log[0]].append(log[1:len(log)-1])
    name_list = list(name_to_log.keys())
    name_list.sort()

    now_time = datetime.now()
    #now_time = datetime(2017,3,15,16,0,0)
    start_time = datetime(2017,3,17,9,0,0)

    delta = now_time - start_time

    text_canvas = Image.new('RGB',(len(name_list)*220+200,int(delta.total_seconds()/sec_per_pix)+300), (255, 255, 255))
    draw = ImageDraw.Draw(text_canvas)


    for i in range(24):
        draw.text((20,ymargin +name_heigth+ i*3600/sec_per_pix-12),str(start_time.hour+i)+':00' , font=font, fill='#000')
        draw.text((20,ymargin +name_heigth+ (i*3600+1800)/sec_per_pix-12),str(start_time.hour+i)+':30', font=font, fill='#000')

    for i in range(len(name_list)):
        column = DrawLog()
        column.set_now_time(delta.total_seconds())
        column.set_info(120+220*i,ymargin,name_list[i])
        for j in range(len(name_to_log[name_list[i]])):
            alog = name_to_log[name_list[i]][j]
            task_start_time = datetime(int(alog[4]),int(alog[5]),int(alog[6]),int(alog[7]),int(alog[8]),int(alog[9]))
            abs_task_start_time = task_start_time - start_time
            time = 60*int(alog[1])
            column.set_log(abs_task_start_time.total_seconds(),time,alog[2],alog[3])
            column.draw_log()

    text_canvas.save('text_img.jpg', 'JPEG', quality=100, optimize=True)


    sc.api_call(
        "chat.postMessage",
        channel="#intern",
        text = 'showResult'
        )
    tm.sleep(1800)







