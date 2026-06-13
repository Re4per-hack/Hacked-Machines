OS: Windows

```ruby
sudo nmap 10.129.228.120 -p- --min-rate 5000 -sS -Pn -n -oN ports
```

```ruby
# Nmap 7.99 scan initiated Fri Jun 12 18:23:57 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p- --min-rate 5000 -sS -Pn -n -oN /home/juan/Hacking/Flight/nmap/ports 10.129.228.120
Nmap scan report for 10.129.228.120
Host is up (0.17s latency).
Not shown: 65518 filtered tcp ports (no-response)
PORT      STATE SERVICE
53/tcp    open  domain
80/tcp    open  http
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
9389/tcp  open  adws
49667/tcp open  unknown
49673/tcp open  unknown
49674/tcp open  unknown
49692/tcp open  unknown

# Nmap done at Fri Jun 12 18:24:37 2026 -- 1 IP address (1 host up) scanned in 39.67 seconds

```

Ahora haremos un escaneo preciso a cada puerto encontrado:

```ruby
sudo nmap 10.129.228.120 -p53,80,88,135,139,389,445,464,593,636,3268,3269,9389,49667,49673,49674,49692 -sCV -T5 -vvv -oN Exact_scan
```

```ruby
# Nmap 7.99 scan initiated Fri Jun 12 18:24:37 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p53,80,88,135,139,389,445,464,593,636,3268,3269,9389,49667,49673,49674,49692 -sCV -T5 -vvv -oN /home/juan/Hacking/Flight/nmap/Exact_scan 10.129.228.120
Nmap scan report for 10.129.228.120
Host is up, received echo-reply ttl 127 (0.18s latency).
Scanned at 2026-06-12 18:24:38 EDT for 106s

PORT      STATE SERVICE       REASON          VERSION
53/tcp    open  domain        syn-ack ttl 127 Simple DNS Plus
80/tcp    open  http          syn-ack ttl 127 Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)
|_http-server-header: Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.1
|_http-title: g0 Aviation
| http-methods: 
|   Supported Methods: HEAD GET POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
88/tcp    open  kerberos-sec  syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2026-06-13 05:24:45Z)
135/tcp   open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
389/tcp   open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: flight.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds? syn-ack ttl 127
464/tcp   open  kpasswd5?     syn-ack ttl 127
593/tcp   open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped    syn-ack ttl 127
3268/tcp  open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: flight.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped    syn-ack ttl 127
9389/tcp  open  mc-nmf        syn-ack ttl 127 .NET Message Framing
49667/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49673/tcp open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49692/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
Service Info: Host: G0; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 50845/tcp): CLEAN (Timeout)
|   Check 2 (port 23690/tcp): CLEAN (Timeout)
|   Check 3 (port 21917/udp): CLEAN (Timeout)
|   Check 4 (port 7712/udp): CLEAN (Timeout)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
|_clock-skew: 6h59m59s
| smb2-time: 
|   date: 2026-06-13T05:25:39
|_  start_date: N/A

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Jun 12 18:26:24 2026 -- 1 IP address (1 host up) scanned in 106.64 seconds

```

