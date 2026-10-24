# Nikola Kubera

**Property data, maps and AI tools — built on open UK government data.**
London · open to remote work in data, GIS and applied AI

[![Live demo](https://img.shields.io/badge/Live_demo-kubera--geoai.pages.dev-0E75B6?style=for-the-badge)](https://kubera-geoai.pages.dev)
[![Email](https://img.shields.io/badge/Email-jobkubera%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:jobkubera@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-kuberababa-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/kuberababa)

---

## ▶ KUBERA GEO SI — property facts for UK estate agents

**Live:** [kubera-geoai.pages.dev](https://kubera-geoai.pages.dev) · **Showcase:** [jobkubera-lab/kubera-geoai](https://github.com/jobkubera-lab/kubera-geoai) · **Pilot area:** Mitcham (CR4), London Borough of Merton

[![KUBERA GEO SI map](https://raw.githubusercontent.com/jobkubera-lab/kubera-geoai/main/docs/screenshots/01-map.jpg)](https://kubera-geoai.pages.dev)

A map-based tool that prepares, for every home, the facts an estate agent has to give a buyer — with the source next to every figure and nothing guessed.

| What it does | How |
|---|---|
| Exact location and energy certificate | OS Open UPRN address points; EPC matched by UPRN |
| Material Information pack (Parts A / B / C) | each line marked *from data*, *partly from data* or *ask the seller* |
| Risks | Environment Agency flood zones, conservation areas, listed buildings, police.uk crime, Defra road and rail noise |
| Costs | Stamp Duty, mortgage, running costs, agency fee, lettings, buy-to-let lender test |
| **Legal documents check** | agent adds PDFs → read in the browser → what is confirmed (with page), missing, conflicting or out of date, plus questions for the conveyancer |
| **AI assistant** | answers property questions using tools over official data; personal details masked before any AI call |
| Agency's own listings | CSV upload; export as PDTF v3 JSON (open industry schema) |

**Engineering:** TypeScript · React · Leaflet and WMS map layers · Cloudflare Pages and Workers AI · pdf.js · 106 automated tests · weekly data refresh with GitHub Actions · English / Russian interface

**Principles:** official open data first · source and date on every figure · unknown means "not in our data", never "no risk" · no valuations or buy/sell advice

---

## Other work

| Project | What it is | Evidence |
|---|---|---|
| [KUBERA AGENT OS](kubera-lab/agent-os/) | Python runtime for controlled AI agents: evidence ledger, approval gates, replay protection | 173 tests, 89% branch coverage (2 Oct 2026) |
| [KUBERA TAO LAB](kubera-lab/kubera-tao-lab/) | Evaluation discipline for property-price models: temporal splits, leakage control | 34 tests, CI passing; code private |
| [KUBERA Real Estate OS](kubera-lab/real-estate-os/) | Early architecture for agency workflows and CRM automation | 3/3 core tests; bootstrap phase |
| [Tender Intelligence](kubera-lab/tender-intelligence/) | UK public-procurement qualification with provenance | 16 tests |
| [Civic service finder](research/council-ai-service-finder/) | Plain-language council service discovery with an evaluation harness | research prototype |
| [Kubera Guide](https://www.google.com/maps/contrib/111907570264362429428) | Google Maps contributions: field mapping and place data | public profile |

More: [Portfolio review](PORTFOLIO_REVIEW.md) · [Status](STATUS.md) · [Repository map](REPO_MAP.md) · [Full background](EXTENDED_README.md)

---

## Skills

`TypeScript` `React` `Python` `GIS · WMS · GeoJSON` `UK open data — HM Land Registry, EPC, OS, Environment Agency, ONS, Planning Data` `Cloudflare` `GitHub Actions` `AI agents and tool use` `PDF and document processing` `automated testing`
