import paramiko
ip ="192.168.1.40"
port=22
username="kullanıcı"
password="sjfadf"
sshBaglantı=paramiko.SSHClient()
sshBaglantı.set_missing_host_key_policy(paramiko.AutoAddPolicy)
sshBaglantı.connect(ip,port=port,username=username,password=password)
sshBaglantı.exec_command()#Komut göndermeye yarar.
