#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programmatic SEO + GEO + OpenGraph PNG builder for TuringTec Agent Studio.
Generates 6 vertical solution landing pages (/solutions/<slug>/index.html),
7 branded 1200x630 OG PNGs, robots.txt, sitemap.xml, llms.txt, llms-full.txt,
IndexNow key file, and README.md.
"""

from __future__ import annotations

import datetime
import html
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://gabhack.github.io/turingtec-agent-studio"
GUMROAD_STORE = "https://gabbler407.gumroad.com/"
TODAY = datetime.date.today().isoformat()
INDEXNOW_KEY = "c8e4a91f7b2d406ea35c89f14d2b7019"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

SOLUTIONS = [
    {
        "slug": "clinic-whatsapp-voice-agent",
        "badge": "HEALTHCARE & CLINICS · 24/7 WHATSAPP + VOICE",
        "title": "24/7 AI WhatsApp & Voice Receptionist Agent for Clinics (Anti-No-Show + Calendar Sync)",
        "short_title": "Clinic WhatsApp & Voice Receptionist Agent",
        "meta_desc": "Deploy a self-hosted 24/7 WhatsApp & Voice AI receptionist for medical and dental clinics. Automates triage, Google Calendar booking & 24h/2h anti-no-show reminders with BYOK pricing.",
        "price_kit": "$39 n8n Workflow / $99 Business-in-a-Box",
        "price_pilot": "$690 7-Day Turnkey Pilot",
        "accent": (16, 185, 129),
        "intro": "Stop losing after-hours patients and manual front-desk hours. TuringTec's self-hosted ClinicFlow AI connects WhatsApp Cloud API, Google Calendar / EMR webhooks, and automated 24h/2h confirmation reminders on a BYOK architecture ($0 SaaS markup).",
        "rows": [
            ("Channels", "WhatsApp Cloud API + Optional ElevenLabs/Vapi Voice"),
            ("Calendar & Intake", "Real-time slot check, booking, rescheduling & insurance card intake"),
            ("No-Show Reduction", "Automated 24-hour and 2-hour WhatsApp confirmations + waitlist refill"),
            ("Hosting & Data Control", "100% BYOK (your Meta Business, your LLM key, zero vendor lock-in)"),
            ("Deployment Options", "$39 Self-Host n8n JSON Pack · $99 Business-in-a-Box · $690 7-Day Pilot"),
        ],
        "faqs": [
            ("Does ClinicFlow AI require paying per-seat SaaS fees?", "No. It runs on your own self-hosted Docker n8n instance and Meta WhatsApp Cloud API (roughly $0.003-$0.005 per conversation window)."),
            ("Can a human receptionist take over complex patient conversations?", "Yes. The workflow supports instant human hand-off rules via Chatwoot or direct escalation alerts whenever clinical edge cases arise."),
        ],
    },
    {
        "slug": "hardware-b2b-quoting-agent",
        "badge": "B2B HARDWARE & WHOLESALE · AUTOMATED RFQ QUOTING",
        "title": "FerreQuote AI: B2B Hardware & Industrial Wholesale RFQ Quoting Agent (WhatsApp/Email to SKU)",
        "short_title": "B2B Hardware & Wholesale RFQ Quoting Agent",
        "meta_desc": "Convert messy WhatsApp and email material lists into accurate SKU quotes with tiered volume discounts and margin protection in seconds. Self-hosted n8n + Python agent.",
        "price_kit": "$39 n8n Workflow / $99 Business-in-a-Box",
        "price_pilot": "$690 7-Day Turnkey Pilot",
        "accent": (28, 105, 212),
        "intro": "Wholesale distributors lose deals when manual quoting takes hours. FerreQuote AI parses unstructured WhatsApp texts, Excel sheets, or emails against your real SKU price catalog, applies volume tier margins, and outputs ready-to-send CSV/PDF quotes in seconds.",
        "rows": [
            ("Input Formats", "Unstructured WhatsApp texts, emails, CSV/Excel material lists"),
            ("Matching Engine", "Fuzzy SKU matching + unit normalization + volume discount rules"),
            ("Margin Protection", "Automated floor-margin checks before sending quotes"),
            ("ERP / Sheet Sync", "Outputs clean JSON/CSV ready for Siigo, Alegra, SAP, NetSuite, or Sheets"),
            ("Deployment Options", "$39 n8n Pack · $99 Business-in-a-Box · $690 7-Day Turnkey Pilot"),
        ],
        "faqs": [
            ("How does FerreQuote handle messy abbreviations or typos in WhatsApp messages?", "It combines normalized synonym maps with low-cost LLM extraction (BYOK) and confidence thresholds so ambiguous lines are flagged for 1-click sales review."),
            ("Can I test it with a real material list right now?", "Yes—open our zero-signup browser sandbox on the TuringTec Agent Studio home page and paste any Spanish or English hardware list."),
        ],
    },
    {
        "slug": "invoice-pdf-extraction-agent",
        "badge": "BACK-OFFICE FINANCE · IDP DOCUMENT AGENT",
        "title": "DocFlow B2B: Automated Invoice & Purchase Order PDF-to-ERP Extraction Agent",
        "short_title": "Invoice & PO PDF-to-ERP Extraction Agent",
        "meta_desc": "Extract vendor details, NIT/Tax IDs, line items, IVA/taxes and math-validated totals from B2B PDF invoices and purchase orders into JSON, Excel, or ERP webhooks.",
        "price_kit": "$39 n8n Workflow / $99 Business-in-a-Box",
        "price_pilot": "$690 7-Day Turnkey Pilot",
        "accent": (79, 70, 229),
        "intro": "Eliminate manual invoice typing and accounting errors. DocFlow B2B extracts line-by-line structured JSON from vendor invoices and purchase orders, runs deterministic math/tax checks with confidence scoring, and routes verified entries straight to Sheets or your ERP.",
        "rows": [
            ("Extracted Fields", "Vendor Name, Tax ID/NIT, Invoice #, Date, Line Items, Tax, Total"),
            ("Validation Gate", "Deterministic subtotal + tax arithmetic check + confidence score"),
            ("Exception Routing", "Low-confidence or mismatched totals route automatically to human review"),
            ("Outputs", "Strict JSON Schema, CSV/Excel, or Webhook POST to ERP / Accounting"),
            ("Deployment Options", "$39 n8n Pack · $99 Business-in-a-Box · $690 7-Day Turnkey Pilot"),
        ],
        "faqs": [
            ("Does DocFlow charge per document forever?", "With our $39 n8n Pack or $99 Business-in-a-Box, you self-host the agent and pay only your raw LLM token cost (~$0.001-$0.003 per invoice)."),
            ("Can it catch supplier math discrepancies automatically?", "Yes—deterministic post-extraction checks verify line totals and IVA/VAT sums before pushing to accounting."),
        ],
    },
    {
        "slug": "aws-finops-guardrails-mcp",
        "badge": "CLOUD ARCHITECT · OPEN-CORE CLI + MCP SERVER",
        "title": "AWS FinOps & LLM Token Guardrails: Open-Core CLI + stdio MCP Server with Terraform Auto-Fix",
        "short_title": "AWS FinOps & LLM Token Guardrails MCP",
        "meta_desc": "Audit AWS EBS, NAT Gateways, EIPs, idle RDS and Bedrock/OpenAI/Gemini token waste locally via CLI or Claude/Cursor MCP Server. Unlock Terraform HCL auto-remediation & SARIF.",
        "price_kit": "$0 Open-Core / $49 Pro License Key",
        "price_pilot": "$299 48-Hour FinOps Audit",
        "accent": (245, 158, 11),
        "intro": "Cut 25–60% of cloud and AI agent waste without sharing AWS IAM credentials with third-party SaaS dashboards. Run aws-finops-guard locally in your terminal or inside Claude Desktop/Cursor via MCP stdio, then unlock safe Terraform HCL patches & CI/CD SARIF gates.",
        "rows": [
            ("AWS Rules Included", "Unattached EBS, gp2->gp3, idle NAT Gateways, $0 S3 Gateway Endpoints, EIPs, RDS"),
            ("AI / LLM FinOps Rules", "Detects premium models used for classification/triage + missing prompt caching"),
            ("MCP Integration", "Zero-dependency JSON-RPC 2.0 stdio server for Claude Desktop, Cursor & VS Code"),
            ("Pro Unlock ($49)", "Safe Terraform HCL patches, AWS CLI commands & CI/CD SARIF 2.1.0 reports"),
            ("Source Repository", "Open-Core MIT on GitHub (github.com/gabhack/aws-finops-guard)"),
        ],
        "faqs": [
            ("Does aws-finops-guard require sending my AWS credentials to an external server?", "Never. All audits run 100% locally against your JSON cost/resource snapshots with zero external network calls (except one-time Gumroad Pro license verification)."),
            ("How quickly does the $49 Pro license pay for itself?", "Fixing a single idle NAT Gateway ($32.85/mo) or switching one triage agent from a premium model to a fast model pays back the $49 license in days."),
        ],
    },
    {
        "slug": "n8n-ai-agent-workflows-pack",
        "badge": "15 IMPORTABLE JSON WORKFLOWS + DOCKER SELF-HOST",
        "title": "15 Production n8n AI Agent Workflows Pack (Clinics, B2B RFQ, Invoices, FinOps & MCP Bridge)",
        "short_title": "15 Production n8n AI Agent Workflows Pack",
        "meta_desc": "Skip broken 4,000-workflow dumps. Download 15 clean, tested, BYOK n8n AI Agent JSON workflows + 1-command Docker Compose self-host stack for $39 one-time.",
        "price_kit": "$39 Standard / $79 Agency License",
        "price_pilot": "$99 All-Access Business-in-a-Box",
        "accent": (14, 165, 233),
        "intro": "Stop debugging broken templates. This curated pack gives you 15 clean, environment-variable-driven n8n AI Agent workflows spanning customer support, B2B sales quoting, PDF extraction, Gumroad onboarding, AWS FinOps alerts, and an MCP HTTP bridge—plus a 1-command Docker Compose file.",
        "rows": [
            ("Workflow Count", "15 complete importable JSON graphs (indexed in catalog/index.json)"),
            ("Self-Host Stack", "Includes docker-compose.yml + .env.example ($0/mo local or VPS)"),
            ("LLM Flexibility", "Works with OpenAI, OpenRouter, Gemini OpenAI-compatible API, or Ollama"),
            ("Security Hygiene", "Zero hardcoded keys; clean env var references throughout"),
            ("License", "$39 Personal/Internal · $79 Agency Unlimited Client Deployments"),
        ],
        "faqs": [
            ("Do I need a paid n8n Cloud subscription to run these?", "No. The included docker-compose.yml launches n8n self-hosted in under 60 seconds at $0 software cost."),
            ("What makes this pack different from huge 4,000-file n8n dumps?", "Every workflow follows a uniform, clean, modern n8n v1 schema with BYOK headers and practical B2B use cases rather than outdated deprecated nodes."),
        ],
    },
    {
        "slug": "mcp-agent-business-in-a-box",
        "badge": "FLAGSHIP ALL-ACCESS VAULT · $99 ONE-TIME",
        "title": "TuringTec AI Agent Business-in-a-Box: 15 n8n Workflows + 4 MCP Servers + 12 Agent Skills",
        "short_title": "AI Agent Business-in-a-Box (All-Access Vault)",
        "meta_desc": "Launch or white-label B2B AI agents immediately: 15 n8n workflows, 4 production MCP servers (Apify Standby PPE + AWS FinOps), 12 Claude/Cursor/Codex Agent Skills & commercial rights.",
        "price_kit": "$99 All-Access (Save 60%)",
        "price_pilot": "Includes Commercial White-Label Rights",
        "accent": (99, 102, 241),
        "intro": "Our complete engineering vault for solo developers, AI consultants, and agencies building recurring B2B AI agent offers. Combines all 15 n8n workflows, 4 production MCP servers, 12 cross-platform SKILL.md modules, and full commercial client deployment rights in one $99 ZIP.",
        "rows": [
            ("Module 1", "15 Production n8n AI Agent Workflows + Docker Compose Self-Host"),
            ("Module 2", "aws-finops-guard CLI + stdio MCP Server + Terraform Auto-Fix source"),
            ("Module 3", "3 Apify Dual-Mode Standby + Pay-Per-Event v2 MCP Servers"),
            ("Module 4", "12 Cross-Platform SKILL.md modules (Claude Code, Cursor, Codex, Antigravity)"),
            ("Commercial Rights", "Deploy & white-label for unlimited paying clients (no raw ZIP resale)"),
        ],
        "faqs": [
            ("Is this a recurring subscription?", "No. Pay $99 USD once via Gumroad and receive instant ZIP delivery with full source code and commercial deployment rights."),
            ("Can I use these assets to sell $500-$1,500 B2B setups to local businesses?", "Yes—that is the exact purpose of the Business-in-a-Box commercial license."),
        ],
    },
]


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def make_og(out_path: Path, badge: str, title: str, subtitle: str, accent: tuple[int, int, int]) -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (10, 16, 30))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(9 + 11 * t), int(15 + 16 * t), int(28 + 24 * t)))
    draw.rectangle([0, 0, 14, H], fill=accent)
    draw.rectangle([0, 0, W, 6], fill=accent)
    f_b = ImageFont.truetype(FONT_BOLD, 26) if Path(FONT_BOLD).exists() else ImageFont.load_default()
    f_bg = ImageFont.truetype(FONT_BOLD, 20) if Path(FONT_BOLD).exists() else ImageFont.load_default()
    f_t = ImageFont.truetype(FONT_BOLD, 48) if Path(FONT_BOLD).exists() else ImageFont.load_default()
    f_s = ImageFont.truetype(FONT_REG, 24) if Path(FONT_REG).exists() else ImageFont.load_default()

    draw.rounded_rectangle([68, 52, 126, 110], radius=12, fill=accent)
    draw.text((80, 66), "TT", font=f_b, fill=(255, 255, 255))
    draw.text((144, 65), "TuringTec Agent Studio", font=f_b, fill=(241, 245, 249))

    btxt = badge.upper()[:46]
    bb = draw.textbbox((0, 0), btxt, font=f_bg)
    bw = (bb[2] - bb[0]) + 32
    bx = max(460, W - 68 - bw)
    draw.rounded_rectangle([bx, 58, bx + bw, 102], radius=22, fill=(24, 34, 54), outline=accent, width=2)
    draw.text((bx + 16, 68), btxt, font=f_bg, fill=(191, 219, 254))

    y_cur = 165
    for line in textwrap.wrap(title, width=38)[:3]:
        draw.text((68, y_cur), line, font=f_t, fill=(248, 250, 252))
        y_cur += 62
    y_cur += 16
    for line in textwrap.wrap(subtitle, width=76)[:2]:
        draw.text((68, y_cur), line, font=f_s, fill=(148, 163, 184))
        y_cur += 35

    draw.line([(68, 542), (W - 68, 542)], fill=(30, 41, 59), width=2)
    draw.text((68, 562), "gabhack.github.io/turingtec-agent-studio", font=f_s, fill=(96, 165, 250))
    draw.text((W - 445, 562), "Self-Hosted AI Agents · MCP · FinOps", font=f_s, fill=(148, 163, 184))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)


def build_solution_html(sol: dict) -> str:
    slug = sol["slug"]
    canonical = f"{BASE_URL}/solutions/{slug}/"
    rows_html = "".join(f"<tr><td><strong>{esc(k)}</strong></td><td>{esc(v)}</td></tr>" for k, v in sol["rows"])
    faqs_html = "".join(f"<div style='margin-top:0.85rem;'><h3 style='margin:0 0 0.25rem; font-size:1rem;'>{esc(q)}</h3><p style='margin:0; color:var(--muted); font-size:0.9rem;'>{esc(a)}</p></div>" for q, a in sol["faqs"])
    siblings = "".join(f'<li><a href="../{esc(s["slug"])}/">{esc(s["short_title"])}</a></li>' for s in SOLUTIONS if s["slug"] != slug)
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "TuringTec Agent Studio", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": sol["short_title"], "item": canonical},
                ],
            },
            {
                "@type": "SoftwareApplication",
                "name": sol["short_title"],
                "description": sol["meta_desc"],
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Cross-Platform",
                "url": canonical,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sol["faqs"]],
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(sol['title'])} | TuringTec Agent Studio</title>
  <meta name="description" content="{esc(sol['meta_desc'])}" />
  <link rel="canonical" href="{esc(canonical)}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{esc(sol['title'])}" />
  <meta property="og:description" content="{esc(sol['meta_desc'])}" />
  <meta property="og:url" content="{esc(canonical)}" />
  <meta property="og:image" content="{BASE_URL}/assets/og/{esc(slug)}.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{BASE_URL}/assets/og/{esc(slug)}.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../styles.css" />
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
  <div class="accent-bar" aria-hidden="true"></div>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="../../">
        <div class="brand-mark">TT</div>
        <div><div class="brand-title">TuringTec Agent Studio</div><div class="brand-sub">{esc(sol['short_title'])}</div></div>
      </a>
      <div class="nav-actions">
        <a class="btn" href="../../#sandboxes">Try Live Demo ($0)</a>
        <a class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Get Agent Kits →</a>
      </div>
    </div>
  </header>
  <main class="container">
    <div style="font-size:0.82rem; color:var(--muted); margin-bottom:0.85rem;">
      <a href="../../" style="color:var(--brand); text-decoration:none;">TuringTec Agent Studio</a> / {esc(sol['short_title'])}
    </div>
    <section class="card hero">
      <div>
        <span class="badge badge-brand">{esc(sol['badge'])}</span>
        <h1>{esc(sol['title'])}</h1>
        <p>{esc(sol['intro'])}</p>
      </div>
      <div class="card" style="background:var(--surface-2); box-shadow:none;">
        <div style="font-size:0.8rem; color:var(--muted); font-weight:700;">SELF-HOSTED KIT</div>
        <div style="font-size:1.15rem; font-weight:800; margin:0.2rem 0 0.65rem;">{esc(sol['price_kit'])}</div>
        <div style="font-size:0.8rem; color:var(--muted); font-weight:700;">TURNKEY DEPLOYMENT</div>
        <div style="font-size:1.05rem; font-weight:700; margin:0.2rem 0 0.85rem; color:var(--success);">{esc(sol['price_pilot'])}</div>
        <div style="display:flex; flex-direction:column; gap:0.5rem;">
          <a class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Buy Self-Hosted Kit on Gumroad →</a>
          <a class="btn" href="../../#sandboxes">Test Live Sandbox Free</a>
        </div>
      </div>
    </section>
    <section class="card" style="margin-top:1.2rem;">
      <h2 style="margin:0 0 0.5rem; font-size:1.2rem;">Production Architecture &amp; Capabilities</h2>
      <table class="data-table"><thead><tr><th>Component</th><th>Production Specification</th></tr></thead><tbody>{rows_html}</tbody></table>
    </section>
    <section class="card" style="margin-top:1.2rem;">
      <h2 style="margin:0 0 0.35rem; font-size:1.15rem;">Frequently Asked Questions</h2>
      {faqs_html}
    </section>
    <footer class="footer">
      <div class="footer-grid">
        <div><h4>Other TuringTec AI Agent Solutions</h4><ul>{siblings}</ul></div>
        <div>
          <h4>Quick Links</h4>
          <ul>
            <li><a href="../../">TuringTec Agent Studio Home (4 Live Sandboxes)</a></li>
            <li><a href="{GUMROAD_STORE}" target="_blank" rel="noopener">Gumroad Store ($39–$99 Kits)</a></li>
            <li><a href="https://github.com/gabhack/aws-finops-guard" target="_blank" rel="noopener">aws-finops-guard Open-Core CLI + MCP</a></li>
            <li><a href="https://gabhack.github.io/cloudcert-lab/" target="_blank" rel="noopener">CloudCert Lab Multi-Cloud Simulator</a></li>
          </ul>
        </div>
      </div>
      <div>Updated {TODAY} · TuringTec Agent Studio.</div>
    </footer>
  </main>
</body>
</html>
"""


def main() -> None:
    og_dir = ROOT / "assets" / "og"
    make_og(
        og_dir / "home.png",
        "PRODUCTION AI AGENTS · BYOK",
        "TuringTec Agent Studio — B2B AI Agents & MCP Servers",
        "4 live browser sandboxes (Hardware RFQ, Invoice Extraction, AWS FinOps, Clinic WhatsApp) + $39-$99 self-hosted kits.",
        (28, 105, 212),
    )

    sol_dir = ROOT / "solutions"
    sol_dir.mkdir(exist_ok=True)
    sitemap_urls = [(f"{BASE_URL}/", "1.0")]
    llms = [
        "# TuringTec Agent Studio — Production B2B AI Agents, MCP Servers & n8n Kits (2026–2027)",
        "",
        f"> Live Interactive B2B AI Agent Sandboxes ($0 signup) + Self-Hosted Production Kits ($39-$99 one-time, zero SaaS lock-in): {BASE_URL}/",
        "",
        f"- Live Storefront & 4 Interactive Sandboxes: {BASE_URL}/",
        f"- Complete Reference (llms-full.txt): {BASE_URL}/llms-full.txt",
        f"- Gumroad Store (15 n8n Workflows $39 · AWS FinOps Guard Pro $49 · Business-in-a-Box $99): {GUMROAD_STORE}",
        "- Open-Core AWS FinOps CLI + stdio MCP Server: https://github.com/gabhack/aws-finops-guard",
        "- Apify Dual-Mode Pay-Per-Event MCP Suite: https://github.com/gabhack/apify-cloud-mcp-suite",
        "- CloudCert Lab Multi-Cloud Exam Simulator: https://gabhack.github.io/cloudcert-lab/",
        "",
        "## Vertical AI Agent Solutions",
    ]
    full = list(llms) + ["", "---", ""]

    for sol in SOLUTIONS:
        sdir = sol_dir / sol["slug"]
        sdir.mkdir(parents=True, exist_ok=True)
        (sdir / "index.html").write_text(build_solution_html(sol), encoding="utf-8")
        make_og(og_dir / f"{sol['slug']}.png", sol["badge"], sol["short_title"], sol["meta_desc"], sol["accent"])
        surl = f"{BASE_URL}/solutions/{sol['slug']}/"
        sitemap_urls.append((surl, "0.9"))
        llms.append(f"- [{sol['short_title']}]({surl}): {sol['meta_desc']}")
        full.append(f"### {sol['title']}")
        full.append(f"- URL: {surl}")
        full.append(f"- Pricing: {sol['price_kit']} | {sol['price_pilot']}")
        full.append(f"- Overview: {sol['intro']}")
        for k, v in sol["rows"]:
            full.append(f"  - **{k}:** {v}")
        full.append("")

    (ROOT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    sm_items = "\n".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>" for u, p in sitemap_urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm_items}\n</urlset>\n', encoding="utf-8")
    (ROOT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (ROOT / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")
    (ROOT / "README.md").write_text(
        f"""# TuringTec Agent Studio — Production B2B AI Agents, MCP Servers & n8n Kits

[![Live Sandboxes](https://img.shields.io/badge/Live%20Demos-4%20Interactive%20Sandboxes-1c69d4?style=for-the-badge)]({BASE_URL}/)
[![Gumroad Store](https://img.shields.io/badge/Agent%20Kits-%2439%20to%20%2499%20One--Time-15803d?style=for-the-badge)]({GUMROAD_STORE})
[![Open-Core CLI](https://img.shields.io/badge/Open--Core-aws--finops--guard-f59e0b?style=for-the-badge)](https://github.com/gabhack/aws-finops-guard)

Interactive storefront and open-core B2B AI Agent ecosystem deployed at **$0/month** on GitHub Pages:
- **Live Storefront & 4 Browser Sandboxes:** {BASE_URL}/
- **Vertical Solutions:** Clinic WhatsApp Receptionist · B2B Hardware RFQ Quoter · Invoice PDF-to-ERP Extractor · AWS FinOps Guardrails MCP · 15 n8n Workflows Pack · AI Agent Business-in-a-Box
- **Ecosystem Repos:** [aws-finops-guard](https://github.com/gabhack/aws-finops-guard) · [apify-cloud-mcp-suite](https://github.com/gabhack/apify-cloud-mcp-suite) · [cloudcert-lab](https://gabhack.github.io/cloudcert-lab/)
""",
        encoding="utf-8",
    )
    print(f"OK: Generated {len(SOLUTIONS)} solution SEO pages + {len(SOLUTIONS)+1} OG PNGs + sitemap.xml ({len(sitemap_urls)} URLs) + llms-full.txt")


if __name__ == "__main__":
    main()
