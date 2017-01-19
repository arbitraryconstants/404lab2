import socket

# AF_INET means we want an IPV4 socket
# SOCKET_STREAM means we want a TCP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Port 80 is standard port for http
clientSocket.connect(("www.google.com", 80))

request = "GET / HTTP/1.0\r\n\r\n" # \r\n\r\n two blank lines signifies the end of the header

clientSocket.sendall(request)

response = bytearray()
while True:
    part = clientSocket.recv(1024)
    if (part):
        response.extend(part)
    else:
        break

print response















