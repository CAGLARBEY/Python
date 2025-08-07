import nmap
nm=nmap.PortScanner()

ip_range="1.1.1.1/10"
nm.scan(ip_range,arguments='-sn')
for host in nm.all_hosts():
    print(host)

ip_list=''.join(nm.all_hosts())
print(ip_list)

nm.scan(ip_list,arguments='-sV')
print(nm.scaninfo())

for ip in nm.all_hosts():
    print(nm[ip]['tcp'.keys()])
    print("---"+20)