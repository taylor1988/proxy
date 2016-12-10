#-*- coding:utf-8 -*-
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.connect(('45.78.36.229', 12345))
fp = open('local.tar','wb')
data = sock.recv(4096)
lencunt = 0
while data:
    fp.write(data)
    lencunt += len(data)
    print('已读取 -- %s' % lencunt)
    data = sock.recv(4096)

print('写入完成...')