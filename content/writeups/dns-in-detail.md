---
title: "TryHackMe: DNS in Detail"
date: 2026-06-16
description: "Walkthrough of the DNS in Detail room — domain hierarchy, record types, and DNS resolution flow."
tags: ["tryhackme", "dns", "networking", "pre-security"]
---

## Overview

**Room:** DNS in Detail  
**Difficulty:** Easy  
**Platform:** TryHackMe  

---

## What is DNS?

DNS (Domain Name System) is the internet's phonebook. Every device on the internet is identified by an IP address (e.g. `104.26.10.229`). Since memorising raw numbers for every site is impractical, DNS maps human-readable names like `tryhackme.com` to the correct IP behind the scenes.

---

## Domain Hierarchy

Domains follow a right-to-left hierarchy:

- **TLD (Top-Level Domain)** — the rightmost label. Two types:
  - **gTLD** (Generic): `.com`, `.org`, `.edu`, `.gov`
  - **ccTLD** (Country Code): `.co.uk`, `.ae`, `.ca`
- **Second-Level Domain** — sits left of the TLD (e.g. `tryhackme` in `tryhackme.com`). Max 63 characters, `a-z 0-9` and hyphens only.
- **Subdomain** — prepended to the left (e.g. `admin.tryhackme.com`). Same character rules. Total domain length must not exceed **253 characters**.

---

## DNS Record Types

| Record | Resolves To | Notes |
|---|---|---|
| A | IPv4 address | e.g. `104.26.10.229` |
| AAAA | IPv6 address | e.g. `2606:4700:20::681a:be5` |
| CNAME | Another domain name | Triggers a second DNS lookup on the target |
| MX | Mail server hostname | Includes a priority value — lower = higher priority |
| TXT | Arbitrary text | Used for SPF, DMARC, domain ownership verification |

---

## DNS Resolution Flow

When you request a domain, the query travels through several layers:

1. **Local Cache** — OS checks its own cache first; if TTL is valid, returns immediately
2. **Recursive DNS Server** — usually your ISP's (or public like `1.1.1.1` / `8.8.8.8`); also caches results
3. **Root DNS Servers** — 13 clusters worldwide; redirect to the correct TLD server
4. **TLD Server** — holds the registry of authoritative nameservers per domain
5. **Authoritative Nameserver** — holds the actual zone records and returns the final answer

Every record includes a **TTL (Time To Live)** in seconds, controlling how long resolvers cache the response before re-querying.

---

## Practical — DNS Queries

The task uses TryHackMe's in-browser DNS tool against `website.thm`. Real-world equivalent:

```bash
nslookup --type=CNAME shop.website.thm
nslookup --type=TXT website.thm
nslookup --type=MX website.thm
nslookup www.website.thm
```

Or with `dig`:

```bash
dig CNAME shop.website.thm
dig TXT website.thm
dig MX website.thm
dig A www.website.thm
```

---

## Flags / Answers

| Question | Answer |
|---|---|
| What does DNS stand for? | `Domain Name System` |
| Maximum length of a subdomain? | `63` |
| Character that cannot be used in a subdomain (3 b _ -)? | `_` |
| Maximum length of a domain name? | `253` |
| What type of TLD is .co.uk? | `ccTLD` |
| Record type used to advise where to send email? | `MX` |
| Record type that handles IPv6 addresses? | `AAAA` |
| Field that specifies how long a DNS record is cached? | `TTL` |
| Type of DNS server usually provided by your ISP? | `Recursive DNS Server` |
| Type of server that holds all records for a domain? | `Authoritative DNS Server` |
| CNAME of shop.website.thm? | `shops.myshopify.com` |
| TXT record value of website.thm? | `THM{7012BBA60997F35A9516C2E16D2944FF}` |
| Numerical priority value for the MX record? | `30` |
| IP address for the A record of www.website.thm? | `10.10.10.10` |

---

## Key Takeaways

- DNS is hierarchical — understanding the chain (root → TLD → authoritative) is fundamental to both networking and recon
- TXT and MX records during enumeration can expose mail providers, SPF configs, and third-party integrations
- CNAME chains often reveal CDN or SaaS vendors in use — useful passive intel
- `nslookup` and `dig` are your go-to tools; know both
