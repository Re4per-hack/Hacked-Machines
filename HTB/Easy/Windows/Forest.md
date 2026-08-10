OS: Windows

# Enumeration

We look at the open ports:

```bash
sudo nmap 10.129.4.30 -p- --min-rate 5000 -sS -Pn -n -oN ports
```

```console
Nmap scan report for 10.129.4.30
Host is up (0.19s latency).
PORT      STATE SERVICE
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
5985/tcp  open  wsman
9389/tcp  open  adws
47001/tcp open  winrm
49664/tcp open  unknown
(... additional high RPC ports ...)
```

Now we run a detailed scan against each port we found:

```bash
sudo nmap 10.129.4.30 -p53,88,135,139,389,445,464,593,636,3268,3269,5985,9389,47001,... -sCV -T5 -vvv -oN Exact_scan
```

```console
PORT      STATE SERVICE      VERSION
53/tcp    open  domain       Simple DNS Plus
88/tcp    open  kerberos-sec Microsoft Windows Kerberos
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local)
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 (workgroup: HTB)
636/tcp   open  tcpwrapped
3268/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local)
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
9389/tcp  open  mc-nmf       .NET Message Framing
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery:
|   OS: Windows Server 2016 Standard 14393
|   Computer name: FOREST
|   Domain name: htb.local
|   FQDN: FOREST.htb.local
```

_(Writeup in progress — enumeration completed; exploitation section to be added.)_
