import socket
import select
import sys

lshostname = socket.gethostname()
lslistenport = int(sys.argv[1])

ts1hostname = socket.gethostbyname(sys.argv[2])
ts1listenport = int(sys.argv[3])

ts2hostname = socket.gethostbyname(sys.argv[4])
ts2listenport = int(sys.argv[5])

while True: 
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.bind((lshostname,lslistenport))

    cs.listen(10)

    conn, addr = cs.accept() 

    clientdata = conn.recv(4096)  
    if not clientdata:            
         break
    domain_name = clientdata.decode('utf-8')

    ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ts1.connect((ts1hostname, ts1listenport))
    ts2.connect((ts2hostname, ts2listenport))

    ts1.send(clientdata)
    ts2.send(clientdata)

    TIMEOUT = 5.0

    listening_sockets = [ts1, ts2]
    data = (domain_name + " - Error:HOST NOT FOUND").encode('utf-8')

    socket_list = select.select(listening_sockets, [], [], TIMEOUT)[0]
    for this_socket in socket_list:
        try:
            data = this_socket.recv(4096)
        except socket.timeout:
            print("timeout")
    
    conn.sendall(data)
    cs.close()




            
