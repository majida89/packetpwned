---
title: "TryHackMe — DNS in Detail"
date: 2026-06-15
description: "Walkthrough of the Simple CTF room — enumeration, FTP, SSH privilege escalation."
tags: ["tryhackme", "ctf", "DNS", "privesc"]
---

## Overview

**Room:** DNS in Detail https://tryhackme.com/room/dnsindetail  
**Difficulty:** Easy  
**Platform:** TryHackMe  

---


TASK 1 — What is DNS?
─────────────────────
DNS (Domain Name System) is essentially the internet's phonebook. Every device
on the internet has a unique IP address (e.g. 104.26.10.229) which is how
traffic is actually routed. Since remembering raw IP addresses for every site
is impractical, DNS lets us use human-readable names like tryhackme.com instead
and handles the translation behind the scenes.

Q: What does DNS stand for?
A: Domain Name System


TASK 2 — Domain Hierarchy
──────────────────────────
Domain names follow a strict hierarchy, read right to left:

TLD (Top-Level Domain)
  The rightmost part of a domain. Two types exist:
  - gTLD (Generic): .com, .org, .edu, .gov — originally indicated purpose
  - ccTLD (Country Code): .co.uk, .ae, .ca — indicates geographic region
  Demand has created thousands of new gTLDs: .online, .club, .biz, etc.

Second-Level Domain
  The label directly left of the TLD (e.g. "tryhackme" in tryhackme.com).
  Max 63 characters. Allowed: a-z, 0-9, hyphens.
  Cannot start or end with a hyphen, no consecutive hyphens.

Subdomain
  Sits to the left of the second-level domain (e.g. "admin" in admin.tryhackme.com).
  Same character restrictions as the second-level domain (max 63 chars per label).
  Multiple subdomains can be chained: jupiter.servers.tryhackme.com
  Total domain name length must not exceed 253 characters.
  No limit on number of subdomains you can create.

Q: What is the maximum length of a subdomain?
A: 63

Q: Which of the following characters cannot be used in a subdomain (3 b _ -)?
A: _

Q: What is the maximum length of a domain name?
A: 253

Q: What type of TLD is .co.uk?
A: ccTLD


TASK 3 — Record Types
──────────────────────
DNS holds multiple record types, each serving a different purpose:

A Record     — Resolves to an IPv4 address (e.g. 104.26.10.229)
AAAA Record  — Resolves to an IPv6 address (e.g. 2606:4700:20::681a:be5)
CNAME Record — Resolves to another domain name (e.g. store.tryhackme.com →
               shops.shopify.com). Triggers a second DNS lookup on the target.
MX Record    — Points to the mail server handling email for the domain.
               Includes a priority value — lower number = higher priority.
               Allows fallback to backup servers if primary is down.
TXT Record   — Free-text field. Common uses:
               - SPF: authorised mail senders (anti-spam/spoofing)
               - DMARC: email policy enforcement
               - Domain ownership verification for third-party services
               - ACME challenge tokens for SSL certificate issuance

Note for recon: TXT and MX records often expose mail providers, third-party
integrations, and verification tokens. CNAME chains can reveal CDN/SaaS vendors.

Q: What type of record would be used to advise where to send email?
A: MX

Q: What type of record handles IPv6 addresses?
A: AAAA


TASK 4 — Making a DNS Request
──────────────────────────────
DNS resolution is a layered process involving multiple servers:

Step 1 — Local Cache
  Your OS checks its own DNS cache first. If a valid cached entry exists
  (TTL not expired), the IP is returned immediately with no network query.

Step 2 — Recursive DNS Server
  If not cached, the query goes to a Recursive DNS Server (usually your ISP's,
  or a public one like Cloudflare 1.1.1.1 or Google 8.8.8.8). It also caches
  results. Popular domains often resolve here without going further.

Step 3 — Root DNS Servers
  If no cached answer, the recursive server queries a root server. There are
  13 root server clusters (a–m.root-servers.net). They don't hold final answers
  — they redirect to the correct TLD server based on the domain extension.

Step 4 — TLD Server
  The TLD server (e.g. for .com) holds a registry mapping second-level domains
  to their authoritative nameservers. It returns the nameserver address for the
  queried domain.

Step 5 — Authoritative Nameserver
  The authoritative server holds the actual zone records and returns the final
  answer. For tryhackme.com this is kip.ns.cloudflare.com / uma.ns.cloudflare.com.
  Multiple nameservers provide redundancy. The answer is cached by the recursive
  server per the record's TTL, then relayed to the client.

TTL (Time To Live): Every DNS record includes a TTL in seconds. It controls
how long resolvers cache the record before re-querying. Short TTLs enable fast
failover; long TTLs reduce query load but slow propagation of changes.

Q: What field specifies how long a DNS record should be cached for?
A: TTL

Q: What type of DNS Server is usually provided by your ISP?
A: Recursive DNS Server

Q: What type of server holds all the records for a domain?
A: Authoritative DNS Server


TASK 5 — Practical
───────────────────
This task uses TryHackMe's in-browser DNS tool to query website.thm.
Real-world equivalents: nslookup or dig.

Examples:
  nslookup --type=CNAME shop.website.thm
  nslookup --type=TXT website.thm
  nslookup --type=MX website.thm
  nslookup www.website.thm

Q: What is the CNAME of shop.website.thm?
A: shops.myshopify.com

Q: What is the value of the TXT record of website.thm?
A: THM{7012BBA60997F35A9516C2E16D2944FF}

Q: What is the numerical priority value for the MX record?
A: 30

Q: What is the IP address for the A record of www.website.thm?
A: 10.10.10.10

