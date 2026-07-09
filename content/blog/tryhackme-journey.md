---
title: "From Network Engineer to Pentester — Why I Started TryHackMe"
date: 2025-07-11
draft: false
tags: ["tryhackme", "pentesting", "networking", "career", "cybersecurity"]
categories: ["journey"]
description: "I have a CCIE and a CISSP. I've been building and securing networks for over 10 years. So why did I go back to basics and start TryHackMe's Junior Pentester path? Here's the honest answer."
---

I want to be upfront about something before we get into this.

I'm not a beginner. I hold CCIE #55880 and CISSP certifications. I spent 8 years at du (EITC) — one of the UAE's largest telecoms operators — starting from service activation, moving through the NOC, and eventually working on core network infrastructure. I now work as a Senior Network & Security Engineer at Alpha Data, designing and deploying enterprise security solutions across the UAE.

So why am I doing TryHackMe's Junior Pentester path?

That's exactly what I want to talk about.

---

## The Honest Reason

There's a question that started bothering me about two years ago.

I was reviewing a firewall policy for a client — hundreds of rules, multiple zones, NAT policies stacked on top of each other. I knew exactly what each rule was supposed to do. I understood the design intent. I could tell you which traffic was allowed and which was blocked.

But I couldn't tell you, with confidence, *how an attacker would move through it.*

That gap bothered me. A lot.

I know how to build walls. I've spent my entire career building walls — firewalls, VPN tunnels, access policies, segmentation. But knowing how to build a wall and knowing how someone would climb over it, dig under it, or find the door you forgot to lock — those are very different skills.

That's what pushed me toward TryHackMe.

---

## Why Not Just Read a Book?

Fair question. I've read plenty of books. I hold CEH. I understand the theory of offensive security.

But theory and practice are two completely different things.

The first time I tried to exploit a vulnerability in a controlled lab environment, I failed. Multiple times. Not because I didn't understand what I was supposed to do — I did. But understanding a concept and actually executing it under pressure, troubleshooting when it doesn't work, adapting when the environment behaves differently than expected — that's a skill you can only build by doing.

TryHackMe forces you to do. There's no way around it.

---

## Why TryHackMe Specifically

I looked at a few options. HackTheBox, OSCP, INE's PTS path.

I chose TryHackMe's Junior Pentester path for one specific reason — it's structured.

I don't have unlimited time. I'm managing enterprise deployments during the day, dealing with Panorama drift issues and firewall migrations and client escalations. I needed something I could pick up for 45 minutes in the evening and make actual progress on, rather than spending half my time figuring out where to start.

TryHackMe's learning paths are guided. Each room builds on the previous one. The progression makes sense. And critically — the hints are there when you're genuinely stuck, which means you spend your time learning rather than hitting your head against a wall for three hours on a misconfigured wordlist.

That said — I do try to solve each room on my own before I look at hints. The struggle is where the learning is.

---

## What I've Learned So Far

I'm currently at a Top 6% ranking with a 48-day streak and 56 rooms completed. Here's what's actually surprised me:

**1. I knew more than I thought — and less than I thought.**

My networking background gave me a massive advantage in understanding how attacks work at the protocol level. TCP handshakes, ARP spoofing, DNS poisoning — these concepts clicked instantly because I already understood the underlying protocols deeply.

But my actual exploitation skills? Those needed work. Knowing *why* a buffer overflow works is very different from actually writing shellcode that lands.

**2. The attacker's mindset is genuinely different.**

When you're a network engineer, you think in terms of availability and connectivity. Is traffic flowing? Are routes converging? Is the service reachable?

When you're thinking like an attacker, you think in terms of what's *possible*, not what's *intended*. You look at the same network and ask completely different questions. That mindset shift doesn't happen automatically — you have to train it.

**3. Enumeration is everything.**

I cannot stress this enough. The rooms where I struggled most were almost always rooms where I rushed the enumeration phase. Every time I slowed down and did thorough reconnaissance, the rest of the room became significantly easier. This has actually changed how I think about security assessments in my day job — I now ask more questions about what's actually running on a network before I start looking at the firewall policy.

**4. The small wins matter.**

There's something genuinely satisfying about capturing a flag. It's silly, maybe, for someone who's been in this industry as long as I have — but getting that "Correct!" notification after working through a problem for 45 minutes is motivating in a way that reading about pentesting never was.

---

## What I'm Still Struggling With

I'll be honest here too, because I think the glossy "here's everything I've learned" posts aren't that useful.

**Scripting.** My Python is functional but not elegant. When I see other people's solutions after I've solved a room, sometimes I see a 10-line Python script that does something I did manually in 45 minutes. That gap is real and I'm working on closing it.

**Privilege escalation.** Linux privesc in particular. I understand the concepts — SUID binaries, writable cron jobs, kernel exploits. But finding them quickly and systematically in a real environment is a skill I'm still developing.

**Patience.** This is probably the biggest one. I'm used to having a clear objective and a clear path to it. Pentesting is more ambiguous — sometimes you're stuck and there's no obvious next step. Sitting with that uncertainty and working through it methodically rather than reaching for hints too quickly is something I actively have to remind myself to do.

---

## How This Is Changing My Day Job

I wasn't expecting this, but the TryHackMe journey is already making me better at my actual job.

The questions I ask during security assessments have changed. I'm more likely to ask about lateral movement paths, not just perimeter security. I think more about what an attacker could do *after* they're inside the network, not just about keeping them out.

I also approach Panorama rule reviews differently now. When I'm looking at a security policy, I'm not just asking "does this rule make sense?" — I'm asking "how could someone abuse this?" That's a fundamentally different question and it leads to finding issues that I would have missed before.

---

## Is This a Career Pivot?

No. I'm not planning to become a penetration tester.

I'm a network security engineer. That's what I'm good at, that's where I add value, and that's where I want to continue building my career.

But I do believe that the best network security engineers understand how attacks work from the inside. You can't build a wall without knowing how people try to get through it. The two disciplines are more connected than most job descriptions suggest.

TryHackMe is making me a better defender by teaching me how to attack.

That's the whole point.

---

## If You're Thinking About Starting

A few thoughts if you're a network engineer considering the same path:

**Your background is an advantage, not a disadvantage.** Don't let the "junior" in Junior Pentester put you off. Your understanding of protocols and network architecture will make you better at this than someone coming from a pure software background. You'll struggle with different things, but your foundation is solid.

**Do it consistently rather than intensively.** 45 minutes every day beats 6 hours on a weekend and then nothing for two weeks. The streak isn't just a vanity metric — it builds the habit.

**Embrace being bad at it.** This is the hardest part for experienced engineers. We're used to knowing what we're doing. Being a beginner again is uncomfortable. That discomfort is the learning.

**Don't skip the writeups.** After you complete a room, read other people's writeups. There's almost always a faster or more elegant approach than what you did. That's where a lot of the real learning happens.

---

## Where I'm Documenting This

I'm writing up room solutions and lessons learned on this site — packetpwned.com. Not full walkthroughs that spoil the rooms, but the concepts, the techniques, and the thinking behind them.

If you're on a similar journey — CCIE, CCNP, senior network engineer who wants to understand the offensive side — feel free to connect on LinkedIn.

The walls aren't going to secure themselves.

---

*Majid Ahmed — CCIE #55880 | CISSP | PCNSE | Senior Network & Security Engineer*  
*Connect on [LinkedIn](https://www.linkedin.com/in/majid-information-security/)*
