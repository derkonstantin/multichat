#!/usr/bin/env python3

import asyncio
import multiprocessing

class IRC_twicth(multiprocessing.Process):

    def __init__(self, config, chind_pipe):
        super(IRC_twicth, self).__init__()
        self.nick = config['twitch']['nick']
        self.channel = config['twitch']['channel']
        self.password = config['twitch']['password']
        self.pipe = chind_pipe
        self.host = config['twitch']['host'].strip()
        self.port = int(config['twitch']['post'])

    def run(self):
        loop = asyncio.get_event_loop()
        connect_coro = loop.create_connection(lambda: self.Twitch_IRC_proto(self.nick, self.password, self.channel, self.pipe),host = self.host, port = self.port)
        transport, protocol = loop.run_until_complete(connect_coro)
        loop.run_forever()

    class Twitch_IRC_proto(asyncio.Protocol):
        transport = None

        def __init__(self, nick, password, channel, pipe):
            self.nick = nick
            self.password = password
            self.channel = channel
            self.pipe = pipe

        def connection_made(self, transport):
            self.transport = transport
            self.transport.write(bytes('PASS oauth:%s\r\n' % self.password, 'UTF-8'))
            self.transport.write(bytes('NICK %s\r\n' % self.nick, 'UTF-8'))
            self.transport.write(bytes('JOIN %s\r\n' % self.channel, 'UTF-8'))

        def data_received(self, data):
            line = data.decode('UTF-8')

            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:

                if line[0] == 'PING':
                    self.pong_send(line[1])

                if line[1] == 'PRIVMSG':
                    sender = self.get_sender(line[0])
                    message = self.get_message(line)
                    #print(':TWITCH: ' + sender + ": " + message)
                    self.pipe.send(':TWITCH: '+sender + ": " + message)

        def pong_send(self, msg):
            self.transport.write(bytes('PONG %s\r\n' % msg, 'UTF-8'))

        def get_sender(self, msg):
            result = ""
            for char in msg:
                if char == "!":
                    break
                if char != ":":
                    result += char
            return result

        def get_message(self, msg):
            result = ""
            i = 3
            length = len(msg)
            while i < length:
                result += msg[i] + " "
                i += 1
            result = result.lstrip(':')
            return result


if __name__ == "__main__":
    IRC_twicth(None, None).run()