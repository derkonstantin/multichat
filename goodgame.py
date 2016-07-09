#!/usr/bin/env python

import asyncio
import websockets
import json
import sys
import datetime
import multiprocessing

def get_channel_id_by_streamer_name(name):
    import requests
    XML_answer = requests.get('http://goodgame.ru/api/getchannelstatus?id=' + str(name))
    if XML_answer.status_code == 200:
        import untangle
        obj = untangle.parse(XML_answer.text)
        return obj.root.stream.stream_id.cdata
    return None


class GoodGame_websock(multiprocessing.Process):

    def __init__(self, config, child_pipe):
        super(GoodGame_websock, self).__init__()
    #   self.nick = config['goodgame']['nick']
        self.channel = config['goodgame']['channel']
    #   self.password = config['goodgame']['password']
        self.pipe = child_pipe
        self.host = config['goodgame']['host'].strip()
    #   self.port = int(config['goodgame']['post'])

    async def goodgame_chat(self):
        async with websockets.connect(self.host) as websocket:

            greeting = await websocket.recv()
            greeting = json.loads(greeting)
            #print(greeting)
            if greeting['type'] != 'welcome':
                sys.exit(1)

            await websocket.send(self.auth_msg(0))
            #answer = await websocket.recv()
            #answer = json.loads(answer)

            channel_id = get_channel_id_by_streamer_name(self.channel)

            await websocket.send(self.join_channel_msg(channel_id))
            answer = await websocket.recv()
            #answer = json.loads(answer)

            while (1):
                answer = await websocket.recv()
                answer = json.loads(answer)
                if answer['type'] == 'message':
                    self.parse_chat_msg(answer['data'])
                    # print(answer)  - debug output


    def auth_msg(self,user):
        msg = {}
        msg['type'] = 'auth'
        msg['data'] = {}
        msg['data']['site_id'] = 1
        msg['data']['user_id'] = user
        msg['data']['token'] = ''
        return json.dumps(msg)


    def join_channel_msg(self, channel_id):
        msg = {}
        msg['type'] = 'join'
        msg['data'] = {}
        msg['data']['channel_id'] = channel_id
        msg['data']['hidden'] = False
        msg['data']['mobile'] = False
        return json.dumps(msg)


    def get_channel_list_msg(self):
        msg = {}
        msg['type'] = 'get_channels_list'
        msg['data'] = {}
        msg['data']['start'] = 0
        msg['data']['count'] = 50
        return json.dumps(msg)


    def find_channel_id_by_name(self, name, channels):
        for channel in channels:
            if channel['channel_name'] == name:
                return channel['channel_id']
        return None



    def parse_chat_msg(self, msg):
        time = datetime.datetime.fromtimestamp(msg['timestamp']).strftime('%H:%M:%S')
        self.pipe.send(':GG: ' + msg['user_name'] + ' :' + msg['text'])
        #print(':GG:' + time + ':' + msg['user_name'] + ' : ' + msg['text'])

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.goodgame_chat())
        loop.run_forever()

if __name__ == '__main__':
    pass