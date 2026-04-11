
OS: Windows 


# Enumeración

### Nmap

Escaneo inicial (puertos):

```shell
sudo nmap 10.129.26.82 -p- -vvv -sS --min-rate 5000 -n -Pn -oG ports.grep 
```

![[Pasted image 20260410200958.png]]



```ruby
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-09 20:07 -0400
NSE: Loaded 158 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 20:07
Completed NSE at 20:07, 0.00s elapsed
Initiating NSE at 20:07
Completed NSE at 20:07, 0.00s elapsed
Initiating NSE at 20:07
Completed NSE at 20:07, 0.00s elapsed
Initiating Ping Scan at 20:07
Scanning 10.129.26.82 [4 ports]
Completed Ping Scan at 20:07, 0.20s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 20:07
Completed Parallel DNS resolution of 1 host. at 20:07, 0.50s elapsed
Initiating SYN Stealth Scan at 20:07
Scanning 10.129.26.82 [3 ports]
Discovered open port 80/tcp on 10.129.26.82
Discovered open port 1433/tcp on 10.129.26.82
Discovered open port 5985/tcp on 10.129.26.82
Completed SYN Stealth Scan at 20:07, 0.19s elapsed (3 total ports)
Initiating Service scan at 20:07
Scanning 3 services on 10.129.26.82
Completed Service scan at 20:07, 6.81s elapsed (3 services on 1 host)
NSE: Script scanning 10.129.26.82.
Initiating NSE at 20:07
Completed NSE at 20:07, 5.90s elapsed
Initiating NSE at 20:07
Completed NSE at 20:07, 2.77s elapsed
Initiating NSE at 20:07
Completed NSE at 20:07, 0.00s elapsed
Nmap scan report for 10.129.26.82
Host is up (0.18s latency).

PORT     STATE SERVICE  VERSION
80/tcp   open  http     Microsoft IIS httpd 10.0
|_http-title: Did not follow redirect to http://eighteen.htb/
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
1433/tcp open  ms-sql-s Microsoft SQL Server 2022 16.00.1000.00; RTM
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Issuer: commonName=SSL_Self_Signed_Fallback
| Public Key type: rsa
| Public Key bits: 3072
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-04-11T06:57:53
| Not valid after:  2056-04-11T06:57:53
| MD5:     4579 4467 91cf 1cb9 ed2c 2955 d251 adee
| SHA-1:   bece 8681 afbc 9c78 650c 83ed 709a 8536 6ce1 7684
|_SHA-256: d386 5ef9 8077 3591 503c e29e 06d7 4b22 ca8e 2d00 ee94 825c bb0f 4e70 8518 7c4f
| ms-sql-info: 
|   10.129.26.82:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
|_ssl-date: 2026-04-11T07:23:35+00:00; +1d07h15m56s from scanner time.
| ms-sql-ntlm-info: 
|   10.129.26.82:1433: 
|     Target_Name: EIGHTEEN
|     NetBIOS_Domain_Name: EIGHTEEN
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: eighteen.htb
|     DNS_Computer_Name: DC01.eighteen.htb
|     DNS_Tree_Name: eighteen.htb
|_    Product_Version: 10.0.26100
5985/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1d07h15m55s, deviation: 0s, median: 1d07h15m54s

NSE: Script Post-scanning.
Initiating NSE at 20:07
Completed NSE at 20:07, 0.00s elapsed
Initiating NSE at 20:07
Completed NSE at 20:07, 0.00s elapsed
Initiating NSE at 20:07
Completed NSE at 20:07, 0.00s elapsed
Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.66 seconds
           Raw packets sent: 7 (284B) | Rcvd: 4 (160B)
```


Vemos que hay 3 puertos abiertos (IIS, mssql, httpapi):

Intentamos una autenticación hacia mssql  con las credenciales que nos dieron en hack the box:

![[Pasted image 20260410202031.png]]

Comprobadas las conexiones a la base de datos, podemos intentar conectarnos usando `impacket-mssqlclient.py`:

![[Pasted image 20260410210800.png]]