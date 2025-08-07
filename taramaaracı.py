import nmap

scanner=nmap.PortScanner()
ip="1.1.1.1"
print(scanner.scaninfo())
