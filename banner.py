import socket
ip="192.168.1.40"
liste=[]
for port in range(1,65565):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(ip,port)
        response=s.recv(1024)

        print(str(port), "open : " , response.decode())
        liste.append(response.decode())

    except socket.timeout as süreasim:
        if (port==80):
            httpMesaj="Get / HTTP/1.0 \r\n\r\n"
            s.send(httpMesaj.encode())
            httpRcv=s.recv(1024)
            print(str(port), "open : ", httpRcv.decode())
        else:
            print("Çözülmedi") 
    except Exception as close:
        pass
        # print (close)
    finally:
        s.close
def kayıt():
    with open("aktifservis.txt","w") as kayit:
        for servis in liste:
            kayit.write(f"{servis}\n")