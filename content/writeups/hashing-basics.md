---
title: "TryHackMe: Hashing Basics"
date: 2026-06-16
description: "Walkthrough of the Hashing Basics room — hash functions, insecure password storage, hash recognition, cracking with hashcat, and integrity checking."
tags: ["tryhackme", "cryptography", "hashing", "hashcat", "password-cracking"]
---

## Overview

**Room:** Hashing Basics  
**Difficulty:** Easy  
**Platform:** TryHackMe  
**Path:** Cyber Security 101 > Cryptography  

---

## What is Hashing?

A **hash function** takes an input of arbitrary size and produces a fixed-length output called a **hash value**. Key properties:

- **Deterministic** — same input always produces the same output
- **One-way** — you cannot reverse a hash to recover the original input
- **Avalanche effect** — a single bit change in the input produces a completely different hash
- **Fixed output size** — regardless of input length, the output is always the same size

Common use cases: password storage, file integrity verification, digital signatures, and data deduplication.

---

## Task 2 — Hash Functions

Hash functions produce a fixed-size digest. Some common algorithms:

| Algorithm | Output Size | Notes |
|---|---|---|
| MD5 | 128 bits / **16 bytes** | Fast, broken for security use — collision attacks exist |
| SHA-1 | 160 bits / 20 bytes | Deprecated — collision demonstrated (SHAttered attack) |
| SHA-256 | 256 bits / 32 bytes | Part of SHA-2 family, widely used |
| SHA-512 | 512 bits / 64 bytes | Stronger variant of SHA-2 |
| bcrypt | 184 bits | Designed for passwords — slow by design |
| yescrypt | 256 bits | Modern password hashing, default on many Linux distros |

If a hash function has an 8-bit output, there are **2^8 = 256** possible hash values. The smaller the output, the higher the collision probability.

```bash
# Compute SHA256 hash of a file
sha256sum passport.jpg

# Compute MD5
md5sum passport.jpg
```

---

## Task 3 — Insecure Password Storage

**The RockYou breach** is the canonical example of why plaintext password storage is catastrophic. RockYou stored millions of user passwords in plaintext; when breached, those passwords became the `rockyou.txt` wordlist — now a standard tool in every pentester's toolkit, sitting at `/usr/share/wordlists/rockyou.txt` on Kali Linux.

Other insecure patterns:
- **Plaintext storage** — no protection at all
- **Encryption** — reversible with the key; wrong tool for passwords
- **Unsalted MD5/SHA1** — fast to crack; rainbow tables work directly against them

```bash
# View first 20 entries in rockyou.txt
head -n 20 /usr/share/wordlists/rockyou.txt
```

---

## Task 4 — Secure Password Storage with Hashing

Proper password storage uses:

- **Slow hashing algorithms** — bcrypt, scrypt, Argon2, yescrypt. Deliberately computationally expensive to slow down brute-force attempts.
- **Salting** — a unique random value added to each password before hashing. Prevents rainbow table attacks and ensures identical passwords produce different hashes.

A **rainbow table** is a precomputed lookup table mapping hashes back to plaintext. Salting defeats this entirely since the attacker would need a separate table per unique salt.

**Why not encrypt passwords?**  
Encryption is reversible. If the key is compromised, all passwords are exposed. Hashing is one-way by design — the system never needs to recover the original password, only verify it.

---

## Task 5 — Recognising Password Hashes

Hash formats follow identifiable patterns, particularly on Linux and network devices:

| Prefix / Format | Algorithm | Context |
|---|---|---|
| `$1$` | MD5crypt | Legacy Linux `/etc/shadow` |
| `$2a$` / `$2b$` | bcrypt | Linux, web apps |
| `$5$` | SHA-256crypt | Linux `/etc/shadow` |
| `$6$` | SHA-512crypt | Linux `/etc/shadow` (common default) |
| `$y$` | yescrypt | Modern Linux distros |
| `$9$` | scrypt | Cisco IOS |
| 32 hex chars | MD5 | Web apps, legacy systems |
| 40 hex chars | SHA-1 | Git commits, older systems |
| 64 hex chars | SHA-256 | File integrity, modern systems |

Tools for identification:
- `hash-identifier` — Python tool, included in Kali
- `hashid` — more accurate, supports more formats
- Hashcat's example hashes page (referenced in `hashcat --example-hashes`)

---

## Task 6 — Password Cracking

**hashcat** is the go-to GPU-accelerated password cracker. Syntax:

```bash
hashcat -m <mode> <hashfile> <wordlist>
```

Common mode numbers:

| Mode | Hash Type |
|---|---|
| 0 | MD5 |
| 100 | SHA-1 |
| 1400 | SHA-256 |
| 1800 | sha512crypt ($6$) |
| 3200 | bcrypt ($2a$/$2b$) |
| 1750 | HMAC-SHA512 (key = $pass) |
| 2410 | Cisco-ASA MD5 |

**Cracking the Task 6 hashes:**

```bash
# hash1.txt — bcrypt ($2a$)
hashcat -m 3200 hash1.txt /usr/share/wordlists/rockyou.txt

# hash2.txt — SHA2-256
hashcat -m 1400 hash2.txt /usr/share/wordlists/rockyou.txt

# hash3.txt — sha512crypt ($6$)
hashcat -m 1800 hash3.txt /usr/share/wordlists/rockyou.txt

# hash4.txt — MD5
hashcat -m 0 hash4.txt /usr/share/wordlists/rockyou.txt
```

Online tools like [hashes.com](https://hashes.com/en/decrypt/hash) are useful for quick MD5/SHA1 lookups against precomputed databases.

---

## Task 7 — Hashing for Integrity Checking

Hash functions are used to verify that files have not been tampered with. Software projects publish SHA256 checksums alongside downloads — you compute the hash of what you downloaded and compare it against the published value.

```bash
# Verify a downloaded file
sha256sum libgcrypt-1.11.0.tar.bz2

# Compare against published hash
echo "09120c9867ce7f2081d6aaa1775386b98c2f2f246135761aae47d81f58685b9c  libgcrypt-1.11.0.tar.bz2" | sha256sum --check
```

**HMAC (Hash-based Message Authentication Code)** extends this further by combining a hash function with a secret key. It provides both:
- **Integrity** — data has not been altered
- **Authenticity** — data came from someone who holds the key

Used in TLS, API authentication, VPN tunnel verification (TryHackMe's own VPN uses HMAC-SHA512).

---

## Task 8 — Conclusion

Base64 is commonly confused with encryption but it is purely encoding — reversible with no key required. It is used to represent binary data as ASCII text (email attachments, JWT tokens, etc.).

```bash
# Decode base64
base64 -d ~/Hashing-Basics/Task-8/decode-this.txt

# Encode to base64
echo "ENcodeDEcode" | base64
```

---

## Flags / Answers

| Question | Answer |
|---|---|
| SHA256 hash of passport.jpg? | `77148c6f605a8df855f2b764bcc3be749d7db814f5f79134d2aa539a64b61f02` |
| Output size in bytes of MD5? | `16` |
| Possible values with 8-bit hash output? | `256` |
| 20th password in rockyou.txt? | `qwerty` |
| Hash `4c5923b6a6fac7b7355f53bfe2b8f8c1` from rainbow table? | `inS3CyourP4$$` |
| Crack hash `5b31f93c09ad1d065c0491b764d04933` online? | `tryhackme` |
| Should you encrypt passwords in auth systems? Yea/Nay | `Nay` |
| Hash size in yescrypt? | `256` |
| Hash-Mode for Cisco-ASA MD5? | `2410` |
| Hashing algorithm for Cisco-IOS `$9$`? | `scrypt` |
| Crack hash1.txt (bcrypt)? | `85208520` |
| Crack hash2.txt (SHA2-256)? | `halloween` |
| Crack hash3.txt (sha512crypt)? | `spaceman` |
| Crack hash4.txt (MD5)? | `funforyou` |
| SHA256 of libgcrypt-1.11.0.tar.bz2? | `09120c9867ce7f2081d6aaa1775386b98c2f2f246135761aae47d81f58685b9c` |
| hashcat mode for HMAC-SHA512 (key = $pass)? | `1750` |
| Decode `RU5jb2RlREVjb2RlCg==`? | `ENcodeDEcode` |

---

## Key Takeaways

- MD5 and SHA-1 are broken for security purposes — never use them for passwords or signatures
- Always salt passwords before hashing; salting defeats rainbow table attacks entirely
- Use purpose-built slow algorithms (bcrypt, scrypt, Argon2, yescrypt) for password storage — never fast hashes like MD5/SHA-256 raw
- `$2a$` = bcrypt, `$6$` = sha512crypt, `$9$` = scrypt (Cisco) — learn to recognise these on sight
- hashcat with rockyou.txt cracks weak passwords in seconds; strong unique passwords with proper salting are the only real defence
- SHA256 checksums on downloads are your first line of defence against supply chain tampering
