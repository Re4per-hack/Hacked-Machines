OS: Linux

# Enumeración

Miramos los puertos abiertos:

```ruby
sudo nmap 10.129.3.232 -p- --min-rate 5000 -sS -Pn -n -oN ports
```

```ruby
# Nmap 7.99 scan initiated Sun May 24 00:49:32 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p- --min-rate 5000 -sS -Pn -n -oN /home/juan/Hacking/nmap/ports 10.129.3.232
Nmap scan report for 10.129.3.232
Host is up (0.19s latency).
Not shown: 65532 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
54321/tcp open  unknown

# Nmap done at Sun May 24 00:49:49 2026 -- 1 IP address (1 host up) scanned in 16.55 seconds

```

Ahora haremos un escaneo preciso a cada puerto encontrado:

```ruby
sudo nmap 10.129.3.232 -p22,80,54321 -sCV -T5 -vvv -oN Exact_scan
```

```python
# Nmap 7.99 scan initiated Sun May 24 00:49:49 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p22,80,54321 -sCV -T5 -vvv -oN /home/juan/Hacking/nmap/Exact_scan 10.129.3.232
Nmap scan report for 10.129.3.232
Host is up, received echo-reply ttl 63 (0.18s latency).
Scanned at 2026-05-24 00:49:50 EDT for 37s

PORT      STATE SERVICE REASON         VERSION
22/tcp    open  ssh     syn-ack ttl 63 OpenSSH 9.9p1 Ubuntu 3ubuntu3.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4d:d7:b2:8c:d4:df:57:9c:a4:2f:df:c6:e3:01:29:89 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNYjzL0v+zbXt5Zvuhd63ZMVGK/8TRBsYpIitcmtFPexgvOxbFiv6VCm9ZzRBGKf0uoNaj69WYzveCNEWxdQUww=
|   256 a3:ad:6b:2f:4a:bf:6f:48:ac:81:b9:45:3f:de:fb:87 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPCNb2NXAGnDBofpLTCGLMyF/N6Xe5LIri/onyTBifIK
80/tcp    open  http    syn-ack ttl 63 nginx 1.26.3 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.26.3 (Ubuntu)
|_http-title: Did not follow redirect to http://facts.htb/
54321/tcp open  http    syn-ack ttl 62 Golang net/http server
|_http-title: Did not follow redirect to http://10.129.3.232:9001
|_http-server-header: MinIO
| http-methods: 
|_  Supported Methods: GET OPTIONS
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 400 Bad Request
|     Accept-Ranges: bytes
|     Content-Length: 303
|     Content-Type: application/xml
|     Server: MinIO
|     Strict-Transport-Security: max-age=31536000; includeSubDomains
|     Vary: Origin
|     X-Amz-Id-2: dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8
|     X-Amz-Request-Id: 18B26725E7A114E4
|     X-Content-Type-Options: nosniff
|     X-Xss-Protection: 1; mode=block
|     Date: Sun, 24 May 2026 04:50:15 GMT
|     <?xml version="1.0" encoding="UTF-8"?>
|     <Error><Code>InvalidRequest</Code><Message>Invalid Request (invalid argument)</Message><Resource>/nice ports,/Trinity.txt.bak</Resource><RequestId>18B26725E7A114E4</RequestId><HostId>dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8</HostId></Error>
|   GenericLines, Help, RTSPRequest, SSLSessionReq: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 400 Bad Request
|     Accept-Ranges: bytes
|     Content-Length: 276
|     Content-Type: application/xml
|     Server: MinIO
|     Strict-Transport-Security: max-age=31536000; includeSubDomains
|     Vary: Origin
|     X-Amz-Id-2: dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8
|     X-Amz-Request-Id: 18B26721D303E174
|     X-Content-Type-Options: nosniff
|     X-Xss-Protection: 1; mode=block
|     Date: Sun, 24 May 2026 04:49:57 GMT
|     <?xml version="1.0" encoding="UTF-8"?>
|     <Error><Code>InvalidRequest</Code><Message>Invalid Request (invalid argument)</Message><Resource>/</Resource><RequestId>18B26721D303E174</RequestId><HostId>dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8</HostId></Error>
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Vary: Origin
|     Date: Sun, 24 May 2026 04:49:58 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port54321-TCP:V=7.99%I=7%D=5/24%Time=6A128375%P=x86_64-pc-linux-gnu%r(G
SF:enericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20
SF:text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\
SF:x20Request")%r(GetRequest,2B0,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nAc
SF:cept-Ranges:\x20bytes\r\nContent-Length:\x20276\r\nContent-Type:\x20app
SF:lication/xml\r\nServer:\x20MinIO\r\nStrict-Transport-Security:\x20max-a
SF:ge=31536000;\x20includeSubDomains\r\nVary:\x20Origin\r\nX-Amz-Id-2:\x20
SF:dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8\r\nX-A
SF:mz-Request-Id:\x2018B26721D303E174\r\nX-Content-Type-Options:\x20nosnif
SF:f\r\nX-Xss-Protection:\x201;\x20mode=block\r\nDate:\x20Sun,\x2024\x20Ma
SF:y\x202026\x2004:49:57\x20GMT\r\n\r\n<\?xml\x20version=\"1\.0\"\x20encod
SF:ing=\"UTF-8\"\?>\n<Error><Code>InvalidRequest</Code><Message>Invalid\x2
SF:0Request\x20\(invalid\x20argument\)</Message><Resource>/</Resource><Req
SF:uestId>18B26721D303E174</RequestId><HostId>dd9025bab4ad464b049177c95eb6
SF:ebf374d3b3fd1af9251148b658df7ac2e3e8</HostId></Error>")%r(HTTPOptions,5
SF:9,"HTTP/1\.0\x20200\x20OK\r\nVary:\x20Origin\r\nDate:\x20Sun,\x2024\x20
SF:May\x202026\x2004:49:58\x20GMT\r\nContent-Length:\x200\r\n\r\n")%r(RTSP
SF:Request,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text
SF:/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20R
SF:equest")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:
SF:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20
SF:Bad\x20Request")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x20Bad\x20Request
SF:\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20clo
SF:se\r\n\r\n400\x20Bad\x20Request")%r(FourOhFourRequest,2CB,"HTTP/1\.0\x2
SF:0400\x20Bad\x20Request\r\nAccept-Ranges:\x20bytes\r\nContent-Length:\x2
SF:0303\r\nContent-Type:\x20application/xml\r\nServer:\x20MinIO\r\nStrict-
SF:Transport-Security:\x20max-age=31536000;\x20includeSubDomains\r\nVary:\
SF:x20Origin\r\nX-Amz-Id-2:\x20dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af
SF:9251148b658df7ac2e3e8\r\nX-Amz-Request-Id:\x2018B26725E7A114E4\r\nX-Con
SF:tent-Type-Options:\x20nosniff\r\nX-Xss-Protection:\x201;\x20mode=block\
SF:r\nDate:\x20Sun,\x2024\x20May\x202026\x2004:50:15\x20GMT\r\n\r\n<\?xml\
SF:x20version=\"1\.0\"\x20encoding=\"UTF-8\"\?>\n<Error><Code>InvalidReque
SF:st</Code><Message>Invalid\x20Request\x20\(invalid\x20argument\)</Messag
SF:e><Resource>/nice\x20ports,/Trinity\.txt\.bak</Resource><RequestId>18B2
SF:6725E7A114E4</RequestId><HostId>dd9025bab4ad464b049177c95eb6ebf374d3b3f
SF:d1af9251148b658df7ac2e3e8</HostId></Error>");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun May 24 00:50:27 2026 -- 1 IP address (1 host up) scanned in 38.31 seconds

```

Como vemos en nmap  **`|_http-title: Did not follow redirect to http://facts.htb/`*** Esto significa que nmap no pudo resolver facts.htb, por lo que lo agregamos en **`/etc/hosts`**:

![[Pasted image 20260524090556.png]]


Vemos que hay una pagina web, por lo que podemos hacer una enumeración rapida con whatsweb a ver que nos encontramos:

````ruby
whatweb http://10.129.4.18
````

````RUBY
http://10.129.4.18 [302 Found] Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][nginx/1.26.3 (Ubuntu)], IP[10.129.4.18], RedirectLocation[http://facts.htb/], Title[302 Found], nginx[1.26.3]
http://facts.htb/ [200 OK] Cookies[_factsapp_session], Country[RESERVED][ZZ], Email[contact@facts.htb], HTML5, HTTPServer[Ubuntu Linux][nginx/1.26.3 (Ubuntu)], HttpOnly[_factsapp_session], IP[10.129.4.18], Open-Graph-Protocol[website], Script, Title[facts], UncommonHeaders[x-content-type-options,x-permitted-cross-domain-policies,referrer-policy,plugin_front_cache,link,x-request-id], X-Frame-Options[SAMEORIGIN], X-UA-Compatible[IE=edge], X-XSS-Protection[0], nginx[1.26.3]

````

Confirmamos que estamos ante un servidor nginx en una maquina linux, ahora podemos visitar el sitio:

![[Pasted image 20260524091228.png]]

Buscando por la pagina no encontramos ningun vector de entrada principal por lo que podemos buscar por subdirectorios alternativos fuzzeando la pagina web:

![[Pasted image 20260524092020.png]]

Encontramos un endpoint interesante llamado "admin", visitandolo nos redirige a `/admin/login` encontramos lo siguiente:

![[Pasted image 20260524092323.png]]

Credenciales por defecto como `admin`/`admin`  o `admin`/`1234` no sirvieron, por lo que podemos intentar crear una cuenta a ver que encontramos:

![[Pasted image 20260524092551.png]]

Nos lleva a un panel, que como podemos ver abajo del todo, está basada en el CMS camaleon en la versión 2.9.0 (Vulnerable)


![[Pasted image 20260524092729.png]]


Investigando esta versión encontré el CVE: `CVE-2025-2304`:

![[Pasted image 20260524092923.png]]

Vemos que hay una vulnerabilidad que nos permite elevar nuestros privilegios de la cuenta test a **`admin`**, ademas, podemos ver que camaleon tiene cierta relacion con AWS S3, es decir, podemos obtener credenciales privilegiadas para obtener archivos privilegiados:

![[Pasted image 20260524131643.png]]

Ahora nuestra cuenta **test** es administradora, intentemos loggearnos usando las nuevas credenciales: `test`/`test`:

![[Screenshot 2026-05-24 141951.png]]

Primero debemos configurar el aws s3:

```ruby
aws s3 configure
```

![[Pasted image 20260524145050.png]]

Ahora podemos ver que hay dentro de este servidor, especificamente al endpoint que nos especificaba la pagina `{IP}:54321`:

![[Pasted image 20260524145238.png]]

Lo que vemos son los buckets, entremos a internal a ver que encontramos:

![[Pasted image 20260524145300.png]]

El directorio **.ssh** es importante ya que es donde se guardan las llaves privadas/publicas de ssh:

![[Pasted image 20260524151630.png]]

El archivo id_ed25519 parece ser una llave privada, intentemos descargarla a nuestro directorio de trabajo usando cp:

![[Pasted image 20260524151805.png]]

Perfecto, ahora podemos usar esta llave privada, la pregunta es, con cual usuario?, cuando investigué acerca de las vulnerabilidades de camaleon CMS 2.9.0, tambien encontré una vulnerabilidad de tipo LFi, especificamente en ***`/admin/media/download_private_file`***  y el parametro ***`file=`***, de esta forma podemos obtener el archivo **`/etc/passwd`** y de ahí sacar los usuarios del sistema para probar con cual nos sirve la llave privada:

![[Pasted image 20260524184527.png]]

Revisando el archivo encontramos 3 usuarios principales: (root, trivia, william).

![[Pasted image 20260524184329.png]]

Perfecto, ahora podemos intentar conectarnos por ssh, vemos que cuando intentamos usar la lalve privada para el usuario trivia, vemos que nos pide el passprhase, que es basicamente una contraseña que protege la llave privada:

![[Pasted image 20260524185017.png]]

Lo mejor que podemos hacer en este caso es extraer un hash basado en el passprhase para romper la contraseña de la llave privada protegida:

![[Pasted image 20260524190937.png]]

Ahora si, podemos crackearlo con john, lo que nos da la siguiente contraseña:

![[Pasted image 20260524191047.png]]

Listo!, Ahora podemos conectarnos a ssh usando la lalve privada y proporcionando el passphrase ***`dragonballz`***:

![[Pasted image 20260524191227.png]]

Vemos que podemos ejecutar **`/usr/bin/facter`** como root usando root:

![[Pasted image 20260524191259.png]]

Busque facter en nuestro viejo confiable [GTFOBins](https://gtfobins.org/gtfobins/facter/):

![[Pasted image 20260524193704.png]]

Como dice GTFOBins, facter va a ejecutar el primer archivo .rb que encuentre en la ruta especificada, y como lo estamos ejecutando con sudo, el codigo ruby se va a ejecutar con permisos administrativos (root), por lo que nos conviene usar una reverse shell de ruby ej: [Aqui](https://github.com/secjohn/ruby-shells/blob/master/revshell.rb):

![[Pasted image 20260524230147.png]]

Ahora hacemos que facter lo ejecute:

![[Pasted image 20260524230737.png]]

![[Pasted image 20260524230822.png]]


# Maquina Completa




