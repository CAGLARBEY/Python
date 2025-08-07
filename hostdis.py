from scapy.all import *
conf.iface="eth0"
def ping(host):
    paket=IP(dst=host)/ICMP()
    yanıt=sr1(packet,timeout=1 , verbose=0)

    if response:
        return True
    else:
        return False
def tarama(ag):
    aktifListe=[]

    for i in range(256):
        ip=f"{ag}.{i}"
        if ping(ip):
            aktifListe.append(ip)
    return aktifListe


ag="192.168.1"
aktifListe=tarama(ag)
print("Aktif cihazlar")
for i in aktifListe:
    print(i)