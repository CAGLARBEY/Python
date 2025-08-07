from scapy.all import *

def sniccPCKT(pkt):
    pkt.show()
# Paketleri yakalamak için fonksiyon
def snffpack(pck):
    pck.show()
    wrpcap("a.pcap", pck, append=True)

# Ağ arayüzünü belirt ve paketleri yakala
sniff(prn=snffpack, timeout=5, iface="eth0", stop_filter=lambda x: x.haslayer(ICMP))
def read():
    scap_cap=rdpcap("a.pcap")
    ip_list=[]
    for pckt in scap_cap:
        if pckt [IP].src not in ip_list:
            ip_list.append(pckt[IP].src)
        else:    
            pckt.show

print ("1: sniff 2: read ")
secim=input(">> ")
if secim=="1":
    snffpack()
elif secim== "2":
    read()
else:
    print("Hatali giriş yaptiniz ")