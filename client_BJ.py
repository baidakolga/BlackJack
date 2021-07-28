import socket

sock = socket.socket()
sock.connect(('localhost', 9000))

while True:
    data = sock.recv(1024)
    print(data.decode('utf-8'))
    sock.send(input().encode('utf-8'))
    if not data:
        break
sock.close()






