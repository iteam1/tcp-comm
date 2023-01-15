import socket

if __name__ == "__main__":

    ip = "127.0.0.1" # ip of server
    port = 1234 # server port

    # init server connection
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((ip,port))

    # client send request
    request = input("Enter Request Message: ")
    server.send(bytes(request,"utf-8"))

    # client receive server response
    response = server.recv(1024)
    print(response.decode('utf-8'))
