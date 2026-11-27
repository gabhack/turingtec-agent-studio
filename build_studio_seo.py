#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programmatic SEO + GEO + OpenGraph PNG builder for TuringTec Agent Studio.
Generates 6 vertical solution landing pages (/solutions/<slug>/index.html),
3 high-intent comparison + interactive ROI calculator pages (/compare/<slug>/index.html),
10 branded 1200x630 OG PNGs, robots.txt, sitemap.xml (10 URLs), llms.txt, llms-full.txt,
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

COMPARES = [
    {
        "slug": "n8n-vs-zapier-vs-make-calculator",
        "badge": "INTERACTIVE COST CALCULATOR · N8N VS ZAPIER VS MAKE",
        "title": "n8n vs Zapier vs Make Pricing Calculator (2026–2027): Real Annual Self-Hosted Savings",
        "short_title": "n8n vs Zapier vs Make Cost Calculator",
        "meta_desc": "Calculate your exact annual automation bill across Zapier, Make, and self-hosted Docker n8n ($0 software / ~$15/mo VPS). Slide monthly runs and steps to see USD/year saved.",
        "accent": (14, 165, 233),
        "bluf": "At 10,000 monthly workflow runs averaging 6 steps (60,000 tasks/month), Zapier costs ~$5,748/year and Make costs ~$1,284/year—while self-hosted Docker n8n runs for ~$180/year (~$15/mo VPS, $0 software license), saving up to $5,568/year.",
        "intro": "Per-task SaaS automation pricing punishes AI agents that run multi-step loops, webhooks, and LLM retries. Use the interactive slider calculator below to model your real monthly runs and step counts across Zapier, Make, and self-hosted n8n.",
        "sticky_label": "Self-Host n8n ($15/mo VPS): Save thousands/yr with 15 Production AI Workflows ($39) or Business-in-a-Box ($99)",
        "sticky_cta_text": "Get 15 n8n Workflows ($39) →",
        "sticky_cta_url": GUMROAD_STORE,
        "table_headers": ["Platform", "Billing Model", "60k Tasks / Mo Est.", "Self-Host / BYOK Control", "Best For"],
        "table_rows": [
            ("Self-Hosted n8n (Docker)", "$0 Software + ~$15/mo VPS", "$15 / mo ($180 / yr)", "100% Own Server & API Keys", "AI Agents, High-Volume B2B, Agencies"),
            ("Make (Integromat)", "Per Operation (~$1.60 / 1k ops)", "~$107 / mo ($1,284 / yr)", "Cloud SaaS Only", "Visual Mid-Volume Integrations"),
            ("Zapier (Pro / Team)", "Per Task (~$7.50 / 1k tasks)", "~$479 / mo ($5,748 / yr)", "Cloud SaaS Only", "Simple Low-Volume Point-to-Point"),
        ],
        "faqs": [
            ("Is self-hosted n8n really $0 in software licensing fees?", "Yes. Using the official n8n Docker image under the Sustainable Use License for internal business operations costs $0 in software fees—you only pay for a small $10–$20/mo VPS (or run locally)."),
            ("Why do AI agent workflows get so expensive on Zapier and Make?", "Every LLM call, JSON parse, router branch, and retry counts as a billable task or operation. A single 6-step WhatsApp or RFQ AI agent running 10,000 times/month consumes 60,000 billable tasks."),
            ("How fast does the $39 n8n Workflows Pack pay for itself?", "Even on modest automation volume (5,000–10,000 runs/month), switching from Zapier to self-hosted n8n recovers the $39 pack cost in under 4 days."),
        ],
        "calc_html": f"""
    <section class="card" style="margin-top:1.2rem;">
      <span class="badge badge-brand">LIVE INTERACTIVE SLIDERS · INSTANT RECALCULATION</span>
      <h2 style="margin:0.4rem 0 0.9rem; font-size:1.25rem;">Zapier vs Make vs Self-Hosted n8n Annual Cost Calculator</h2>
      <div class="sandbox-grid">
        <div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="n8nRuns"><strong>Monthly Workflow Runs</strong></label>
              <span class="calc-slider-val" id="n8nRunsVal">10,000 runs/mo</span>
            </div>
            <input id="n8nRuns" type="range" min="1000" max="100000" step="1000" value="10000" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="n8nSteps"><strong>Average Steps / Actions per Workflow</strong></label>
              <span class="calc-slider-val" id="n8nStepsVal">6 steps</span>
            </div>
            <input id="n8nSteps" type="range" min="2" max="15" step="1" value="6" />
          </div>
          <div class="card" style="background:var(--surface-2); box-shadow:none; padding:0.9rem;">
            <div style="font-size:0.8rem; color:var(--muted); font-weight:700;">MONTHLY BILLABLE OPERATIONS</div>
            <div id="n8nTasksTotal" style="font-size:1.45rem; font-weight:800; color:var(--fg);">60,000 tasks / mo</div>
            <div style="font-size:0.8rem; color:var(--muted); margin-top:0.25rem;">Self-hosted n8n executes unlimited internal steps on a ~$15/mo VPS ($180/yr).</div>
          </div>
        </div>
        <div>
          <div class="calc-result-grid">
            <div class="calc-stat danger">
              <div class="calc-stat-label">Zapier Annual</div>
              <div class="calc-stat-val" id="n8nZapierYr">$5,748/yr</div>
            </div>
            <div class="calc-stat">
              <div class="calc-stat-label">Make Annual</div>
              <div class="calc-stat-val" id="n8nMakeYr">$1,284/yr</div>
            </div>
            <div class="calc-stat highlight">
              <div class="calc-stat-label">Self-Hosted n8n</div>
              <div class="calc-stat-val" id="n8nSelfYr">$180/yr</div>
            </div>
          </div>
          <div class="card" style="background:var(--surface-2); box-shadow:none; padding:1rem;">
            <div style="font-size:0.82rem; font-weight:700; color:var(--success);">ESTIMATED ANNUAL SAVINGS WITH SELF-HOSTED N8N</div>
            <div id="n8nSavingsHeadline" style="font-size:1.5rem; font-weight:800; color:var(--success); margin:0.2rem 0;">Save $5,568/yr vs Zapier · $1,104/yr vs Make</div>
            <div id="n8nPaybackNote" style="font-size:0.84rem; color:var(--muted); margin-bottom:0.85rem;">The $39 n8n Workflows Pack pays for itself in ~3 days of Zapier savings.</div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a id="n8nCtaPack" class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Save $5,568/yr — Get 15 n8n Workflows ($39) →</a>
              <a id="n8nCtaBox" class="btn" href="{GUMROAD_STORE}" target="_blank" rel="noopener">All-Access Business-in-a-Box ($99) →</a>
            </div>
          </div>
        </div>
      </div>
    </section>""",
        "calc_js": """
    (function() {
      var runsEl = document.getElementById('n8nRuns');
      var stepsEl = document.getElementById('n8nSteps');
      if (!runsEl || !stepsEl) return;
      function fmt(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
      function update() {
        var runs = Number(runsEl.value) || 10000;
        var steps = Number(stepsEl.value) || 6;
        var tasks = runs * steps;
        var zapierMo = Math.max(29, Math.round(tasks * 0.0075 + 29));
        var makeMo = Math.max(11, Math.round(tasks * 0.0016 + 11));
        var n8nMo = 15;
        var zapierYr = zapierMo * 12;
        var makeYr = makeMo * 12;
        var n8nYr = n8nMo * 12;
        var saveZapier = Math.max(0, zapierYr - n8nYr);
        var saveMake = Math.max(0, makeYr - n8nYr);
        var paybackDays = Math.max(1, Math.round(39 / Math.max(0.5, (zapierMo - n8nMo) / 30)));
        document.getElementById('n8nRunsVal').textContent = runs.toLocaleString('en-US') + ' runs/mo';
        document.getElementById('n8nStepsVal').textContent = steps + ' steps';
        document.getElementById('n8nTasksTotal').textContent = tasks.toLocaleString('en-US') + ' tasks / mo';
        document.getElementById('n8nZapierYr').textContent = fmt(zapierYr) + '/yr';
        document.getElementById('n8nMakeYr').textContent = fmt(makeYr) + '/yr';
        document.getElementById('n8nSelfYr').textContent = fmt(n8nYr) + '/yr';
        document.getElementById('n8nSavingsHeadline').textContent = 'Save ' + fmt(saveZapier) + '/yr vs Zapier · ' + fmt(saveMake) + '/yr vs Make';
        document.getElementById('n8nPaybackNote').textContent = 'The $39 n8n Workflows Pack pays for itself in ~' + paybackDays + ' day' + (paybackDays === 1 ? '' : 's') + ' of Zapier savings.';
        document.getElementById('n8nCtaPack').textContent = 'Save ' + fmt(saveZapier) + '/yr — Get 15 n8n Workflows ($39) →';
      }
      runsEl.addEventListener('input', update);
      runsEl.addEventListener('change', update);
      stepsEl.addEventListener('input', update);
      stepsEl.addEventListener('change', update);
      update();
    })();""",
    },
    {
        "slug": "aws-finops-open-source-tools",
        "badge": "CLOUD & LLM FINOPS BENCHMARK · OPEN-SOURCE COMPARISON",
        "title": "AWS FinOps Open-Source Tools Compared (2026–2027): aws-finops-guard vs Infracost vs OpenCost vs Cost Explorer",
        "short_title": "AWS FinOps Open-Source Tools + Waste Estimator",
        "meta_desc": "Objective comparison of aws-finops-guard, Infracost, OpenCost, and AWS Cost Explorer—plus an interactive AWS & LLM Monthly Waste Estimator showing annual waste and payback in hours.",
        "accent": (245, 158, 11),
        "bluf": "Infracost estimates pre-deploy Terraform PR costs, OpenCost tracks Kubernetes pods, and AWS Cost Explorer shows historical spend—while aws-finops-guard audits live AWS + LLM token waste locally via CLI or Claude/Cursor MCP Server and outputs ready-to-apply Terraform HCL fixes.",
        "intro": "Modern cloud teams leak 25–40% of their budget across unattached EBS volumes, idle NAT Gateways, legacy gp2 storage, and unrouted LLM API calls. Compare the top FinOps tools objectively below and estimate your exact recoverable AWS + AI waste.",
        "sticky_label": "aws-finops-guard: Free Open-Core CLI + MCP · $49 Pro Terraform Auto-Fix · $99 Business-in-a-Box",
        "sticky_cta_text": "Unlock Pro License ($49) →",
        "sticky_cta_url": GUMROAD_STORE,
        "table_headers": ["Tool", "Primary Scope", "Live AWS + LLM Token Audit", "Claude / Cursor MCP Server", "Terraform HCL Auto-Fix", "Pricing / License"],
        "table_rows": [
            ("aws-finops-guard", "Live AWS Waste + LLM API Routing", "✓ Yes (EBS, NAT, RDS, S3, Bedrock/OpenAI/Gemini)", "✓ Native stdio JSON-RPC 2.0", "✓ Pro ($49 one-time) + SARIF 2.1.0", "MIT Open-Core ($0) / $49 Pro"),
            ("Infracost", "Pre-Deploy Terraform PR Cost Diffs", "Pre-deploy IaC only (No LLM audit)", "✗ No native FinOps MCP", "✗ Estimates only (No auto-patch)", "Apache 2.0 / Cloud SaaS ($50+/seat)"),
            ("OpenCost", "Kubernetes Pod & Cluster Costing", "K8s clusters only (No LLM audit)", "✗ No", "✗ Reporting only", "CNCF Apache 2.0 ($0)"),
            ("AWS Cost Explorer", "Historical AWS Billing Console", "AWS billing only (No LLM prompt audit)", "✗ No", "✗ Manual console changes", "Free UI / $0.01 per API request"),
        ],
        "faqs": [
            ("How is aws-finops-guard different from Infracost and OpenCost?", "Infracost shines at PR-time Terraform estimates and OpenCost specializes in Kubernetes. aws-finops-guard fills the gap for live AWS waste (idle NAT, gp2->gp3, unattached EBS, idle RDS) AND AI/LLM token overspending, natively inside your terminal or Claude/Cursor via MCP."),
            ("Does aws-finops-guard ever upload my AWS credentials or billing data?", "No. It runs 100% locally against your JSON snapshots or read-only local context with zero third-party SaaS telemetry."),
            ("What does the $49 Pro License unlock?", "Safe Terraform HCL remediation patches, copy-paste AWS CLI commands, and CI/CD SARIF 2.1.0 output so your pipeline blocks wasteful deploys automatically."),
        ],
        "calc_html": f"""
    <section class="card" style="margin-top:1.2rem;">
      <span class="badge badge-warning">INTERACTIVE AWS &amp; LLM WASTE ESTIMATOR</span>
      <h2 style="margin:0.4rem 0 0.9rem; font-size:1.25rem;">Estimate Your Annual Cloud + AI Waste &amp; Payback Period in Hours</h2>
      <div class="sandbox-grid">
        <div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="finAwsSpend"><strong>Monthly AWS Spend (USD)</strong></label>
              <span class="calc-slider-val" id="finAwsSpendVal">$8,000 / mo</span>
            </div>
            <input id="finAwsSpend" type="range" min="1000" max="50000" step="500" value="8000" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="finWastePct"><strong>Est. Idle / Oversized AWS Waste (%)</strong></label>
              <span class="calc-slider-val" id="finWastePctVal">28%</span>
            </div>
            <input id="finWastePct" type="range" min="10" max="45" step="1" value="28" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="finLlmSpend"><strong>Monthly LLM API Spend (OpenAI / Bedrock / Gemini)</strong></label>
              <span class="calc-slider-val" id="finLlmSpendVal">$2,400 / mo</span>
            </div>
            <input id="finLlmSpend" type="range" min="200" max="20000" step="200" value="2400" />
          </div>
        </div>
        <div>
          <div class="calc-result-grid">
            <div class="calc-stat danger">
              <div class="calc-stat-label">Monthly Waste</div>
              <div class="calc-stat-val" id="finMonthlyWaste">$3,080/mo</div>
            </div>
            <div class="calc-stat danger">
              <div class="calc-stat-label">Annual Waste</div>
              <div class="calc-stat-val" id="finAnnualWaste">$36,960/yr</div>
            </div>
            <div class="calc-stat highlight">
              <div class="calc-stat-label">$49 Pro Payback</div>
              <div class="calc-stat-val" id="finPaybackHrs">11.5 hrs</div>
            </div>
          </div>
          <div class="card" style="background:var(--surface-2); box-shadow:none; padding:1rem;">
            <div style="font-size:0.82rem; font-weight:700; color:var(--warning);">RECOVERABLE CLOUD + LLM BUDGET</div>
            <div id="finSummaryLine" style="font-size:1.3rem; font-weight:800; color:var(--fg); margin:0.2rem 0;">$2,240/mo AWS + $840/mo LLM Routing = $36,960/yr</div>
            <div id="finPaybackDetail" style="font-size:0.84rem; color:var(--muted); margin-bottom:0.85rem;">The $49 Pro License pays back in 11.5 hours; the $99 Business-in-a-Box pays back in 23.1 hours.</div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a class="btn" href="https://github.com/gabhack/aws-finops-guard" target="_blank" rel="noopener">Clone Open-Core CLI ($0) →</a>
              <a id="finCtaPro" class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Recover $36,960/yr — Unlock Pro ($49) →</a>
              <a class="btn" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Business-in-a-Box ($99)</a>
            </div>
          </div>
        </div>
      </div>
    </section>""",
        "calc_js": """
    (function() {
      var awsEl = document.getElementById('finAwsSpend');
      var pctEl = document.getElementById('finWastePct');
      var llmEl = document.getElementById('finLlmSpend');
      if (!awsEl || !pctEl || !llmEl) return;
      function fmt(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
      function update() {
        var aws = Number(awsEl.value) || 8000;
        var pct = Number(pctEl.value) || 28;
        var llm = Number(llmEl.value) || 2400;
        var awsWaste = Math.round(aws * (pct / 100));
        var llmWaste = Math.round(llm * 0.35);
        var moWaste = awsWaste + llmWaste;
        var yrWaste = moWaste * 12;
        var hrs49 = Math.max(0.5, 49 / Math.max(0.1, moWaste / 720));
        var hrs99 = Math.max(1.0, 99 / Math.max(0.1, moWaste / 720));
        document.getElementById('finAwsSpendVal').textContent = fmt(aws) + ' / mo';
        document.getElementById('finWastePctVal').textContent = pct + '%';
        document.getElementById('finLlmSpendVal').textContent = fmt(llm) + ' / mo';
        document.getElementById('finMonthlyWaste').textContent = fmt(moWaste) + '/mo';
        document.getElementById('finAnnualWaste').textContent = fmt(yrWaste) + '/yr';
        document.getElementById('finPaybackHrs').textContent = hrs49.toFixed(1) + ' hrs';
        document.getElementById('finSummaryLine').textContent = fmt(awsWaste) + '/mo AWS + ' + fmt(llmWaste) + '/mo LLM Routing = ' + fmt(yrWaste) + '/yr';
        document.getElementById('finPaybackDetail').textContent = 'The $49 Pro License pays back in ' + hrs49.toFixed(1) + ' hours; the $99 Business-in-a-Box pays back in ' + hrs99.toFixed(1) + ' hours.';
        document.getElementById('finCtaPro').textContent = 'Recover ' + fmt(yrWaste) + '/yr — Unlock Pro ($49) →';
      }
      [awsEl, pctEl, llmEl].forEach(function(el) {
        el.addEventListener('input', update);
        el.addEventListener('change', update);
      });
      update();
    })();""",
    },
    {
        "slug": "clinic-whatsapp-ai-bot-roi",
        "badge": "HEALTHCARE ROI CALCULATOR · ANTI-NO-SHOW WHATSAPP AI",
        "title": "Clinic WhatsApp AI Bot & Anti-No-Show ROI Calculator (2026–2027)",
        "short_title": "Clinic WhatsApp AI Bot ROI Calculator",
        "meta_desc": "Calculate how much monthly and annual revenue your medical, dental, or aesthetic clinic recovers with a 24/7 self-hosted WhatsApp booking & 24h/2h anti-no-show AI receptionist.",
        "accent": (16, 185, 129),
        "bluf": "A clinic handling 300 monthly WhatsApp inquiries with a 22% no-show/missed-lead rate at $75/consultation loses ~$4,950/month. Recovering 65% via 24/7 instant booking and 24h/2h automated reminders adds ~$3,225/month ($38,700/year)—paying back a $690 7-day turnkey pilot in under 7 days.",
        "intro": "Patients message clinics after hours and forget appointments without timely reminders. Model your clinic's monthly WhatsApp inquiries, no-show rate, and consultation ticket below to see exact recovered revenue with ClinicFlow AI.",
        "sticky_label": "ClinicFlow AI: $39 Self-Hosted n8n Workflow · $690 7-Day Turnkey Clinic Pilot (BYOK)",
        "sticky_cta_text": "Get Clinic Workflow ($39) →",
        "sticky_cta_url": GUMROAD_STORE,
        "table_headers": ["Workflow Stage", "Manual Front Desk", "ClinicFlow AI (Self-Hosted WhatsApp)", "Measurable Impact"],
        "table_rows": [
            ("After-Hours Inquiries (7pm–8am)", "Unanswered until next day (lead books elsewhere)", "Instant 24/7 WhatsApp triage + live calendar booking", "+35–50% after-hours booking capture"),
            ("24h & 2h Appointment Reminders", "Manual calls or forgotten SMS", "Automated WhatsApp 1-tap Confirm / Reschedule", "Up to 65% reduction in empty chair no-shows"),
            ("Cancellations & Waitlist", "Chair stays empty", "Auto-pings waitlist patients to fill open slots", "Higher daily practitioner utilization"),
            ("Monthly Software Cost", "$299–$599/mo SaaS CRM seats", "$0 software (Docker n8n) + ~$0.004/WhatsApp window", "Zero per-seat SaaS lock-in"),
        ],
        "faqs": [
            ("How does ClinicFlow AI reduce no-shows without annoying patients?", "It sends clean, polite WhatsApp confirmations 24 hours and 2 hours before the visit with 1-tap confirm or reschedule buttons, automatically freeing cancelled slots for waitlist patients."),
            ("Do we keep ownership of our WhatsApp Business number and patient data?", "Yes. ClinicFlow runs 100% BYOK on your own Meta WhatsApp Cloud API, Google Calendar / EMR webhooks, and self-hosted n8n instance."),
            ("Should we buy the $39 n8n Workflow or the $690 7-Day Turnkey Pilot?", "If you have an internal developer or agency, grab the $39 n8n Pack (or $99 Business-in-a-Box). If you want our engineering team to connect WhatsApp, Calendar, guardrails, and train your receptionists in 7 days, book the $690 pilot."),
        ],
        "calc_html": f"""
    <section class="card" style="margin-top:1.2rem;">
      <span class="badge badge-success">INTERACTIVE CLINIC REVENUE CALCULATOR</span>
      <h2 style="margin:0.4rem 0 0.9rem; font-size:1.25rem;">Calculate Your Monthly &amp; Annual Recovered Clinic Revenue</h2>
      <div class="sandbox-grid">
        <div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="clInquiries"><strong>Monthly Patient WhatsApp Inquiries</strong></label>
              <span class="calc-slider-val" id="clInquiriesVal">300 / mo</span>
            </div>
            <input id="clInquiries" type="range" min="50" max="2000" step="25" value="300" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="clNoShowPct"><strong>Current No-Show &amp; Missed-Lead Rate (%)</strong></label>
              <span class="calc-slider-val" id="clNoShowPctVal">22%</span>
            </div>
            <input id="clNoShowPct" type="range" min="5" max="45" step="1" value="22" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head">
              <label for="clAvgConsult"><strong>Average Consultation / Procedure Value (USD)</strong></label>
              <span class="calc-slider-val" id="clAvgConsultVal">$75</span>
            </div>
            <input id="clAvgConsult" type="range" min="25" max="350" step="5" value="75" />
          </div>
        </div>
        <div>
          <div class="calc-result-grid">
            <div class="calc-stat">
              <div class="calc-stat-label">Recovered Visits/Mo</div>
              <div class="calc-stat-val" id="clRecVisits">43 visits</div>
            </div>
            <div class="calc-stat highlight">
              <div class="calc-stat-label">Monthly Recovered</div>
              <div class="calc-stat-val" id="clRecMonth">$3,225/mo</div>
            </div>
            <div class="calc-stat highlight">
              <div class="calc-stat-label">Annual Recovered</div>
              <div class="calc-stat-val" id="clRecYear">$38,700/yr</div>
            </div>
          </div>
          <div class="card" style="background:var(--surface-2); box-shadow:none; padding:1rem;">
            <div style="font-size:0.82rem; font-weight:700; color:var(--success);">ESTIMATED ANTI-NO-SHOW IMPACT (65% CONSERVATIVE RECOVERY)</div>
            <div id="clSummaryLine" style="font-size:1.25rem; font-weight:800; color:var(--fg); margin:0.2rem 0;">Recover $3,225/mo ($38,700/yr) from 66 monthly missed slots</div>
            <div id="clPaybackLine" style="font-size:0.84rem; color:var(--muted); margin-bottom:0.85rem;">The $690 7-Day Turnkey Pilot pays for itself in ~6 days; the $39 n8n workflow pays back on the very first recovered patient.</div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a id="clCtaWorkflow" class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Recover $38,700/yr — Get n8n Workflow ($39) →</a>
              <a id="clCtaPilot" class="btn" href="mailto:gabhack@gmail.com?subject=TuringTec%207-Day%20Clinic%20WhatsApp%20AI%20Pilot%20($690)&body=Hi%20Gabriel%2C%0A%0AI%20calculated%20our%20Clinic%20WhatsApp%20AI%20ROI%20and%20want%20to%20launch%20the%207-Day%20Turnkey%20Pilot%20($690).%0AMonthly%20inquiries%3A%20%0ACountry%3A%20">Book 7-Day Turnkey Pilot ($690) →</a>
            </div>
          </div>
        </div>
      </div>
    </section>""",
        "calc_js": """
    (function() {
      var inqEl = document.getElementById('clInquiries');
      var nsEl = document.getElementById('clNoShowPct');
      var valEl = document.getElementById('clAvgConsult');
      if (!inqEl || !nsEl || !valEl) return;
      function fmt(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
      function update() {
        var inq = Number(inqEl.value) || 300;
        var nsPct = Number(nsEl.value) || 22;
        var ticket = Number(valEl.value) || 75;
        var missed = Math.round(inq * (nsPct / 100));
        var recovered = Math.max(1, Math.round(missed * 0.65));
        var recMo = recovered * ticket;
        var recYr = recMo * 12;
        var pilotDays = Math.max(1, Math.round(690 / Math.max(1, recMo / 30)));
        document.getElementById('clInquiriesVal').textContent = inq.toLocaleString('en-US') + ' / mo';
        document.getElementById('clNoShowPctVal').textContent = nsPct + '%';
        document.getElementById('clAvgConsultVal').textContent = fmt(ticket);
        document.getElementById('clRecVisits').textContent = recovered + ' visits';
        document.getElementById('clRecMonth').textContent = fmt(recMo) + '/mo';
        document.getElementById('clRecYear').textContent = fmt(recYr) + '/yr';
        document.getElementById('clSummaryLine').textContent = 'Recover ' + fmt(recMo) + '/mo (' + fmt(recYr) + '/yr) from ' + missed + ' monthly missed slots';
        document.getElementById('clPaybackLine').textContent = 'The $690 7-Day Turnkey Pilot pays for itself in ~' + pilotDays + ' day' + (pilotDays === 1 ? '' : 's') + '; the $39 n8n workflow pays back on the very first recovered patient.';
        document.getElementById('clCtaWorkflow').textContent = 'Recover ' + fmt(recYr) + '/yr — Get n8n Workflow ($39) →';
      }
      [inqEl, nsEl, valEl].forEach(function(el) {
        el.addEventListener('input', update);
        el.addEventListener('change', update);
      });
      update();
    })();""",
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
    compare_links = "".join(f'<li><a href="../../compare/{esc(c["slug"])}/">{esc(c["short_title"])}</a></li>' for c in COMPARES)
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
  <script src="https://gumroad.com/js/gumroad.js" defer></script>
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body class="has-sticky-cro">
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
        <div class="quick-answer-box">
          <strong>Quick ROI Summary:</strong> Self-host with zero monthly SaaS lock-in (<strong>{esc(sol['price_kit'])}</strong>) or launch a turnkey deployment (<strong>{esc(sol['price_pilot'])}</strong>). Test interactive browser sandboxes free first.
        </div>
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
        <div><h4>Interactive ROI Calculators &amp; Comparisons</h4><ul>{compare_links}</ul></div>
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
  <aside class="sticky-cro-bar" aria-label="Quick TuringTec Agent Studio actions">
    <div class="sticky-cro-inner">
      <div style="font-size:0.82rem;">
        <strong>{esc(sol['short_title'])}:</strong> {esc(sol['price_kit'])} · <strong>{esc(sol['price_pilot'])}</strong>
      </div>
      <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
        <a class="btn" href="../../#sandboxes">Try Live Demo ($0)</a>
        <a class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Get Self-Hosted Kit →</a>
      </div>
    </div>
  </aside>
</body>
</html>
"""


def build_compare_html(cmp: dict) -> str:
    slug = cmp["slug"]
    canonical = f"{BASE_URL}/compare/{slug}/"
    og_name = f"compare-{slug}.png"
    th_html = "".join(f"<th>{esc(h)}</th>" for h in cmp["table_headers"])
    tr_html = "".join(
        "<tr>" + "".join(
            f"<td><strong>{esc(cell)}</strong></td>" if i == 0 else f"<td>{esc(cell)}</td>"
            for i, cell in enumerate(row)
        ) + "</tr>"
        for row in cmp["table_rows"]
    )
    faqs_html = "".join(
        f"<div style='margin-top:0.85rem;'><h3 style='margin:0 0 0.25rem; font-size:1rem;'>{esc(q)}</h3><p style='margin:0; color:var(--muted); font-size:0.9rem;'>{esc(a)}</p></div>"
        for q, a in cmp["faqs"]
    )
    other_compares = "".join(
        f'<li><a href="../{esc(c["slug"])}/">{esc(c["short_title"])}</a></li>'
        for c in COMPARES if c["slug"] != slug
    )
    sol_links = "".join(
        f'<li><a href="../../solutions/{esc(s["slug"])}/">{esc(s["short_title"])}</a></li>'
        for s in SOLUTIONS
    )
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "TuringTec Agent Studio", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": cmp["short_title"], "item": canonical},
                ],
            },
            {
                "@type": "SoftwareApplication",
                "name": cmp["short_title"],
                "description": cmp["meta_desc"],
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Web, Cross-Platform",
                "url": canonical,
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in cmp["faqs"]
                ],
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(cmp['title'])} | TuringTec Agent Studio</title>
  <meta name="description" content="{esc(cmp['meta_desc'])}" />
  <link rel="canonical" href="{esc(canonical)}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{esc(cmp['title'])}" />
  <meta property="og:description" content="{esc(cmp['meta_desc'])}" />
  <meta property="og:url" content="{esc(canonical)}" />
  <meta property="og:image" content="{BASE_URL}/assets/og/{esc(og_name)}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{BASE_URL}/assets/og/{esc(og_name)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../styles.css" />
  <script src="https://gumroad.com/js/gumroad.js" defer></script>
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body class="has-sticky-cro">
  <div class="accent-bar" aria-hidden="true"></div>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="../../">
        <div class="brand-mark">TT</div>
        <div><div class="brand-title">TuringTec Agent Studio</div><div class="brand-sub">{esc(cmp['short_title'])}</div></div>
      </a>
      <div class="nav-actions">
        <a class="btn" href="../../#sandboxes">Live Sandboxes ($0)</a>
        <a class="btn" href="../../#kits">Agent Kits ($39–$99)</a>
        <a class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Open Gumroad Store →</a>
      </div>
    </div>
  </header>
  <main class="container">
    <div style="font-size:0.82rem; color:var(--muted); margin-bottom:0.85rem;">
      <a href="../../" style="color:var(--brand); text-decoration:none;">TuringTec Agent Studio</a> / Compare / {esc(cmp['short_title'])}
    </div>
    <section class="card hero" style="grid-template-columns: 1fr;">
      <div>
        <span class="badge badge-brand">{esc(cmp['badge'])}</span>
        <h1>{esc(cmp['title'])}</h1>
        <p>{esc(cmp['intro'])}</p>
        <div class="quick-answer-box">
          <strong>Bottom Line Up Front (BLUF):</strong> {esc(cmp['bluf'])}
        </div>
      </div>
    </section>
    {cmp['calc_html']}
    <section class="card" style="margin-top:1.2rem; overflow-x:auto;">
      <h2 style="margin:0 0 0.5rem; font-size:1.2rem;">Side-by-Side Comparison Matrix (2026–2027)</h2>
      <table class="data-table"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table>
    </section>
    <section class="card" style="margin-top:1.2rem;">
      <h2 style="margin:0 0 0.35rem; font-size:1.15rem;">Frequently Asked Questions</h2>
      {faqs_html}
    </section>
    <footer class="footer">
      <div class="footer-grid">
        <div><h4>Other ROI Calculators &amp; Comparisons</h4><ul>{other_compares}</ul></div>
        <div><h4>Vertical AI Agent Solutions</h4><ul>{sol_links}</ul></div>
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
  <aside class="sticky-cro-bar" aria-label="Quick TuringTec Agent Studio actions">
    <div class="sticky-cro-inner">
      <div style="font-size:0.82rem;"><strong>{esc(cmp['sticky_label'])}</strong></div>
      <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
        <a class="btn" href="../../#sandboxes">Try Live Demos ($0)</a>
        <a class="btn btn-primary" href="{esc(cmp['sticky_cta_url'])}" target="_blank" rel="noopener">{esc(cmp['sticky_cta_text'])}</a>
      </div>
    </div>
  </aside>
  <script>{cmp['calc_js']}</script>
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
    cmp_dir = ROOT / "compare"
    cmp_dir.mkdir(exist_ok=True)
    sitemap_urls = [(f"{BASE_URL}/", "1.0")]
    llms = [
        "# TuringTec Agent Studio — Production B2B AI Agents, MCP Servers & n8n Kits (2026–2027)",
        "",
        f"> Live Interactive B2B AI Agent Sandboxes ($0 signup) + 3 ROI Calculators + Self-Hosted Production Kits ($39-$99 one-time, zero SaaS lock-in): {BASE_URL}/",
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

    llms.append("")
    llms.append("## Interactive Comparisons & ROI Calculators")
    full.append("---")
    full.append("")
    full.append("## Interactive Comparisons & ROI Calculators")
    full.append("")
    for cmp in COMPARES:
        cdir = cmp_dir / cmp["slug"]
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / "index.html").write_text(build_compare_html(cmp), encoding="utf-8")
        make_og(og_dir / f"compare-{cmp['slug']}.png", cmp["badge"], cmp["short_title"], cmp["meta_desc"], cmp["accent"])
        curl = f"{BASE_URL}/compare/{cmp['slug']}/"
        sitemap_urls.append((curl, "0.9"))
        llms.append(f"- [{cmp['short_title']}]({curl}): {cmp['meta_desc']}")
        full.append(f"### {cmp['title']}")
        full.append(f"- URL: {curl}")
        full.append(f"- BLUF: {cmp['bluf']}")
        full.append(f"- Overview: {cmp['intro']}")
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
- **Interactive ROI Calculators & Comparisons:**
  - [n8n vs Zapier vs Make Annual Cost Calculator]({BASE_URL}/compare/n8n-vs-zapier-vs-make-calculator/)
  - [AWS FinOps Open-Source Tools + Waste Estimator]({BASE_URL}/compare/aws-finops-open-source-tools/)
  - [Clinic WhatsApp AI Bot Anti-No-Show ROI Calculator]({BASE_URL}/compare/clinic-whatsapp-ai-bot-roi/)
- **Vertical Solutions:** Clinic WhatsApp Receptionist · B2B Hardware RFQ Quoter · Invoice PDF-to-ERP Extractor · AWS FinOps Guardrails MCP · 15 n8n Workflows Pack · AI Agent Business-in-a-Box
- **Ecosystem Repos:** [aws-finops-guard](https://github.com/gabhack/aws-finops-guard) · [apify-cloud-mcp-suite](https://github.com/gabhack/apify-cloud-mcp-suite) · [cloudcert-lab](https://gabhack.github.io/cloudcert-lab/)
""",
        encoding="utf-8",
    )
    print(f"OK: Generated {len(SOLUTIONS)} solution SEO pages + {len(COMPARES)} compare ROI calculator pages + {len(SOLUTIONS)+len(COMPARES)+1} OG PNGs + sitemap.xml ({len(sitemap_urls)} URLs) + llms-full.txt")


if __name__ == "__main__":
    main()
