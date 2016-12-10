# -*- coding:utf-8 -*-
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
from tornado.gen import coroutine

class FileServer(TCPServer):

    @coroutine
    def handle_stream(self, stream, address):
        print('new connection ...', address)
        fp = open('/root/aa.tar', 'rb')
        data = fp.read(4096)
        while data :
            yield stream.write(data)
            data = fp.read(4096)
        fp.close()
        stream.close()
        print('传输完成..')


if __name__ == '__main__':
    port = 12345
    server = FileServer()
    server.listen(port)
    IOLoop.current().start()