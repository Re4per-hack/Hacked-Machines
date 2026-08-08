OS: Windows

# Enumeración

Miramos los puertos abiertos:

```ruby
sudo nmap 10.129.4.30 -p- --min-rate 5000 -sS -Pn -n -oN ports
```

```ruby
# Nmap 7.99 scan initiated Tue May 26 19:42:51 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p- --min-rate 5000 -sS -Pn -n -oN /home/juan/Hacking/Forest/nmap/ports 10.129.4.30
Nmap scan report for 10.129.4.30
Host is up (0.19s latency).
Not shown: 65511 closed tcp ports (reset)
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
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49670/tcp open  unknown
49676/tcp open  unknown
49677/tcp open  unknown
49681/tcp open  unknown
49698/tcp open  unknown
54303/tcp open  unknown

# Nmap done at Tue May 26 19:43:07 2026 -- 1 IP address (1 host up) scanned in 16.65 seconds

```

Ahora haremos un escaneo preciso a cada puerto encontrado:

```ruby
sudo nmap 10.129.4.30 -p53,88,135,139,389,445,464,593,636,3268,3269,5985,9389,47001,49664,49665,49666,49667,49670,49676,49677,49681,49698,54303 -sCV -T5 -vvv -oN Exact_scan
```

```ruby
# Nmap 7.99 scan initiated Tue May 26 19:43:08 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p53,88,135,139,389,445,464,593,636,3268,3269,5985,9389,47001,49664,49665,49666,49667,49670,49676,49677,49681,49698,54303 -sCV -T5 -vvv -oN /home/juan/Hacking/Forest/nmap/Exact_scan 10.129.4.30
Nmap scan report for 10.129.4.30
Host is up, received echo-reply ttl 127 (0.19s latency).
Scanned at 2026-05-26 19:43:09 EDT for 79s

PORT      STATE SERVICE      REASON          VERSION
53/tcp    open  domain       syn-ack ttl 127 Simple DNS Plus
88/tcp    open  kerberos-sec syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2026-05-26 23:50:04Z)
135/tcp   open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn  syn-ack ttl 127 Microsoft Windows netbios-ssn
389/tcp   open  ldap         syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds syn-ack ttl 127 Windows Server 2016 Standard 14393 microsoft-ds (workgroup: HTB)
464/tcp   open  kpasswd5?    syn-ack ttl 127
593/tcp   open  ncacn_http   syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped   syn-ack ttl 127
3268/tcp  open  ldap         syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped   syn-ack ttl 127
5985/tcp  open  http         syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf       syn-ack ttl 127 .NET Message Framing
47001/tcp open  http         syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49665/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49666/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49667/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49670/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49676/tcp open  ncacn_http   syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
49677/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49681/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49698/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
54303/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2026-05-26T16:50:57-07:00
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 45558/tcp): CLEAN (Couldn't connect)
|   Check 2 (port 39362/tcp): CLEAN (Couldn't connect)
|   Check 3 (port 41484/udp): CLEAN (Failed to receive data)
|   Check 4 (port 40840/udp): CLEAN (Timeout)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required
|_clock-skew: mean: 2h26m48s, deviation: 4h02m31s, median: 6m46s
| smb2-time: 
|   date: 2026-05-26T23:50:55
|_  start_date: 2026-05-26T23:35:30
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue May 26 19:44:28 2026 -- 1 IP address (1 host up) scanned in 80.76 seconds

```

