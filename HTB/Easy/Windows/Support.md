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

