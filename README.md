# HTB Writeups

A collection of **Hack The Box** machines, solved and documented step by step:
enumeration, exploitation and privilege escalation — explaining the *why* behind
each step, not just the commands.

🔗 **[Read the writeups](https://re4per-hack.github.io/)**  <!-- adjust to your GitHub Pages URL -->

## Machines

Organized by difficulty and operating system:

```
Easy/
  Linux/     CCTV, Facts, Kobold, ...
  Windows/   Eighteen, Forest, MonitorsFour, Support, ...
Hard/
  Windows/   ...
```

Each writeup covers the full path through the machine, from the first scan to
root/administrator.

---

## How it's built

The site is published automatically with Jekyll on GitHub Pages. Writeups are
written in Obsidian (markdown), and a small script (`build.py`) adapts them to
Jekyll's format so there's no HTML to touch by hand.

To add a machine:

1. Write the writeup in Obsidian using `![[image.png]]` for screenshots.
2. Save it in its difficulty/OS folder (`Easy/Linux/`, etc.) and the images in `Images/`.
3. Convert and push:

   ```bash
   python3 build.py
   git add .
   git commit -m "feat: add <machine> writeup"
   git push
   ```

GitHub Pages rebuilds the site automatically.
