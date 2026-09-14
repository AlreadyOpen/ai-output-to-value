# Source code, open source, and AI: faster code does not create a new Linux

AI changes the economics of software development. It can reduce the time required to draft code, write tests and documentation, explore alternatives, refactor, triage issues, and perform parts of production and maintenance work.

That matters.

But a lower cost of producing code does **not** imply that mature software ecosystems become easy to recreate.

> **AI can accelerate development, production, and maintenance cycles. It does not instantly create a new Linux.**

The distinction is important for business leaders because software value is often discussed as if it were identical to the amount of source code written. It is not.

## Source code is an asset, but it is not the whole asset

Source code can embody substantial accumulated value:

- implementation decisions;
- compatibility behaviour;
- bug fixes learned from real use;
- performance work;
- security hardening;
- protocols and interfaces;
- test suites and regression knowledge;
- device and platform support;
- operational assumptions;
- domain knowledge encoded over time.

AI can make some of these things cheaper to produce or modify. It can also help people understand unfamiliar code more quickly.

But the value of a mature software project often extends far beyond the text in the repository.

A useful distinction is:

**Source tree → maintained project → adopted ecosystem → dependable infrastructure**

Each transition adds value that cannot be inferred merely from the ability to generate code.

## Linux is more than kernel source code

Linux is a useful example because it is both open source and foundational infrastructure.

Linux Foundation development reports describe a project built through contributions from thousands of developers and hundreds of companies, with a long-running review and release process. A 2017 report counted roughly 15,600 developers from more than 1,400 companies as kernel contributors since detailed Git tracking began.

The Linux kernel's own maintainer documentation makes clear that maintenance is an active responsibility involving patch review, bug reports, subsystem coordination, public development practices, and long-term stewardship. It explicitly treats trust and understanding as foundations of maintainership.

This means that reproducing a snapshot of source code would not reproduce:

- the maintainer network;
- the review process;
- the accumulated trust relationships;
- hardware-vendor participation;
- compatibility expectations;
- release discipline;
- downstream distributions;
- documentation and tooling;
- the installed base;
- the surrounding commercial ecosystem;
- the social process by which changes become accepted upstream.

An AI system might help generate a large amount of kernel-like code. That is very different from creating another Linux.

## AI changes the cost curve, not the definition of value

Suppose AI reduces the cost of writing a feature by 80%.

That is a real productivity gain if the resulting feature is useful and fit for purpose.

But it does not automatically reduce by 80% the cost of:

- deciding which feature should exist;
- preserving backwards compatibility;
- reviewing changes across subsystem boundaries;
- validating behaviour across hardware;
- handling security reports;
- operating release infrastructure;
- earning adoption;
- maintaining downstream compatibility;
- supporting users for years;
- coordinating organisations with different incentives.

In some settings AI may help with those tasks too. The point is not that they are permanently human or permanently expensive. The point is that they are **separate components of capability and value**.

## Open source demonstrates why price is not value

Open-source software is often available at a monetary price of zero. That does not make its economic value zero.

Harvard Business School researchers studying widely used open-source software estimated a supply-side replacement cost of about **US$4.15 billion** for the commonly used OSS in their dataset, while estimating a much larger **US$8.8 trillion demand-side value** by modelling what firms would face if they each had to recreate the OSS they rely on. These figures depend on the study's methodology and should not be read as a market valuation of open source, but they illustrate an important point: **availability at zero licence price can coexist with enormous replacement and dependency value**.

This is highly relevant to AI.

As code generation gets cheaper, the value of a project may increasingly concentrate in things such as:

- specification and problem selection;
- trusted tests and benchmarks;
- maintainer judgement;
- review and governance;
- compatibility and standards;
- security response;
- provenance;
- distribution;
- adoption and network effects;
- operating knowledge;
- reputation and trust;
- sustainable maintenance.

AI does not remove these forms of value simply because it can generate source code quickly.

## Open source is not passive free labour

The Linux Foundation's 2024 funding research estimated that organisations invest billions of dollars each year in open-source software, with labour representing most of that value.

Its 2026 research on return from open-source contribution also reported that organisations often incur significant costs when they maintain private forks and workarounds instead of participating upstream. The exact survey estimates should be treated within the study's methodology, but the underlying business lesson is useful:

> **Being able to copy source code is not the same as being able to maintain an economically sustainable substitute.**

A fork is cheap to create.

A replacement ecosystem is not.

AI may make a fork even cheaper to create. It may also make maintenance more efficient. But if the fork diverges from upstream, someone still has to reconcile changes, validate behaviour, respond to vulnerabilities, preserve interfaces, and support users.

## The value can move away from typing code

This does not mean source code stops mattering.

It means that as the cost of producing code falls, code-writing effort may become a smaller fraction of the total value of some software systems.

A useful analogy is manufacturing automation. If a machine dramatically reduces the labour required to fabricate a component, the product does not become valueless. Competitive advantage may move toward design, supply chains, quality control, distribution, integration, brand, service, and scale.

Software can behave similarly.

AI can make implementation cheaper while increasing the relative importance of:

**What should be built?**

**What must remain compatible?**

**How do we know it works?**

**Who maintains it?**

**Who adopts it?**

**Who trusts it?**

**What depends on it?**

## Open source can gain value from AI rather than lose it

There is another possibility: AI may increase the leverage of established open-source projects.

If developers and agents can understand, integrate, test, and extend mature open-source projects more easily, then existing projects with strong documentation, tests, APIs, governance, and communities may become **more useful building blocks**, not less.

At the same time, AI can reduce the barrier to creating alternatives. Both effects can happen together:

- easier experimentation and competition;
- faster contribution and maintenance;
- more forks;
- more rapid feature development;
- stronger reuse of trusted foundations;
- greater need to distinguish maintained projects from abandoned generated code.

The outcome will vary by project.

## A boss-facing test

When someone says:

> "AI can build this now, so the code is no longer valuable."

ask:

1. **Can it generate a codebase?**
2. **Can the organisation verify its behaviour?**
3. **Can it preserve compatibility over time?**
4. **Can it respond to vulnerabilities and failures?**
5. **Can it sustain releases and maintenance?**
6. **Can it attract or retain users, contributors, vendors, and integrations?**
7. **Can it replace the surrounding ecosystem, not just the repository?**

If the answer to the first question is yes and the others are unknown, then AI has demonstrated **generation capability**, not replacement value.

## The Linux test

The simple version for executives is:

> **If cheap code generation were enough to recreate software value, generating a new Linux would be mainly a coding problem. It is not.**

AI can help make Linux better. It can help maintainers, developers, vendors, and users move faster. It may dramatically change how patches, tests, documentation, migrations, and analysis are produced.

But Linux's value is also the accumulated result of decades of real-world use, coordination, compatibility, maintainership, institutional participation, and trust.

That distinction is exactly what **AI Output to Value** is trying to make visible.

## Sources

- Harvard Business School AI Institute — *Revealing Value: The Economic Power of Open Source Software*: https://aiinstitute.hbs.edu/revealing-value-the-economic-power-of-open-source-software/
- Linux Foundation — *Annual Kernel Development Report* summary: https://www.linuxfoundation.org/press/press-release/linux-foundation-releases-annual-kernel-development-report
- Linux kernel documentation — *Feature and driver maintainers*: https://www.kernel.org/doc/html/latest/maintainer/feature-and-driver-maintainers.html
- Linux Foundation Research — *2024 Open Source Software Funding Report*: https://www.linuxfoundation.org/research/open-source-funding-2024
- Linux Foundation — *ROI for Open Source Software Contribution* announcement, 2026: https://www.linuxfoundation.org/press/new-linux-foundation-report-shows-active-open-source-contribution-delivers-2-5x-roi-while-passive-consumption-increases-costly-technical-debt
