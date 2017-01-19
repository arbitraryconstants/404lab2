# A proxy is an intermediary between your browser and the web server 

import socket, os, sys, errno, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Reuse the address even if it is in use
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to a particular port
# 0.0.0.0 is not a "real" IP address, means every address on this machine
serverSocket.bind(("0.0.0.0", 8000))
serverSocket.listen(5) # how many the OS will allow to form a queue

while True:
    # Address is who connected to us
    (incomingSocket, address) = serverSocket.accept()
    print("Got a connection from %s" % (repr(address)))
    
    try: 
        reaped = os.waitpid(0, os.WNOHANG)
    except OSError, e:
        if e.errno == errno.ECHILD:
            pass
        else:
            raise
    else:
        print ("Reaped %s" % (repr(reaped)))
   
    if (os.fork() != 0 ):
        continue # parent process

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    clientSocket.connect(("www.google.com", 80))

    # need to enable non-blocking IO so we no longer get stuck on the recv lines
    incomingSocket.setblocking(0)
    clientSocket.setblocking(0)

    while True:
        request = bytearray()
        while True:    
            try:
                part = incomingSocket.recv(1024) # read up to a KB of the request
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    break
                else:
                    raise
            if (part):
                request.extend(part) 
                clientSocket.sendall(part) # forward the request to google
            else: # what happens when empty string
                sys.exit(0) # quit the program
        
        if len(request) > 0:
            print(request)

        response = bytearray()
        while True:
            try:
                part = clientSocket.recv(1024) 
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    break
                else:
                    raise
            if (part):
                response.extend(part)
                incomingSocket.sendall(part) # response from google
            else:
                sys.exit(0) # quit the program
        
        if len(response) > 0:
            print(response)

        select.select(
            [incomingSocket, clientSocket], # read
            [],                             # write
            [incomingSocket, clientSocket], # exceptions
            1.0)                            # timeout








