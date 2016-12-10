#-*- coding:utf-8 -*-
from tornado.tcpserver import TCPServer, IOStream
from tornado.gen import coroutine
import ssl
from tornado.ioloop import IOLoop
import socket
import tornado.iostream
import os

class StreamToSquid():

    def __init__(self,clientStream):
        self.clientStream = clientStream
        squidsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
        self.squidstream = IOStream(squidsock)
        self.squidstream.connect(('127.0.0.1', 3128), callback=self.handleSquidStream)

    @coroutine
    def handleSquidStream(self):
        self.readClientWriteSquid()
        while True:
            try:
                data = yield self.squidstream.read_bytes(4096,partial=True)
                yield self.clientStream.write(data)
            except tornado.iostream.StreamClosedError as e:
                break
            except Exception:
                break
            if not data:
                break
        self.closeAllStream()


    @coroutine
    def readClientWriteSquid(self):
        while True:
            try:
                data = yield self.clientStream.read_bytes(4096,partial=True)
                yield self.squidstream.write(data)
            except tornado.iostream.StreamClosedError as e:
                break
            except Exception:
                break
            if not data:
                break
        self.closeAllStream()

    def closeAllStream(self):
        if not self.clientStream.closed():
            self.clientStream.close()
        if not self.squidstream.closed():
            self.squidstream.close()

class Proxy(TCPServer):

    def __init__(self, certinfo):
        super(Proxy, self).__init__(ssl_options=certinfo)

    @coroutine
    def handle_stream(self, stream, address):
        print('get new Connection... PID : %s' % os.getpid())
        squidStream = StreamToSquid(stream)



if __name__ == '__main__':
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain('cert.pem','key.pem')
    server = Proxy(ssl_ctx)
    # server.listen(9205)
    server.bind(9205)
    server.start(0)
    IOLoop.current().start()