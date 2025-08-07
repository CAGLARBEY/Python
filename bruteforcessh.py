import paramiko

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ip="1.1.1.1"
port=22
username="admin"
password="admin"
ssh.connect(ip,port=port,username=username,password=password)
command1="cat /etc/passwd"

stdin,stdout,stderr=ssh.exec_command(command1)
cmd_output=stdout.read
ssh.close()
print(cmd_output)

etcpaswd=cmd_output.decode().split("\n")
for i in etcpaswd:
    print(i)
