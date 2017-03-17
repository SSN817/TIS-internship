# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import json
import re
import csv
from datetime import datetime
import os.path

from pprint import pprint
from slackclient import SlackClient

slack_token = "XXX"
sc = SlackClient(slack_token)

user_data = sc.api_call(
"users.list",
)


def id_to_name(ID):
    print(type(user_data))
    if(not user_data['ok']):
        return 'error'
    else:
        for l in user_data['members']:
            if(l['id'] == ID):
                return l['name']
    return 'error'


@listen_to('(.*)')
@respond_to('(.*)')
def hello(message, something):
    if(something != 'showResult'):
        #print(message.body['user'])
        #print(type(message.body))

        name = message.body['user']
        mnc=something.split(':')

        m = mnc[0]
        if(m.isdigit()):
            if(len(mnc)>1):
                n = mnc[1]
            else:
                n =""

            if(len(mnc)>2):
                c = mnc[2]
            else:
                c = ""

            now = datetime.now()
            row = []
            row.append(name)
            row.append(something)
            row.append(m)
            row.append(n)
            row.append(c)
            row.append(now.year)
            row.append(now.month)
            row.append(now.day)
            row.append(now.hour)
            row.append(now.minute)
            row.append(now.second)

            if(os.path.exists('log.txt')):
                f = open('log.txt','a')
                f.write('\n')
            else:
                f = open('log.txt','a')
            
            for i in range(len(row)):
                f.write(str(row[i]))
                f.write('|')
            f.close()

            message.reply(id_to_name(name)+'さんがいまから'+m+'分'+n+'をするそうです')


@listen_to('showResult')
@respond_to('showResult')
def load(message):
    message.channel.upload_file('結果報告','text_img.jpg','引き続きお仕事頑張って下さい' )
