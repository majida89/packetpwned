---
title: "John the Ripper — TryHackMe"
date: 2026-06-23
description: "A deep dive into password cracking with John the Ripper — hashes, wordlists, custom rules, zip/RAR files, and SSH keys."
tags: ["TryHackMe", "Password Cracking", "John", "Linux", "Jr Pentester"]
---

## Overview

John the Ripper (JtR) is one of the most widely used password cracking tools in offensive security. This room on TryHackMe walks through everything from cracking basic hashes to protected archives and SSH private keys. One of the best rooms on the platform — highly recommended.

**Room:** [John the Ripper](https://tryhackme.com/room/johntheripper0)  
**Difficulty:** Easy  
**Path:** Jr Penetration Tester

---

## What is John the Ripper?

John the Ripper is an open-source, fast password cracker. It supports hundreds of hash types and can operate in several modes:

- **Wordlist mode** — tries every word in a list
- **Single crack mode** — uses the username and GECOS fields to mangle passwords
- **Incremental mode** — brute-forces all character combinations

The community-enhanced version (`john` from Jumbo) supports more formats and is what's installed on most pentesting distros.

---

## Basic Syntax

```bash
john [options] <hash-file>

# Specify wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# Specify format explicitly
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# Show cracked passwords
john --show hash.txt
```

---

## Task 1 — Cracking Basic Hashes

John can auto-detect many hash types, but you can force a format with `--format`.

```bash
# Auto-detect
john --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt

# MD5
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt

# SHA1
john --format=raw-sha1 --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt

# SHA256
john --format=raw-sha256 --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt
```

**Tip:** Use `hash-identifier` or [hashes.com](https://hashes.com/en/tools/hash_identifier) to identify an unknown hash type before cracking.

---

## Task 2 — Cracking Windows Hashes (NTLM)

Windows stores passwords as NTLM hashes in the SAM database. Once you have a hash (via Mimikatz, secretsdump, etc.), crack it like this:

```bash
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt ntlm.txt
```

NTLM is unsalted, which makes it fast to crack and vulnerable to pass-the-hash attacks.

---

## Task 3 — Cracking /etc/shadow Hashes

Linux stores hashed passwords in `/etc/shadow`. To crack them, first combine `/etc/passwd` and `/etc/shadow` using `unshadow`, then feed to John:

```bash
unshadow /etc/passwd /etc/shadow > unshadowed.txt
john --wordlist=/usr/share/wordlists/rockyou.txt unshadowed.txt
```

Common Linux hash formats you'll encounter:

| Prefix | Algorithm |
|--------|-----------|
| `$1$`  | MD5       |
| `$2$`  | Blowfish  |
| `$5$`  | SHA-256   |
| `$6$`  | SHA-512   |

---

## Task 4 — Single Crack Mode

Single crack mode is useful when you know the username. John mangles the username with rules to generate password candidates — surprisingly effective against weak passwords.

```bash
john --single --format=raw-sha256 hash.txt
```

The hash file needs the username prepended:

```
mike:1efee03cdcb96d90ad48ccc7b8666033
```

---

## Task 5 — Custom Rules

Custom rules let you define mangling patterns — extremely powerful for targeted cracking when you know the password policy.

Rules go in `/etc/john/john.conf` under `[List.Rules:RuleName]`.

**Example rule** — capitalise first letter, append a digit and symbol:

```ini
[List.Rules:THMRules]
Az"[0-9]" ^[!@#$]
cAz"[0-9]" ^[!@#$]
```

**Rule syntax:**

| Symbol | Meaning |
|--------|---------|
| `Az`   | Append characters from the set |
| `A0`   | Prepend characters from the set |
| `c`    | Capitalise first letter |
| `^`    | Prepend a character |
| `[0-9]` | Character class — digits |

Use the rule:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt --rules=THMRules hash.txt
```

---

## Task 6 — Cracking Password-Protected Zip Files

John can crack protected zip files using `zip2john` to extract the hash first:

```bash
zip2john protected.zip > zip_hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt zip_hash.txt
```

Once cracked, extract with:

```bash
unzip -P <password> protected.zip
```

---

## Task 7 — Cracking Password-Protected RAR Archives

Same workflow using `rar2john`:

```bash
rar2john protected.rar > rar_hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt rar_hash.txt
```

---

## Task 8 — Cracking SSH Key Passphrases

If you find an encrypted SSH private key (`id_rsa`) during an engagement, extract the hash with `ssh2john` and crack it:

```bash
ssh2john id_rsa > ssh_hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt ssh_hash.txt
```

Then use the cracked passphrase to log in:

```bash
ssh -i id_rsa user@target
```

---

## Key Takeaways

- Always try `--single` first — it's fast and catches weak/obvious passwords
- `rockyou.txt` covers the majority of CTF passwords; for real engagements use curated lists or `CeWL` to generate target-specific wordlists
- When auto-detection fails, use `--format=` explicitly — run `john --list=formats` to see all supported types
- The `*2john` tools (`zip2john`, `ssh2john`, `rar2john`) are your bridge between protected files and John
- Custom rules are a multiplier — learning the syntax pays off fast

---

## Tools Referenced

| Tool | Purpose |
|------|---------|
| `john` | Core password cracker |
| `unshadow` | Combine passwd + shadow for Linux cracking |
| `zip2john` | Extract hash from protected zip |
| `rar2john` | Extract hash from protected RAR |
| `ssh2john` | Extract hash from encrypted SSH key |
| `hash-identifier` | Identify unknown hash types |
| `rockyou.txt` | Most commonly used wordlist (`/usr/share/wordlists/`) |
