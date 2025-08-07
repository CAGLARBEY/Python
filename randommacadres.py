from scapy.all import * 
srcMac=RandMAC()
dstMac=RandMAC()
srcIp=RandIP()
dstIp=RandIP()

ether=Ether(src=srcMac,dst=dstMac)
ip=IP(src=srcIp,dst=dstIp)
packet=ether/ip
# paketi gönderme
sendp(packet,iface="eth0")
