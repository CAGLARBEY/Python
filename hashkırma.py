import subprocess
import crypt
shadow=subprocess.check_output("cat /etc/shadow",shell=True).decode()
print(shadow)
passwdlist=shadow.split("\n")
f=open("wordlist.txt","r")
for i in passwdlist:
    print(i)
    if "kali" in i:
        s=i.split("$")
        salt="$"+s[2]+"$"+s[3]
        print(salt)        
        for passwdtry in f:
            tmp_passwd=crypt.crypt(passwdtry.strip(),salt)
            print(tmp_passwd)
            if tmp_passwd in i:
                print("Şifreniz : " , passwdtry.strip())