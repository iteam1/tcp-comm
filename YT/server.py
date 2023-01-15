'''
Client: img:path/img,model:type_of_model
Server: img:path/img,result:result_of_model
'''
import socket

if __name__ == "__main__":

    ip = "127.0.0.1"
    port = 1234

    # init server tcp
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))

    # server listen client timeout = 5
    print('Server listening')
    server.listen(5)

    while True:
        client,address = server.accept()
        print(f'Connection Established - {address[0]}:{address[1]}')

        # read client request
        request = client.recv(1024) # number of bytes
        request = request.decode("utf-8")
        print("Client Message: ",request)

        # check the message
        if request == '1234':
            response = 'Correct Number!'
            client.send(bytes(response,'utf-8'))
        else:
            response = 'Wrong Number!'
            client.send(bytes(response,'utf-8'))

        client.close()
