---
title: "5 Red Flags in Enterprise Firewall Audits"
date: 2026-07-13
draft: false
tags: ["firewall", "palo-alto", "panorama", "security-audit", "ngfw", "network-security"]
categories: ["network-security"]
description: "After years of reviewing enterprise firewall estates across the UAE, these are the red flags I find almost every single time. If your network has any of these, fix them before someone else finds them for you."
---

I've reviewed a lot of firewall policies over the years.

Multi-site enterprises, healthcare organisations, financial institutions, telecoms infrastructure. Different industries, different sizes, different vendors. But the problems I find? They're almost always the same ones.

That's not a coincidence. These issues aren't unique to one organisation or one team. They're the natural result of networks that grow faster than documentation, teams that change without handover, and policies that get added under pressure and never revisited.

This post is about the red flags I look for first when I'm reviewing an enterprise firewall estate. Not because they're the most sophisticated problems — they're not. But because they're the most common, and in many cases, the most dangerous.

---

## Before We Start — What "Audit" Actually Means Here

I'm not talking about a formal compliance audit with a checklist and a report that goes to the board. I'm talking about the technical review that happens when you take over a network, when you're onboarding a new client, or when something feels wrong and you need to understand why.

The kind of review where you pull the config, open it up, and start asking questions.

---

## Red Flag 1 — Rules With No Description, No Owner, No Expiry

This is the first thing I check. Every time.

Pull up a firewall policy. Look at the description field. If more than 30% of your rules have empty descriptions, you have a problem.

Here's why this matters more than it sounds. A firewall rule without a description is a rule without a reason. And a rule without a reason is a rule you can't safely touch. So it stays. Forever. Even when the service it was created for no longer exists. Even when the server it was pointing to was decommissioned two years ago. Even when the team that created it has completely turned over.

I've seen rules in production that were created in 2015 and never touched since. The person who created them left the organisation years ago. Nobody knows what they do. Nobody wants to disable them in case something breaks.

That's not a security policy. That's accumulated technical debt with a firewall in front of it.

**What good looks like:**
Every rule should have at minimum:
- A description explaining what it does and why it exists
- A ticket reference or change request number
- The date it was created
- The owner or team responsible for it

If you're on Palo Alto with Panorama, use tags to track rule owners and review dates. It takes five minutes to set up and saves hours of confusion later.

---

## Red Flag 2 — VPN Tunnels Nobody Remembers

This one always gets a reaction when I mention it to clients.

"We have a tunnel to a vendor. We don't know which vendor. We don't know what it's for. But we're afraid to take it down."

I've heard variations of that sentence more times than I can count.

VPN tunnels accumulate over time. A vendor needs access for a deployment. An integration gets built between two systems. A project creates a site-to-site connection for testing that was supposed to be temporary. The project ends. The tunnel stays.

The security implication here is real. An active VPN tunnel is a trusted path into your network. If you don't know what's on the other end of it, you don't know what has access to your infrastructure. That's not a theoretical risk — that's an actual unknown exposure sitting in your routing table.

**What I do when I find these:**

First, check if the tunnel is actually up. A lot of "mystery tunnels" have been down for months and nobody noticed because nothing was using them. If it's down, document it, then disable and eventually remove it.

If it's up, check the traffic. What source and destination IPs are using it? What applications? That usually gives you enough context to track down the original purpose. Then you can make an informed decision about whether it should stay or go.

And if you genuinely cannot determine what a tunnel is for after investigating — that's a conversation you need to have with your security team before you make any decisions either way.

---

## Red Flag 3 — The Mystery Critical Server

This one is more specific but I've found it often enough to include it.

You're reviewing the security policy and you notice one particular IP address — or a small group of IPs — appearing in rules across almost every branch or zone. Dedicated rules. Usually broad access. And when you look at the documentation, there's nothing. No entry in the CMDB. No mention in the network diagram. No ticket that explains what it is.

But clearly, something depends on it. Because those rules didn't create themselves.

The instinct is to leave it alone. And I understand that instinct — if something is clearly being used and you don't know what it is, touching it feels risky. But leaving an undocumented server with broad firewall access sitting in your environment is also a risk. You don't know what's running on it. You don't know who has access to it. You don't know if it's patched.

**How to investigate:**

Start with traffic logs. What's actually communicating with this IP? What applications, what users, what frequency? That usually tells you what the server does even if you don't know what it is.

Then work backwards from there. If it's receiving database traffic from branch offices, it's probably a centralised database. If it's receiving syslog traffic, it's probably a log aggregation server. Once you know what it does, finding who owns it becomes much easier.

Document everything you find. Even if you can't fully identify the server, a documented unknown is better than an undocumented unknown.

---

## Red Flag 4 — Overlapping Rules Creating Hidden Allow Paths

This is the most technically interesting one and in some ways the most dangerous.

In a large security policy — hundreds or thousands of rules — it's very easy for overlapping rules to create access paths that weren't intended. A broad rule created early in the policy allows traffic that a more specific rule further down was supposed to block. Or two rules that were created independently by different teams end up combining to allow traffic that neither team individually intended to permit.

The reason this is particularly dangerous is that it's invisible from a normal review. The rules individually look fine. The intent of each rule is understandable. But the *combination* of rules creates an exposure that nobody designed.

On Palo Alto, the Security Policy Optimizer and the Rule Usage feature in Panorama are your friends here. Rule Usage shows you which rules are actually matching traffic — rules with zero hits in 90 days are either redundant or covering traffic that no longer exists. The Policy Optimizer will flag rules that can be tightened based on actual traffic patterns.

But tools only get you so far. There's no substitute for actually reading through your policy from top to bottom, understanding the logic, and asking "what traffic does this combination of rules actually permit?" That's a time-consuming exercise on a large policy. It's also one of the most valuable things you can do.

**The quick check:**

Look for any-to-any rules. Any rule where source, destination, application, or service is set to "any" is a candidate for review. Not necessarily wrong — sometimes broad rules are legitimate. But every one of them should be challenged: is this as broad as it needs to be, or has it just never been tightened?

---

## Red Flag 5 — No Change Management Trail

This is less about the technical config and more about the process around it.

When I'm reviewing a firewall estate and I ask "why does this rule exist?" — I should be able to find the answer. There should be a change request. A ticket. An email thread. Something that explains the business reason this rule was created, who approved it, and when.

If the answer is "we don't know" or "we'd have to ask the person who used to manage this" — that's a process failure. Not a personal one, and not necessarily anyone's fault. But it's a failure that creates ongoing risk because it means future changes are being made in a context vacuum.

Good change management isn't bureaucracy for its own sake. It's the paper trail that lets you understand your own environment. Without it, every review becomes an archaeology project instead of an audit.

---

## The Common Thread

If you look at all five of these, there's one thing they all have in common.

They're all the result of something being done in the moment — a rule added under pressure, a tunnel created for a project, a server deployed without documentation — and then never revisited.

Firewall policies aren't set-and-forget. They're living documents that need regular review, cleanup, and maintenance. The organisations I've seen with the cleanest security postures aren't necessarily the ones with the most sophisticated tools. They're the ones with the most consistent processes.

Review your policy regularly. Document everything. Own your rules.

Because if you don't know what's in your firewall policy, you can be sure someone eventually will.

---

## A Practical Starting Point

If you're reading this and thinking about where to start with your own estate, here's a simple first step:

Export your security policy to a spreadsheet. Sort by last hit date. Look at everything that hasn't matched traffic in 90 days. That list is your starting point for cleanup.

You won't fix everything at once. You don't need to. Start with the obvious stuff — disabled rules, rules pointing to decommissioned IPs, rules with no description and no hits. Clean those up first. Then work your way through the rest.

Incremental improvement is still improvement. And a cleaner policy is a more secure policy.

---

*Majid Ahmed — CCIE #55880 | CISSP | PCNSE | Senior Network & Security Engineer*  
*Connect on [LinkedIn](https://www.linkedin.com/in/majid-information-security/)*
