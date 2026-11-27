#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Bilingual (EN + ES) Site, SEO, GEO & OpenGraph Builder for TuringTec Agent Studio v2.
Generates 20 static pages (10 EN + 10 ES):
  - /index.html & /es/index.html (Elite Deep-Tech Storefront + 4 Live Sandboxes)
  - /solutions/<6 slugs>/index.html & /es/solutions/<6 slugs>/index.html
  - /compare/<3 slugs>/index.html & /es/compare/<3 slugs>/index.html (Interactive ROI Calculators)
  - 20 localized 1200x630 OG PNGs, hreflang-reciprocal sitemap.xml, robots.txt, llms.txt & llms-full.txt.
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
CLOUDCERT_URL = "https://gabhack.github.io/cloudcert-lab/"
FINOPS_REPO = "https://github.com/gabhack/aws-finops-guard"
APIFY_REPO = "https://github.com/gabhack/apify-cloud-mcp-suite"
TODAY = datetime.date.today().isoformat()
INDEXNOW_KEY = "c8e4a91f7b2d406ea35c89f14d2b7019"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def make_og(out_path: Path, badge: str, title: str, subtitle: str, accent: tuple[int, int, int], lang: str = "en") -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (7, 9, 15))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(7 + 9 * t), int(10 + 13 * t), int(18 + 22 * t)))
    for rad in range(380, 40, -30):
        f = 0.015 * (380 - rad) / 340
        c = (
            min(255, int(11 + accent[0] * f * 4.5)),
            min(255, int(16 + accent[1] * f * 4.5)),
            min(255, int(28 + accent[2] * f * 4.5)),
        )
        draw.ellipse([W - 220 - rad, -60 - rad, W - 220 + rad, -60 + rad], fill=c)

    draw.rectangle([0, 0, 14, H], fill=accent)
    draw.rectangle([0, 0, W, 6], fill=accent)

    f_b = ImageFont.truetype(FONT_BOLD, 26) if Path(FONT_BOLD).exists() else ImageFont.load_default()
    f_bg = ImageFont.truetype(FONT_BOLD, 19) if Path(FONT_BOLD).exists() else ImageFont.load_default()
    f_t = ImageFont.truetype(FONT_BOLD, 48) if Path(FONT_BOLD).exists() else ImageFont.load_default()
    f_s = ImageFont.truetype(FONT_REG, 24) if Path(FONT_REG).exists() else ImageFont.load_default()

    draw.rounded_rectangle([68, 52, 126, 110], radius=12, fill=accent)
    draw.text((80, 66), "TT", font=f_b, fill=(255, 255, 255))
    draw.text((144, 65), "TuringTec Agent Studio", font=f_b, fill=(241, 245, 249))

    btxt = badge[:44]
    bb = draw.textbbox((0, 0), btxt, font=f_bg)
    bw = (bb[2] - bb[0]) + 32
    bx = max(480, W - 68 - bw)
    draw.rounded_rectangle([bx, 58, bx + bw, 102], radius=22, fill=(18, 26, 44), outline=accent, width=2)
    draw.text((bx + 16, 69), btxt, font=f_bg, fill=(191, 219, 254))

    y_cur = 165
    for line in textwrap.wrap(title, width=36)[:3]:
        draw.text((68, y_cur), line, font=f_t, fill=(248, 250, 252))
        y_cur += 62
    y_cur += 14
    for line in textwrap.wrap(subtitle, width=74)[:2]:
        draw.text((68, y_cur), line, font=f_s, fill=(148, 163, 184))
        y_cur += 35

    draw.line([(68, 542), (W - 68, 542)], fill=(30, 41, 59), width=2)
    foot_l = "gabhack.github.io/turingtec-agent-studio/es/" if lang == "es" else "gabhack.github.io/turingtec-agent-studio/"
    foot_r = "Agentes IA Self-Hosted · MCP · FinOps" if lang == "es" else "Self-Hosted AI Agents · MCP · FinOps"
    draw.text((68, 562), foot_l, font=f_s, fill=(96, 165, 250))
    draw.text((W - 460, 562), foot_r, font=f_s, fill=(148, 163, 184))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)


SOLUTIONS = [
    {
        "slug": "clinic-whatsapp-voice-agent",
        "accent": (16, 185, 129),
        "en": {
            "badge": "Clinics · 24/7 WhatsApp & Voice",
            "title": "24/7 AI WhatsApp & Voice Receptionist for Clinics (Anti-No-Show + Calendar Sync)",
            "short_title": "Clinic WhatsApp & Voice Receptionist",
            "meta_desc": "Deploy a self-hosted 24/7 WhatsApp & Voice AI receptionist for medical and dental clinics. Automates intake, Google Calendar booking & 24h/2h anti-no-show reminders with zero SaaS lock-in.",
            "price_kit": "$39 n8n Pack / $99 Business-in-a-Box",
            "price_pilot": "$690 7-Day Turnkey Pilot",
            "intro": "Stop losing after-hours patients and paying staff to chase confirmations. ClinicFlow AI answers WhatsApp chats and voice inquiries in under 2 seconds, checks real-time calendar availability, and triggers 24h/2h anti-no-show reminders on your own BYOK stack.",
            "card_desc": "Answers patient WhatsApp & voice inquiries 24/7, checks live slots, and cuts empty chairs with 24h/2h automated confirmations.",
            "rows": [
                ("Channels", "Official Meta WhatsApp Cloud API + optional ElevenLabs / Vapi Voice"),
                ("Live Scheduling", "Real-time Google Calendar / EMR slot lookup, booking & rescheduling"),
                ("Anti-No-Show Engine", "Automated 24h & 2h 1-tap Confirm / Reschedule + waitlist refill"),
                ("Clinical Safety", "Immediate warm hand-off to human receptionists via Chatwoot or alerts"),
                ("Ownership", "100% self-hosted Docker n8n + BYOK (~$0.004/WhatsApp window, $0/seat)"),
            ],
            "faqs": [
                ("Does ClinicFlow charge per-seat SaaS fees every month?", "No. You own the n8n workflow and run it on your own Docker host with Meta's official WhatsApp Cloud API—zero per-agent seat markups."),
                ("What happens if a patient reports a medical urgency?", "Deterministic escalation rules immediately pause the bot and notify your on-duty staff via Chatwoot or WhatsApp alert."),
            ],
        },
        "es": {
            "badge": "Clínicas · WhatsApp y Voz 24/7",
            "title": "Recepcionista IA 24/7 por WhatsApp y Voz para Clínicas (Citas + Anti-Inasistencias)",
            "short_title": "Recepcionista IA WhatsApp para Clínicas",
            "meta_desc": "Implementa una recepcionista IA 24/7 en WhatsApp y Voz para clínicas médicas y odontológicas. Agenda citas en tiempo real y reduce inasistencias con recordatorios automáticos 24h/2h sin rentas SaaS.",
            "price_kit": "$39 Pack n8n / $99 Business-in-a-Box",
            "price_pilot": "$690 Piloto Llave en Mano (7 días)",
            "intro": "Deja de perder pacientes fuera de horario y horas de recepción persiguiendo confirmaciones. ClinicFlow AI responde WhatsApp en menos de 2 segundos, consulta cupos reales en agenda y envía recordatorios automáticos 24h y 2h antes sobre tu propia infraestructura.",
            "card_desc": "Atiende pacientes 24/7 por WhatsApp y voz, agenda directo en Google Calendar y recorta ausencias con confirmaciones automáticas.",
            "rows": [
                ("Canales", "Meta WhatsApp Cloud API oficial + Voz natural opcional (ElevenLabs / Vapi)"),
                ("Agenda en Vivo", "Consulta de cupos, reserva, reprogramación y recepción de carné de seguro"),
                ("Motor Anti-No-Show", "Confirmación automática 24h y 2h antes + llenado automático desde lista de espera"),
                ("Seguridad Clínica", "Escalamiento inmediato a tu recepción humana por Chatwoot ante urgencias"),
                ("Propiedad Total", "100% self-hosted en Docker n8n + BYOK (~$0.004/ventana WhatsApp, $0/asiento)"),
            ],
            "faqs": [
                ("¿Tengo que pagar mensualidades por cada recepcionista o sede?", "No. Eres dueño del flujo n8n y lo corres en tu propio servidor Docker conectado a la API oficial de WhatsApp Business sin rentas por asiento."),
                ("¿Qué pasa si un paciente reporta una urgencia médica?", "Las reglas de seguridad detectan síntomas de alerta, pausan la automatización y transfieren de inmediato el caso a tu equipo humano."),
            ],
        },
    },
    {
        "slug": "hardware-b2b-quoting-agent",
        "accent": (37, 99, 235),
        "en": {
            "badge": "Wholesale & Hardware · B2B RFQ Quoter",
            "title": "FerreQuote AI: Instant B2B Hardware & Wholesale RFQ Quoting Agent (WhatsApp to SKU)",
            "short_title": "B2B Hardware & Wholesale RFQ Quoter",
            "meta_desc": "Turn messy WhatsApp and email material lists into accurate SKU quotes with tiered volume discounts and margin protection in 45 seconds. Self-hosted n8n + Python agent.",
            "price_kit": "$39 n8n Pack / $99 Business-in-a-Box",
            "price_pilot": "$690 7-Day Turnkey Pilot",
            "intro": "Distributors lose high-margin orders when manual quoting takes 3 to 4 hours. FerreQuote AI parses messy WhatsApp material lists, fuzzy-matches against your SKU catalog, applies volume discounts safely, and outputs a ready-to-close CSV/PDF quote in under a minute.",
            "card_desc": "Reads unstructured WhatsApp/email material lists, matches SKUs & tier pricing, protects floor margins, and exports quotes in seconds.",
            "rows": [
                ("Unstructured Inputs", "Messy WhatsApp messages, emails, CSV & Excel bills of materials"),
                ("SKU Resolution", "Fuzzy synonym matching + unit normalization + confidence flagging"),
                ("Margin Guardrails", "Enforces volume discount brackets and minimum floor margins automatically"),
                ("ERP / Export", "Clean JSON & CSV ready for SAP, NetSuite, Odoo, Siigo, Alegra, or Sheets"),
                ("Deployment", "$39 Self-Host n8n Pack · $99 Business-in-a-Box · $690 7-Day Pilot"),
            ],
            "faqs": [
                ("How does it handle typos and local trade abbreviations?", "It combines normalized synonym dictionaries with low-cost LLM extraction (BYOK) and routes low-confidence lines to 1-click sales confirmation."),
                ("Can I test it with a real bill of materials right now?", "Yes—open our live zero-signup sandbox on the main page and paste any hardware or industrial material list."),
            ],
        },
        "es": {
            "badge": "Ferreterías y Mayoristas · Cotizador B2B",
            "title": "FerreQuote AI: Cotizador B2B Automático por WhatsApp para Ferreterías y Distribuidores",
            "short_title": "Cotizador B2B Ferretero por WhatsApp",
            "meta_desc": "Convierte listas desordenadas de obra por WhatsApp o correo en cotizaciones exactas con SKU, descuentos por volumen y control de margen en 45 segundos.",
            "price_kit": "$39 Pack n8n / $99 Business-in-a-Box",
            "price_pilot": "$690 Piloto Llave en Mano (7 días)",
            "intro": "Los mayoristas pierden pedidos grandes cuando cotizar manualmente toma 3 o 4 horas. FerreQuote AI interpreta listas sucias de WhatsApp o Excel, cruza contra tu catálogo real de SKUs, aplica descuentos por volumen sin regalar margen y entrega la cotización en segundos.",
            "card_desc": "Interpreta listas de materiales por WhatsApp, cruza SKU y descuentos por volumen y genera la cotización lista para cerrar venta.",
            "rows": [
                ("Entradas Reales", "Mensajes de WhatsApp sin formato, correos y listados de obra en Excel/CSV"),
                ("Cruce de SKUs", "Matching difuso de sinónimos + normalización de unidades y alertas de duda"),
                ("Control de Margen", "Aplica escalas de descuento por volumen respetando siempre tu piso de utilidad"),
                ("Salida ERP / Excel", "Exporta JSON y CSV listos para Siigo, Alegra, Odoo, SAP o Google Sheets"),
                ("Despliegue", "$39 Pack n8n Self-Host · $99 Business-in-a-Box · $690 Piloto 7 días"),
            ],
            "faqs": [
                ("¿Cómo maneja abreviaturas de obra y errores de ortografía?", "Combina tablas de sinónimos del catálogo con extracción IA económica (BYOK) y marca líneas ambiguas para revisión humana de 1 clic."),
                ("¿Puedo probarlo hoy mismo con una lista real?", "Sí: entra al sandbox interactivo en nuestra portada sin registrarte y pega cualquier lista ferretera o industrial."),
            ],
        },
    },
    {
        "slug": "invoice-pdf-extraction-agent",
        "accent": (99, 102, 241),
        "en": {
            "badge": "Finance & Back-Office · PDF-to-ERP",
            "title": "DocFlow B2B: Automated Invoice & Purchase Order PDF-to-ERP Extraction Agent",
            "short_title": "Invoice & PO PDF-to-ERP Extractor",
            "meta_desc": "Extract vendor details, Tax IDs/NIT, line items, taxes, and math-validated totals from B2B PDF invoices into clean ERP JSON or Excel with confidence scoring.",
            "price_kit": "$39 n8n Pack / $99 Business-in-a-Box",
            "price_pilot": "$690 7-Day Turnkey Pilot",
            "intro": "Stop burning 40+ accounting hours every month retyping supplier PDFs. DocFlow B2B reads multi-page invoices and purchase orders without brittle templates, verifies subtotal and tax arithmetic deterministically, and posts verified records straight into your ERP.",
            "card_desc": "Parses supplier PDFs & POs without rigid templates, validates subtotal/tax math automatically, and flags discrepancies before ERP entry.",
            "rows": [
                ("Extracted Schema", "Vendor, Tax ID/NIT, Invoice #, Date, Line Items, Tax/VAT, Grand Total"),
                ("Deterministic Math Check", "Recomputes line subtotals & taxes independently to catch vendor errors"),
                ("Exception Queue", "Only mismatched totals or low-confidence scans route to human approval"),
                ("Integrations", "Strict JSON webhook to SAP, NetSuite, Odoo, Siigo, Alegra, or Google Sheets"),
                ("Unit Economics", "~$0.001–$0.003 per invoice in raw BYOK LLM tokens ($0 SaaS per-doc markup)"),
            ],
            "faqs": [
                ("Do I pay per-document SaaS markups forever?", "No. With our $39 n8n Pack or $99 Business-in-a-Box, you host the agent yourself and pay only raw API tokens (~$1 per 500 invoices)."),
                ("Can it detect supplier math or tax mismatches automatically?", "Yes—every extracted invoice passes through a deterministic arithmetic verifier before entering your accounting system."),
            ],
        },
        "es": {
            "badge": "Contabilidad y Finanzas · PDF a ERP",
            "title": "DocFlow B2B: Agente Extractor de Facturas PDF y Órdenes de Compra hacia tu ERP",
            "short_title": "Extractor de Facturas PDF a ERP",
            "meta_desc": "Extrae proveedor, NIT, ítems, IVA y totales validados matemáticamente desde facturas PDF y órdenes de compra directo a tu ERP o Excel sin digitación manual.",
            "price_kit": "$39 Pack n8n / $99 Business-in-a-Box",
            "price_pilot": "$690 Piloto Llave en Mano (7 días)",
            "intro": "Deja de gastar más de 40 horas contables al mes digitando facturas de proveedores. DocFlow B2B lee facturas PDF y órdenes de compra sin plantillas rígidas, valida sumas e IVA de forma determinística y envía registros limpios directo a tu ERP.",
            "card_desc": "Lee facturas PDF sin plantillas rígidas, verifica sumas e IVA automáticamente y alerta discrepancias antes de causar en tu ERP.",
            "rows": [
                ("Campos Extraídos", "Proveedor, NIT/RUT, N.º Factura, Fecha, Líneas de Ítem, IVA y Total"),
                ("Validación Matemática", "Recalcula subtotales e impuestos para detectar sobrecostos o errores de factura"),
                ("Cola de Excepciones", "Solo facturas con descuadre o baja confianza pasan a revisión humana"),
                ("Integraciones", "Webhook JSON estricto hacia Siigo, Alegra, Odoo, SAP, NetSuite o Google Sheets"),
                ("Costo por Factura", "~$0.001–$0.003 USD en tokens BYOK (cero cobros abusivos por documento)"),
            ],
            "faqs": [
                ("¿Debo pagar comisiones por cada documento procesado?", "No. Con el Pack n8n ($39) o Business-in-a-Box ($99) ejecutas el agente en tu infraestructura pagando solo tokens directos (~$1 por cada 500 facturas)."),
                ("¿Detecta descuadres de IVA o totales errados del proveedor?", "Sí: cada factura extraída pasa por un validador aritmético determinístico antes de llegar a contabilidad."),
            ],
        },
    },
    {
        "slug": "aws-finops-guardrails-mcp",
        "accent": (245, 158, 11),
        "en": {
            "badge": "Cloud FinOps · Open-Core CLI + MCP",
            "title": "AWS FinOps & LLM Token Guard: Open-Core CLI + stdio MCP Server with Terraform Auto-Fix",
            "short_title": "AWS FinOps & LLM Guardrails MCP",
            "meta_desc": "Audit AWS EBS, NAT Gateways, EIPs, idle RDS, and Bedrock/OpenAI/Gemini token waste locally via CLI or Claude/Cursor MCP Server. Unlock Terraform HCL fixes & CI/CD SARIF.",
            "price_kit": "$0 Open-Core / $49 Pro License",
            "price_pilot": "$299 48-Hour FinOps Audit",
            "intro": "Eliminate 25–60% of silent cloud and AI token waste without handing IAM credentials to third-party SaaS dashboards. Run aws-finops-guard locally in your terminal or directly inside Claude Desktop and Cursor via MCP stdio.",
            "card_desc": "Finds idle EBS, NAT Gateways, oversized RDS, and overpaying LLM prompts locally via CLI or Claude/Cursor MCP—with Terraform fixes.",
            "rows": [
                ("AWS Waste Rules", "Unattached EBS, gp2→gp3, idle NAT Gateways, $0 S3 Gateway Endpoints, EIPs, RDS"),
                ("LLM Token FinOps", "Catches triage/extraction agents burning frontier models + missing prompt caching"),
                ("Native MCP stdio", "Zero-dependency JSON-RPC 2.0 server for Claude Desktop, Cursor & VS Code"),
                ("Pro License ($49)", "Safe Terraform HCL remediation patches, AWS CLI commands & CI/CD SARIF 2.1.0"),
                ("Open-Core Repo", "MIT licensed on GitHub (github.com/gabhack/aws-finops-guard)"),
            ],
            "faqs": [
                ("Does aws-finops-guard ever upload my AWS credentials?", "Never. Every audit runs 100% locally against your JSON resource snapshots with zero cloud telemetry."),
                ("How fast does the $49 Pro License pay for itself?", "Removing a single idle NAT Gateway ($32.85/mo) or switching one triage agent to a fast model recovers $49 in days."),
            ],
        },
        "es": {
            "badge": "FinOps AWS · CLI Open-Core + MCP",
            "title": "AWS FinOps & LLM Token Guard: CLI Open-Core + Servidor MCP con Parches Terraform",
            "short_title": "Auditor FinOps AWS y Tokens LLM (MCP)",
            "meta_desc": "Audita desperdicio en AWS (EBS, NAT Gateways, EIPs, RDS ocioso) y tokens Bedrock/OpenAI/Gemini en local por CLI o MCP en Claude/Cursor con parches Terraform automáticos.",
            "price_kit": "$0 Open-Core / $49 Licencia Pro",
            "price_pilot": "$299 Auditoría FinOps en 48h",
            "intro": "Recorta entre 25% y 60% de gasto silencioso en AWS y APIs de IA sin entregar llaves IAM a plataformas SaaS externas. Corre aws-finops-guard en tu terminal o desde Claude Desktop y Cursor vía MCP stdio.",
            "card_desc": "Detecta EBS huérfanos, NAT Gateways costosos, RDS sobredimensionados y desperdicio en tokens LLM desde tu terminal o Claude/Cursor.",
            "rows": [
                ("Reglas Cloud AWS", "EBS sin adjuntar, gp2→gp3, NAT ociosos, S3 Gateway Endpoints $0, EIPs y RDS"),
                ("FinOps de Tokens IA", "Detecta agentes de clasificación pagando modelos caros y falta de prompt caching"),
                ("Servidor MCP Nativo", "JSON-RPC 2.0 stdio sin dependencias para Claude Desktop, Cursor y VS Code"),
                ("Licencia Pro ($49)", "Parches seguros en Terraform HCL, comandos AWS CLI y salida SARIF 2.1.0 para CI/CD"),
                ("Repositorio Abierto", "Licencia MIT en GitHub (github.com/gabhack/aws-finops-guard)"),
            ],
            "faqs": [
                ("¿La herramienta sube mis credenciales o datos de AWS a la nube?", "Nunca. Toda la auditoría corre 100% en tu máquina sobre snapshots JSON locales sin enviar telemetría a terceros."),
                ("¿En cuánto tiempo se paga la licencia Pro de $49?", "Con eliminar un solo NAT Gateway ocioso ($32.85/mes) o ajustar un agente de triaje a modelo Flash recuperas la inversión en días."),
            ],
        },
    },
    {
        "slug": "n8n-ai-agent-workflows-pack",
        "accent": (14, 165, 233),
        "en": {
            "badge": "15 Importable JSONs + Docker Stack",
            "title": "15 Production n8n AI Agent Workflows Pack (Clinics, B2B RFQ, Invoices, FinOps & MCP)",
            "short_title": "15 Production n8n AI Agent Workflows",
            "meta_desc": "Skip broken 4,000-file dumps. Download 15 clean, BYOK n8n AI Agent JSON workflows + 1-command Docker Compose self-host stack for $39 one-time.",
            "price_kit": "$39 Standard / $79 Agency",
            "price_pilot": "$99 All-Access Business-in-a-Box",
            "intro": "Stop debugging broken template dumps. Get 15 clean, environment-variable-driven n8n v1 AI Agent workflows covering clinic bookings, B2B quoting, invoice extraction, Gumroad onboarding, AWS FinOps alerts, and an MCP HTTP bridge—plus 1-command Docker Compose.",
            "card_desc": "15 clean, tested BYOK n8n JSON workflows + 1-command Docker self-host stack ($0 software fees) for B2B ops and agencies.",
            "rows": [
                ("15 Curated Workflows", "Clinics, B2B RFQ, Invoice PDF, FinOps Guard, LLM Router, Chatwoot, MCP Bridge"),
                ("Zero-Cost Self-Hosting", "Includes docker-compose.yml + .env.example to launch in under 60 seconds"),
                ("Provider Agnostic", "Works with OpenAI, OpenRouter, Gemini OpenAI-compatible API, or Ollama"),
                ("Production Hygiene", "Zero hardcoded secrets; indexed catalog/index.json + full setup guide"),
                ("One-Time Pricing", "$39 Personal/Internal · $79 Agency Unlimited Client Deployments"),
            ],
            "faqs": [
                ("Do I need a paid n8n Cloud subscription?", "No. The included docker-compose.yml runs n8n self-hosted at $0 software licensing cost on your laptop or a ~$15/mo VPS."),
                ("Why 15 curated workflows instead of 4,000 scraped files?", "Massive scraped dumps are full of deprecated nodes and broken auth. These 15 workflows follow a clean uniform BYOK schema built for real B2B ops."),
            ],
        },
        "es": {
            "badge": "15 Flujos JSON + Docker Self-Host",
            "title": "Pack de 15 Workflows n8n de Agentes IA en Producción (Clínicas, B2B, Facturas y MCP)",
            "short_title": "Pack 15 Workflows n8n de Agentes IA",
            "meta_desc": "Olvida packs rotos de 4,000 archivos. Descarga 15 workflows n8n de Agentes IA limpios y probados + Docker Compose self-hosted por $39 pago único.",
            "price_kit": "$39 Estándar / $79 Agencia",
            "price_pilot": "$99 Business-in-a-Box Completo",
            "intro": "Deja de perder horas arreglando plantillas viejas. Recibe 15 workflows n8n v1 limpios con variables de entorno para clínicas WhatsApp, cotizador B2B, facturas PDF, onboarding Gumroad, alertas FinOps AWS y puente MCP—junto con Docker Compose en 1 comando.",
            "card_desc": "15 flujos JSON n8n listos para importar + Docker Compose ($0 licencia software) para lanzar automatizaciones B2B hoy mismo.",
            "rows": [
                ("15 Flujos Curados", "Clínicas, Cotizador B2B, Facturas PDF, FinOps AWS, Router LLM, Chatwoot y MCP"),
                ("Self-Host a Costo $0", "Incluye docker-compose.yml + .env.example para levantar en menos de 60 segundos"),
                ("Multi-Modelo BYOK", "Compatible con OpenAI, OpenRouter, Gemini API o modelos locales Ollama"),
                ("Higiene de Producción", "Cero llaves quemadas; índice catalog/index.json y guía completa paso a paso"),
                ("Pago Único", "$39 uso interno · $79 licencia comercial para agencias"),
            ],
            "faqs": [
                ("¿Necesito pagar suscripción mensual de n8n Cloud?", "No. El archivo docker-compose.yml incluido levanta n8n self-hosted con $0 de licencia en tu computador o un VPS económico."),
                ("¿Por qué 15 flujos curados en vez de 4,000 archivos reciclados?", "Los megapacks masivos traen nodos obsoletos que fallan al importar. Estos 15 flujos usan un esquema limpio v1 listo para negocio real."),
            ],
        },
    },
    {
        "slug": "mcp-agent-business-in-a-box",
        "accent": (79, 70, 229),
        "en": {
            "badge": "Flagship All-Access · Save 60%",
            "title": "TuringTec AI Agent Business-in-a-Box: 15 n8n Workflows + 4 MCP Servers + 12 Skills",
            "short_title": "AI Agent Business-in-a-Box ($99)",
            "meta_desc": "Launch or white-label B2B AI agents immediately: 15 n8n workflows, 4 production MCP servers, 12 Claude/Cursor/Codex Agent Skills & commercial deployment rights for $99 once.",
            "price_kit": "$99 One-Time (Value $245+)",
            "price_pilot": "Includes Commercial White-Label Rights",
            "intro": "The complete production toolkit for developers, consultants, and agencies building recurring B2B AI agent businesses. Unlock every n8n workflow, all 4 MCP servers, 12 cross-platform SKILL.md modules, and unlimited client deployment rights for one $99 payment.",
            "card_desc": "Everything in one vault: 15 n8n workflows, 4 MCP servers, 12 cross-platform Agent Skills & commercial white-label client rights.",
            "rows": [
                ("Module 1", "15 Production n8n AI Agent Workflows + 1-Command Docker Self-Host"),
                ("Module 2", "aws-finops-guard Full Source + Terraform HCL Auto-Fix & SARIF Engine"),
                ("Module 3", "3 Apify Dual-Mode Standby + Pay-Per-Event v2 MCP Servers"),
                ("Module 4", "12 Cross-Platform SKILL.md Modules (Claude Code, Cursor, Codex, Antigravity)"),
                ("Commercial License", "Deploy & white-label for unlimited paying clients (no raw ZIP resale)"),
            ],
            "faqs": [
                ("Is this a monthly subscription?", "No—pay $99 USD once via Gumroad and keep full source code and commercial deployment rights permanently."),
                ("Can I deploy these agents for paying $500–$1,500 B2B clients?", "Yes. The commercial white-label license is designed specifically for consultants and agencies delivering client projects."),
            ],
        },
        "es": {
            "badge": "Bóveda Completa · Ahorra 60%",
            "title": "TuringTec AI Agent Business-in-a-Box: 15 Flujos n8n + 4 MCP Servers + 12 Agent Skills",
            "short_title": "AI Agent Business-in-a-Box ($99)",
            "meta_desc": "Lanza o vende agentes IA B2B en marca blanca desde hoy: 15 workflows n8n, 4 servidores MCP en producción, 12 Agent Skills y licencia comercial ilimitada por $99 pago único.",
            "price_kit": "$99 Pago Único (Valor $245+)",
            "price_pilot": "Incluye Licencia Comercial White-Label",
            "intro": "La bóveda de ingeniería completa para desarrolladores, consultores y agencias que quieren vender agentes IA B2B sin arrancar desde cero. Desbloquea los 15 workflows n8n, 4 servidores MCP, 12 Agent Skills multi-IDE y derechos comerciales para clientes ilimitados.",
            "card_desc": "Todo en un solo paquete: 15 flujos n8n, 4 servidores MCP, 12 Agent Skills y licencia comercial para desplegar a clientes ilimitados.",
            "rows": [
                ("Módulo 1", "15 Workflows n8n de Agentes IA en Producción + Docker Compose Self-Host"),
                ("Módulo 2", "Código completo aws-finops-guard + parches Terraform HCL y motor SARIF"),
                ("Módulo 3", "3 Servidores MCP Dual-Mode Apify Standby + Pay-Per-Event v2"),
                ("Módulo 4", "12 Módulos SKILL.md compatibles con Claude Code, Cursor, Codex y Antigravity"),
                ("Licencia Comercial", "Despliega en marca blanca para clientes ilimitados (no reventa del ZIP crudo)"),
            ],
            "faqs": [
                ("¿Es una suscripción mensual?", "No: pagas $99 USD una sola vez vía Gumroad y te quedas para siempre con el código fuente y la licencia de despliegue a clientes."),
                ("¿Puedo usar estos kits para cobrar setups B2B de $500 a $1,500 a clientes?", "Sí: la licencia comercial white-label está pensada exactamente para consultores y agencias."),
            ],
        },
    },
]


COMPARES = [
    {
        "slug": "n8n-vs-zapier-vs-make-calculator",
        "accent": (14, 165, 233),
        "en": {
            "badge": "ROI Calculator · n8n vs Zapier vs Make",
            "title": "n8n vs Zapier vs Make Pricing Calculator (2026–2027): Real Self-Hosted Savings",
            "short_title": "n8n vs Zapier vs Make Cost Calculator",
            "meta_desc": "Calculate your exact annual automation bill across Zapier, Make, and self-hosted Docker n8n ($0 software / ~$15/mo VPS). Slide monthly runs and steps to see USD/year saved.",
            "bluf": "At 10,000 monthly workflow runs averaging 6 steps (60,000 tasks/month), Zapier costs ~$5,748/year and Make costs ~$1,284/year—while self-hosted Docker n8n runs for ~$180/year (~$15/mo VPS, $0 software fee), saving up to $5,568/year.",
            "intro": "Per-task SaaS automation pricing punishes AI agents that run multi-step loops, webhooks, and LLM retries. Model your real monthly volume below.",
            "table_headers": ["Platform", "Billing Model", "60k Tasks / Mo Est.", "Self-Host Control", "Best For"],
            "table_rows": [
                ("Self-Hosted n8n (Docker)", "$0 Software + ~$15/mo VPS", "$15 / mo ($180 / yr)", "100% Own Server & Keys", "AI Agents, High-Volume B2B, Agencies"),
                ("Make (Integromat)", "Per Operation (~$1.60 / 1k)", "~$107 / mo ($1,284 / yr)", "Cloud SaaS Only", "Visual Mid-Volume Integrations"),
                ("Zapier (Pro / Team)", "Per Task (~$7.50 / 1k)", "~$479 / mo ($5,748 / yr)", "Cloud SaaS Only", "Low-Volume Simple Triggers"),
            ],
            "faqs": [
                ("Is self-hosted n8n really $0 in software fees?", "Yes—running the official Docker image for internal business operations costs $0 in software licensing; you only pay for a small ~$15/mo VPS."),
                ("Why do AI agents get so expensive on Zapier and Make?", "Every LLM call, JSON parse, router branch, and retry counts as a separate billable task."),
            ],
            "calc_title": "Interactive Annual Automation Cost Calculator",
            "lbl_runs": "Monthly Workflow Runs",
            "lbl_steps": "Average Steps per Workflow",
            "lbl_ops": "Monthly Billable Operations",
            "lbl_save_head": "Estimated Annual Savings with Self-Hosted n8n",
            "cta_box": "All-Access Business-in-a-Box ($99)",
        },
        "es": {
            "badge": "Calculadora ROI · n8n vs Zapier vs Make",
            "title": "Calculadora de Costos n8n vs Zapier vs Make (2026–2027): Ahorro Real Self-Hosted",
            "short_title": "Calculadora n8n vs Zapier vs Make",
            "meta_desc": "Calcula tu factura anual exacta comparando Zapier, Make y n8n self-hosted en Docker ($0 licencia / ~$15/mes VPS). Ajusta ejecuciones y pasos para ver tu ahorro anual en USD.",
            "bluf": "Con 10,000 ejecuciones mensuales de 6 pasos (60,000 tareas/mes), Zapier cuesta ~$5,748/año y Make ~$1,284/año—mientras que n8n self-hosted en Docker corre por ~$180/año (~$15/mes VPS, $0 licencia), ahorrando hasta $5,568/año.",
            "intro": "Los cobros por tarea castigan duramente a los agentes IA que hacen ciclos, webhooks y reintentos. Ajusta tu volumen real abajo para ver el ahorro exacto.",
            "table_headers": ["Plataforma", "Modelo de Cobro", "Est. 60k Tareas/Mes", "Control Self-Host", "Ideal Para"],
            "table_rows": [
                ("n8n Self-Hosted (Docker)", "$0 Licencia + ~$15/mes VPS", "$15 / mes ($180 / año)", "100% Servidor y Llaves Propias", "Agentes IA, B2B Alto Volumen, Agencias"),
                ("Make (Integromat)", "Por Operación (~$1.60 / 1k)", "~$107 / mes ($1,284 / año)", "Solo SaaS en Nube", "Integraciones Visuales Medianas"),
                ("Zapier (Pro / Team)", "Por Tarea (~$7.50 / 1k)", "~$479 / mes ($5,748 / año)", "Solo SaaS en Nube", "Disparadores Simples Bajo Volumen"),
            ],
            "faqs": [
                ("¿De verdad n8n self-hosted cuesta $0 en licencia de software?", "Sí: correr la imagen oficial de Docker para operación interna tiene $0 de licencia; solo pagas tu VPS (~$15/mes)."),
                ("¿Por qué salen tan caros los agentes IA en Zapier y Make?", "Cada llamada LLM, parseo JSON, validación y reintento cuenta como una tarea facturable adicional."),
            ],
            "calc_title": "Calculadora Interactiva de Gasto Anual en Automatización",
            "lbl_runs": "Ejecuciones Mensuales de Flujos",
            "lbl_steps": "Pasos Promedio por Flujo",
            "lbl_ops": "Operaciones Facturables al Mes",
            "lbl_save_head": "Ahorro Anual Estimado con n8n Self-Hosted",
            "cta_box": "Bóveda Business-in-a-Box ($99)",
        },
    },
    {
        "slug": "aws-finops-open-source-tools",
        "accent": (245, 158, 11),
        "en": {
            "badge": "Cloud & LLM FinOps Benchmark",
            "title": "AWS FinOps Open-Source Tools Compared (2026–2027): aws-finops-guard vs Infracost vs OpenCost",
            "short_title": "AWS FinOps Tools + Waste Estimator",
            "meta_desc": "Compare aws-finops-guard, Infracost, OpenCost, and AWS Cost Explorer—plus an interactive AWS & LLM Monthly Waste Estimator showing payback in hours.",
            "bluf": "Infracost estimates pre-deploy Terraform PR diffs and OpenCost tracks Kubernetes pods, while aws-finops-guard audits live AWS + LLM token waste locally via CLI or Claude/Cursor MCP Server and outputs safe Terraform HCL fixes.",
            "intro": "Cloud teams routinely leak 25–40% of spend across idle NAT Gateways, legacy gp2 storage, oversized non-prod RDS, and overpaying LLM prompts. Compare the tools and model your recoverable budget below.",
            "table_headers": ["Tool", "Primary Scope", "Live AWS + LLM Audit", "MCP Server", "Terraform Auto-Fix", "License"],
            "table_rows": [
                ("aws-finops-guard", "Live AWS Waste + LLM Routing", "✓ Yes (EBS, NAT, RDS, LLMs)", "✓ Native stdio MCP", "✓ Pro ($49) + SARIF", "MIT ($0) / $49 Pro"),
                ("Infracost", "Pre-Deploy Terraform PR Diffs", "Pre-deploy IaC only", "✗ No", "✗ Estimates only", "Apache 2.0 / SaaS"),
                ("OpenCost", "Kubernetes Pod Costing", "K8s clusters only", "✗ No", "✗ Reporting only", "CNCF Apache 2.0"),
                ("AWS Cost Explorer", "Historical Billing Console", "AWS billing only", "✗ No", "✗ Manual changes", "Free UI / $0.01 API"),
            ],
            "faqs": [
                ("How is aws-finops-guard different from Infracost and OpenCost?", "Infracost focuses on Terraform PR estimates and OpenCost on Kubernetes; aws-finops-guard audits both live AWS waste AND LLM token routing locally or inside Claude/Cursor via MCP."),
                ("What does the $49 Pro License unlock?", "Copy-paste Terraform HCL remediation patches, AWS CLI commands, and CI/CD SARIF 2.1.0 gates."),
            ],
            "calc_title": "Interactive AWS + LLM Waste & Payback Estimator",
            "lbl_aws": "Monthly AWS Spend (USD)",
            "lbl_pct": "Est. Idle / Oversized AWS Waste (%)",
            "lbl_llm": "Monthly LLM API Spend (OpenAI / Bedrock / Gemini)",
            "lbl_rec": "Recoverable Cloud + AI Budget",
        },
        "es": {
            "badge": "Comparativa FinOps AWS y Tokens LLM",
            "title": "Herramientas Open-Source FinOps AWS (2026–2027): aws-finops-guard vs Infracost vs OpenCost",
            "short_title": "Comparativa FinOps AWS + Calculadora",
            "meta_desc": "Compara aws-finops-guard, Infracost, OpenCost y AWS Cost Explorer con calculadora interactiva de desperdicio AWS + LLM y retorno en horas.",
            "bluf": "Infracost estima costos en PRs de Terraform y OpenCost mide pods Kubernetes, mientras que aws-finops-guard audita desperdicio real de AWS y tokens LLM en local por CLI o MCP (Claude/Cursor) generando parches Terraform listos.",
            "intro": "Los equipos cloud suelen desperdiciar entre 25% y 40% en NAT Gateways ociosos, volúmenes gp2, RDS sobredimensionado y prompts en modelos caros. Estima tu presupuesto recuperable abajo.",
            "table_headers": ["Herramienta", "Alcance Principal", "Auditoría AWS + LLM", "Servidor MCP", "Auto-Fix Terraform", "Licencia"],
            "table_rows": [
                ("aws-finops-guard", "Desperdicio AWS + Enrutado LLM", "✓ Sí (EBS, NAT, RDS, LLMs)", "✓ MCP stdio nativo", "✓ Pro ($49) + SARIF", "MIT ($0) / $49 Pro"),
                ("Infracost", "Diff de costo pre-despliegue PR", "Solo IaC pre-despliegue", "✗ No", "✗ Solo estimado", "Apache 2.0 / SaaS"),
                ("OpenCost", "Costos de pods Kubernetes", "Solo clusters K8s", "✗ No", "✗ Solo reportes", "CNCF Apache 2.0"),
                ("AWS Cost Explorer", "Consola histórica de factura", "Solo factura AWS", "✗ No", "✗ Cambios manuales", "UI Gratis / $0.01 API"),
            ],
            "faqs": [
                ("¿En qué se diferencia aws-finops-guard de Infracost y OpenCost?", "Infracost estima cambios en PRs y OpenCost mide Kubernetes; aws-finops-guard audita desperdicio real AWS más sobrepago de tokens IA directamente desde terminal o Claude/Cursor vía MCP."),
                ("¿Qué desbloquea la Licencia Pro de $49?", "Parches seguros en Terraform HCL, comandos AWS CLI listos y reportes SARIF 2.1.0 para bloquear despliegues costosos en CI/CD."),
            ],
            "calc_title": "Calculadora Interactiva de Desperdicio AWS + LLM",
            "lbl_aws": "Gasto Mensual en AWS (USD)",
            "lbl_pct": "Desperdicio Estimado en Recursos Ociosos (%)",
            "lbl_llm": "Gasto Mensual en APIs LLM (OpenAI / Bedrock / Gemini)",
            "lbl_rec": "Presupuesto Recuperable Cloud + IA",
        },
    },
    {
        "slug": "clinic-whatsapp-ai-bot-roi",
        "accent": (16, 185, 129),
        "en": {
            "badge": "Healthcare ROI · Anti-No-Show WhatsApp AI",
            "title": "Clinic WhatsApp AI Bot & Anti-No-Show ROI Calculator (2026–2027)",
            "short_title": "Clinic WhatsApp AI ROI Calculator",
            "meta_desc": "Calculate how much monthly and annual revenue your medical, dental, or aesthetic clinic recovers with a 24/7 self-hosted WhatsApp booking & 24h/2h anti-no-show AI receptionist.",
            "bluf": "A clinic handling 300 monthly WhatsApp inquiries with a 22% no-show/missed-lead rate at $75/visit loses ~$4,950/month. Recovering 65% via 24/7 booking and 24h/2h reminders adds ~$3,225/month ($38,700/year)—paying back a $690 pilot in under 7 days.",
            "intro": "Patients message after hours and forget appointments without timely WhatsApp reminders. Model your clinic's exact monthly recovered revenue below.",
            "table_headers": ["Stage", "Manual Front Desk", "ClinicFlow AI (Self-Hosted)", "Impact"],
            "table_rows": [
                ("After-Hours Chats (7pm–8am)", "Unanswered until morning", "Instant 24/7 WhatsApp triage + live booking", "+35–50% booking capture"),
                ("24h & 2h Reminders", "Manual calls or forgotten SMS", "Automated 1-tap Confirm / Reschedule", "Up to 65% fewer no-shows"),
                ("Cancellations", "Chair stays empty", "Auto-notifies waitlist patients", "Higher daily utilization"),
                ("Monthly Software Cost", "$299–$599/mo SaaS seats", "$0 Docker n8n + ~$0.004/WhatsApp window", "Zero per-seat SaaS lock-in"),
            ],
            "faqs": [
                ("Do we keep full ownership of our WhatsApp number and patient data?", "Yes—ClinicFlow runs 100% BYOK on your Meta WhatsApp Cloud API, Google Calendar / EMR, and self-hosted n8n instance."),
                ("Should we pick the $39 Workflow or the $690 7-Day Pilot?", "Grab the $39 n8n Pack if you have an internal developer; pick the $690 7-Day Pilot if you want us to wire WhatsApp, calendar sync, and safety hand-offs for you."),
            ],
            "calc_title": "Interactive Clinic Recovered Revenue Calculator",
            "lbl_inq": "Monthly Patient WhatsApp Inquiries",
            "lbl_ns": "Current No-Show & Missed-Lead Rate (%)",
            "lbl_val": "Average Consultation / Procedure Value (USD)",
            "lbl_impact": "Estimated Monthly & Annual Recovered Revenue (65% Recovery)",
        },
        "es": {
            "badge": "ROI Clínicas · WhatsApp IA Anti-Inasistencias",
            "title": "Calculadora ROI de Agente IA WhatsApp y Anti-Inasistencias para Clínicas (2026–2027)",
            "short_title": "Calculadora ROI WhatsApp para Clínicas",
            "meta_desc": "Calcula cuántos ingresos mensuales y anuales recupera tu clínica médica, odontológica o estética con una recepcionista IA 24/7 en WhatsApp y recordatorios 24h/2h.",
            "bluf": "Una clínica con 300 consultas mensuales por WhatsApp, 22% de inasistencias/leads perdidos y ticket promedio de $75 USD pierde ~$4,950/mes. Recuperar el 65% con agenda 24/7 y recordatorios 24h/2h suma ~$3,225/mes ($38,700/año).",
            "intro": "Los pacientes escriben de noche y olvidan sus citas si nadie les confirma a tiempo. Ajusta los valores de tu clínica para ver el ingreso recuperado exacto.",
            "table_headers": ["Etapa", "Recepción Manual", "ClinicFlow AI (Self-Hosted)", "Impacto Real"],
            "table_rows": [
                ("Chats Fuera de Horario", "Sin respuesta hasta el día siguiente", "Atención 24/7 + agendamiento en vivo", "+35–50% captación nocturna"),
                ("Recordatorios 24h y 2h", "Llamadas manuales o SMS olvidados", "Confirmación/reprogramación en 1 toque", "Hasta 65% menos ausencias"),
                ("Cancelaciones", "Consultorio vacío", "Avisa automático a lista de espera", "Mayor ocupación diaria"),
                ("Costo Mensual Software", "$299–$599/mes en SaaS por asiento", "$0 Docker n8n + ~$0.004/ventana WhatsApp", "Cero amarres ni rentas por asiento"),
            ],
            "faqs": [
                ("¿Conservamos control total del número de WhatsApp y datos de pacientes?", "Sí: ClinicFlow corre 100% en modo BYOK con tu propia API oficial de Meta WhatsApp, Google Calendar/historia clínica y servidor n8n."),
                ("¿Conviene comprar el Pack de $39 o el Piloto de $690?", "Si cuentas con desarrollador interno, compra el Pack de $39; si quieres que conectemos WhatsApp, calendario y reglas de escalamiento en 7 días, elige el Piloto de $690."),
            ],
            "calc_title": "Calculadora Interactiva de Ingresos Recuperados en tu Clínica",
            "lbl_inq": "Consultas Mensuales de Pacientes por WhatsApp",
            "lbl_ns": "Tasa Actual de Inasistencias y Leads Perdidos (%)",
            "lbl_val": "Valor Promedio por Consulta o Procedimiento (USD)",
            "lbl_impact": "Ingresos Recuperados Estimados (65% Conservador)",
        },
    },
]


def render_head(title: str, desc: str, lang: str, rel_path: str, og_file: str, css_href: str, json_ld: dict) -> str:
    en_url = f"{BASE_URL}/{rel_path}" if rel_path else f"{BASE_URL}/"
    es_url = f"{BASE_URL}/es/{rel_path}" if rel_path else f"{BASE_URL}/es/"
    canonical = es_url if lang == "es" else en_url
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{esc(canonical)}" />
  <link rel="alternate" hreflang="en" href="{esc(en_url)}" />
  <link rel="alternate" hreflang="es" href="{esc(es_url)}" />
  <link rel="alternate" hreflang="x-default" href="{esc(en_url)}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="{'es_CO' if lang == 'es' else 'en_US'}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{esc(canonical)}" />
  <meta property="og:image" content="{BASE_URL}/assets/og/{esc(og_file)}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{BASE_URL}/assets/og/{esc(og_file)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{esc(css_href)}" />
  <script>
    (function(){{
      var t = localStorage.getItem("tt_theme_v2");
      if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
    }})();
  </script>
  <script src="https://gumroad.com/js/gumroad.js" defer></script>
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>"""


def render_navbar(lang: str, home_href: str, en_href: str, es_href: str) -> str:
    is_es = lang == "es"
    return f"""  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="{esc(home_href)}">
        <span class="brand-mark">TT</span>
        <span class="brand-title">TuringTec</span>
        <span class="brand-live"><span class="live-dot"></span>{'4 demos en vivo' if is_es else '4 live sandboxes'}</span>
      </a>
      <nav class="nav-links" aria-label="{'Navegación principal' if is_es else 'Primary navigation'}">
        <a class="nav-link" href="{esc(home_href)}#sandboxes">{'Demos en Vivo' if is_es else 'Live Demos'}</a>
        <a class="nav-link" href="{esc(home_href)}#solutions">{'Soluciones' if is_es else 'Solutions'}</a>
        <a class="nav-link" href="{esc(home_href)}#calculators">{'Calculadoras ROI' if is_es else 'ROI Calculators'}</a>
        <a class="nav-link" href="{esc(home_href)}#pricing">{'Precios' if is_es else 'Pricing'}</a>
      </nav>
      <div class="nav-right">
        <div class="lang-switch" role="group" aria-label="Language switcher">
          <a class="lang-opt {'active' if not is_es else ''}" href="{esc(en_href)}" hreflang="en" rel="alternate" data-lang="en">EN</a>
          <a class="lang-opt {'active' if is_es else ''}" href="{esc(es_href)}" hreflang="es" rel="alternate" data-lang="es">ES</a>
        </div>
        <button id="btnTheme" class="btn btn-icon" type="button" aria-label="Toggle theme">{'Claro' if is_es else 'Light'}</button>
        <a class="btn btn-primary btn-sm" href="{GUMROAD_STORE}" target="_blank" rel="noopener">{'Ver Tienda' if is_es else 'Open Store'}</a>
      </div>
    </div>
  </header>"""


def render_footer(lang: str, root_rel: str) -> str:
    is_es = lang == "es"
    sol_prefix = f"{root_rel}es/solutions/" if is_es else f"{root_rel}solutions/"
    cmp_prefix = f"{root_rel}es/compare/" if is_es else f"{root_rel}compare/"
    sol_links = "".join(f'<li><a href="{sol_prefix}{s["slug"]}/">{esc(s[lang]["short_title"])}</a></li>' for s in SOLUTIONS)
    cmp_links = "".join(f'<li><a href="{cmp_prefix}{c["slug"]}/">{esc(c[lang]["short_title"])}</a></li>' for c in COMPARES)
    return f"""    <footer class="footer">
      <div class="footer-grid">
        <div>
          <h4>{'Soluciones Verticales de Agentes IA' if is_es else 'Vertical AI Agent Solutions'}</h4>
          <ul>{sol_links}</ul>
        </div>
        <div>
          <h4>{'Calculadoras Interactivas de ROI' if is_es else 'Interactive ROI Calculators'}</h4>
          <ul>{cmp_links}</ul>
        </div>
        <div>
          <h4>{'Ecosistema Open-Core y Cloud' if is_es else 'Open-Core & Cloud Ecosystem'}</h4>
          <ul>
            <li><a href="{FINOPS_REPO}" target="_blank" rel="noopener">aws-finops-guard (GitHub CLI + MCP)</a></li>
            <li><a href="{APIFY_REPO}" target="_blank" rel="noopener">Apify Dual-Mode MCP Suite (3 Servers)</a></li>
            <li><a href="{CLOUDCERT_URL}" target="_blank" rel="noopener">CloudCert Lab — {'Simulador Certificaciones Cloud' if is_es else 'Multi-Cloud Exam Simulator'}</a></li>
            <li><a href="{GUMROAD_STORE}" target="_blank" rel="noopener">{'Tienda Oficial Gumroad ($39–$99)' if is_es else 'Official Gumroad Store ($39–$99)'}</a></li>
            <li><a href="{root_rel}llms-full.txt">llms-full.txt ({'Referencia IA' if is_es else 'AI Reference'})</a></li>
          </ul>
        </div>
      </div>
      <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
        <span>© 2026 TuringTec Agent Studio · {'Agentes IA B2B, Servidores MCP y FinOps AWS.' if is_es else 'B2B AI Agents, MCP Servers & AWS FinOps.'}</span>
        <span>{'Actualizado' if is_es else 'Updated'} {TODAY}</span>
      </div>
    </footer>"""


def build_home_html(lang: str) -> str:
    is_es = lang == "es"
    root_rel = "../" if is_es else ""
    home_href = "./"
    en_href = "../" if is_es else "./"
    es_href = "./" if is_es else "es/"

    title = (
        "TuringTec Agent Studio — Agentes IA B2B en Producción, Servidores MCP y FinOps AWS (2026–2027)"
        if is_es
        else "TuringTec Agent Studio — Production B2B AI Agents, MCP Servers & AWS FinOps (2026–2027)"
    )
    desc = (
        "Prueba 4 demos en vivo sin registro: recepcionista WhatsApp para clínicas, cotizador B2B ferretero, extractor de facturas PDF a ERP y auditor FinOps AWS. Kits self-hosted $39–$99 o piloto en 7 días."
        if is_es
        else "Test 4 live browser AI agent sandboxes ($0 signup): B2B hardware quoting, invoice PDF-to-ERP extraction, AWS FinOps Guard, and 24/7 clinic WhatsApp receptionist. Self-hosted kits $39–$99 or 7-day turnkey pilot."
    )
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE_URL}/#organization",
                "name": "TuringTec Agent Studio",
                "url": f"{BASE_URL}/",
                "sameAs": [FINOPS_REPO, APIFY_REPO, CLOUDCERT_URL],
            },
            {
                "@type": "WebPage",
                "@id": f"{BASE_URL}/{'es/' if is_es else ''}#webpage",
                "url": f"{BASE_URL}/{'es/' if is_es else ''}",
                "name": title,
                "description": desc,
                "inLanguage": lang,
                "isPartOf": {"@id": f"{BASE_URL}/#organization"},
            },
            {
                "@type": "SoftwareApplication",
                "name": "TuringTec AI Agent Business-in-a-Box",
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Cross-Platform",
                "inLanguage": lang,
                "offers": [
                    {"@type": "Offer", "name": "15 Production n8n AI Workflows", "price": "39", "priceCurrency": "USD", "url": GUMROAD_STORE},
                    {"@type": "Offer", "name": "AWS FinOps & LLM Guard Pro", "price": "49", "priceCurrency": "USD", "url": GUMROAD_STORE},
                    {"@type": "Offer", "name": "AI Agent Business-in-a-Box", "price": "99", "priceCurrency": "USD", "url": GUMROAD_STORE},
                ],
            },
        ],
    }

    sol_cards = "".join(
        f"""<a class="bento-card" href="{'solutions/' if not is_es else 'solutions/'}{s['slug']}/">
          <div>
            <span class="tag tag-brand">{esc(s[lang]['badge'])}</span>
            <h3>{esc(s[lang]['short_title'])}</h3>
            <p>{esc(s[lang]['card_desc'])}</p>
          </div>
          <div class="bento-foot">
            <span>{esc(s[lang]['price_kit'].split('/')[0].strip())}</span>
            <span>{'Ver arquitectura' if is_es else 'View architecture'} →</span>
          </div>
        </a>"""
        for s in SOLUTIONS
    )

    cmp_cards = "".join(
        f"""<a class="bento-card" href="compare/{c['slug']}/">
          <div>
            <span class="tag tag-live">{esc(c[lang]['badge'])}</span>
            <h3>{esc(c[lang]['short_title'])}</h3>
            <p>{esc(c[lang]['bluf'][:155])}...</p>
          </div>
          <div class="bento-foot">
            <span>{'Abrir calculadora' if is_es else 'Open calculator'}</span>
            <span>→</span>
          </div>
        </a>"""
        for c in COMPARES
    )

    faqs = (
        [
            ("¿Debo pagar suscripciones SaaS mensuales por estos agentes?", "No. Todos los kits corren self-hosted en tu propio Docker n8n o Python/MCP usando tus propias API keys (BYOK), sin comisiones mensuales ni amarres de proveedor."),
            ("¿Puedo instalar estos agentes para mis propios clientes en marca blanca?", "Sí. El paquete Business-in-a-Box ($99) incluye licencia comercial para desplegar y personalizar los 15 workflows n8n, 4 servidores MCP y 12 Agent Skills para clientes ilimitados."),
            ("¿Qué pasa si un caso es complejo o crítico (urgencia médica o factura descuadrada)?", "Todos nuestros flujos incluyen validación determinística y reglas Human-in-the-Loop para pausar el bot y escalar al instante a tu equipo por WhatsApp, Chatwoot o Slack."),
            ("¿Cuándo conviene el Kit de $39–$99 vs. el Piloto Llave en Mano de $690?", "Si tienes perfil técnico o agencia, compra los kits self-hosted ($39–$99) y despliégalos hoy. Si prefieres que nuestro equipo conecte tu WhatsApp, ERP o AWS en 7 días con entrega llave en mano, reserva el piloto."),
        ]
        if is_es
        else [
            ("Do these AI agents require monthly SaaS subscriptions?", "No. Every kit runs self-hosted via Docker Compose or local Python/MCP using your own API keys (BYOK), with zero per-seat markup or platform lock-in."),
            ("Can I white-label and deploy these agents for paying agency clients?", "Yes. The $99 AI Agent Business-in-a-Box includes full commercial deployment rights for unlimited client installations (raw ZIP resale is excluded)."),
            ("How do you prevent hallucinations on invoices, quotes, or medical triage?", "Every workflow combines strict JSON schemas, deterministic arithmetic/margin validation, and human-in-the-loop escalation gates before write actions."),
            ("Should I buy the $39–$99 Self-Hosted Kits or the $690 Turnkey Pilot?", "Pick the $39–$99 kits if you or your dev team want immediate source code. Book the $690 7-day pilot if you want us to wire your WhatsApp, ERP, or AWS stack end-to-end."),
        ]
    )
    faq_html = "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs)

    fq_default = (
        "Hola necesito cotizar urgente para obra norte:\n40 bultos cemento gris 50kg\n12 tubos pvc sanitario 2 pulgadas\n5 cajas tornillo drywall 1 pulg\n3 galones pintura vinilo blanco tipo 1\n20 ladrillos estructurales"
        if is_es
        else "Hi, urgent quote needed for North Site:\n40 bags gray cement 50kg\n12 pvc sanitary pipe 2 inch\n5 boxes drywall screw 1 inch\n3 gal white vinyl paint\n20 structural brick"
    )
    df_default = (
        "FACTURA ELECTRONICA DE VENTA No. FE-2026-8841\nPROVEEDOR: DISTRIBUIDORA INDUSTRIAL ANDINA S.A.S.\nNIT: 901.442.819-3\nFECHA: 2026-11-26\nITEM 1: VALVULA BOLA BRONCE 1 PULG | CANT: 25 | UNIT: 14.50 | SUB: 362.50\nITEM 2: CABLE THHN CALIBRE 12 ROLLO 100M | CANT: 6 | UNIT: 48.00 | SUB: 288.00\nSUBTOTAL: 650.50\nIVA 19%: 123.60\nTOTAL A PAGAR USD: 774.10"
        if is_es
        else "COMMERCIAL INVOICE No. FE-2026-8841\nVENDOR: ANDINA INDUSTRIAL SUPPLY LLC\nTAX ID: 901.442.819-3\nDATE: 2026-11-26\nITEM 1: BRONZE BALL VALVE 1 INCH | QTY: 25 | UNIT: 14.50 | SUB: 362.50\nITEM 2: THHN COPPER CABLE 12 AWG 100M | QTY: 6 | UNIT: 48.00 | SUB: 288.00\nSUBTOTAL: 650.50\nTAX 19%: 123.60\nTOTAL USD: 774.10"
    )

    body = f"""<body class="ambient-bg">
{render_navbar(lang, home_href, en_href, es_href)}
  <main class="container">
    <!-- HERO -->
    <section class="hero-split">
      <div>
        <div class="status-pill">
          <span class="live-dot"></span>
          <span>{'Agentes IA en Producción · Código Propio · Cero Amarres SaaS' if is_es else 'Production B2B AI Agents · Own Your Code · Zero SaaS Lock-In'}</span>
        </div>
        <h1>{'Agentes IA que cotizan, agendan, causan facturas y podan tu AWS 24/7.' if is_es else 'Deploy AI agents that quote, book, reconcile invoices & cut AWS waste 24/7.'}</h1>
        <p class="hero-lead">
          {'Convierte chats de WhatsApp en citas confirmadas, listas ferreteras en cotizaciones PDF en 45 segundos, facturas PDF en registros listos para tu ERP y desperdicio de AWS en ahorro real—sobre tu propio Docker n8n, ERP y MCP.' if is_es else 'Turn WhatsApp chats into booked clinic visits, messy hardware RFQs into 45-second quotes, supplier PDFs into validated ERP entries, and idle AWS spend into recovered margin—running on your own n8n, ERP & MCP stack.'}
        </p>
        <div class="hero-ctas">
          <a class="btn btn-primary" href="#sandboxes">{'Probar 4 Demos en Vivo ($0)' if is_es else 'Test 4 Live Demos ($0)'}</a>
          <a class="btn" href="#pricing">{'Ver Kits ($39–$99) y Pilotos' if is_es else 'See Kits ($39–$99) & Pilots'}</a>
        </div>
        <div class="hero-micro">
          <span>✓ {'Sin registro para las demos' if is_es else 'No signup for live sandboxes'}</span>
          <span>✓ {'100% BYOK y código propio' if is_es else '100% BYOK & source ownership'}</span>
          <span>✓ {'Entrega instantánea Gumroad' if is_es else 'Instant Gumroad delivery'}</span>
        </div>
      </div>

      <aside class="trace-card" aria-label="Live execution preview">
        <div class="trace-top">
          <span class="trace-dots"><i></i><i></i><i></i></span>
          <span class="mono">turingtec-agent-runtime · v2.6</span>
          <span class="tag tag-live">● {'En línea' if is_es else 'Online'}</span>
        </div>
        <div class="trace-steps">
          <div class="trace-step">
            <div>
              <strong>1. {'Entrada Omnicanal (WhatsApp / PDF / AWS)' if is_es else 'Omnichannel Ingest (WhatsApp / PDF / AWS)'}</strong>
              <span>{'Lista de obra, factura proveedor, cita médica o snapshot AWS' if is_es else 'Bill of materials, supplier PDF, patient chat, or AWS snapshot'}</span>
            </div>
            <span class="trace-ms">42 ms</span>
          </div>
          <div class="trace-step">
            <div>
              <strong>2. {'Validación Determinística y Guardrails' if is_es else 'Deterministic Schema & Margin Guardrails'}</strong>
              <span>{'Cruce SKU + verificación aritmética IVA + escalamiento humano' if is_es else 'SKU lookup + tax math verification + human escalation rules'}</span>
            </div>
            <span class="trace-ms">118 ms</span>
          </div>
          <div class="trace-step">
            <div>
              <strong>3. {'Ejecución en Producción (ERP / Agenda / Terraform)' if is_es else 'Production Action (ERP / Calendar / Terraform)'}</strong>
              <span>{'Cotización CSV, asiento ERP validado o parche HCL listo' if is_es else 'Ready-to-send quote CSV, clean ERP JSON, or Terraform patch'}</span>
            </div>
            <span class="trace-ms">210 ms</span>
          </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; padding-top:0.5rem; border-top:1px solid var(--border); font-size:0.8rem;">
          <span class="mono" style="color:var(--muted);">{'Latencia total: 370 ms · Costo SaaS: $0/mes' if is_es else 'Total latency: 370ms · SaaS fee: $0/mo'}</span>
          <a href="#sandboxes" style="color:var(--brand-hover); font-weight:600; text-decoration:none;">{'Ejecutar abajo ↓' if is_es else 'Run below ↓'}</a>
        </div>
      </aside>
    </section>

    <!-- PROOF STRIP -->
    <section class="proof-strip" aria-label="Key operational outcomes">
      <div class="proof-cell">
        <div class="proof-num">45 s</div>
        <div class="proof-label">{'Cotizaciones B2B de 40 ítems (antes 3–4 horas manuales)' if is_es else '40-line B2B quotes generated (vs 3–4 hrs manual)'}</div>
      </div>
      <div class="proof-cell">
        <div class="proof-num">24/7</div>
        <div class="proof-label">{'Cero chats ni llamadas perdidas en clínicas con WhatsApp IA' if is_es else 'Zero missed clinic chats with 24h/2h anti-no-show'}</div>
      </div>
      <div class="proof-cell">
        <div class="proof-num">99.4%</div>
        <div class="proof-label">{'Exactitud validada matemáticamente en facturas PDF a ERP' if is_es else 'Math-validated line accuracy on supplier PDFs to ERP'}</div>
      </div>
      <div class="proof-cell">
        <div class="proof-num">25–60%</div>
        <div class="proof-label">{'Recorte típico en gasto ocioso AWS y tokens LLM vía MCP' if is_es else 'Typical AWS idle & LLM token spend recovered via MCP'}</div>
      </div>
    </section>

    <!-- 4 LIVE INTERACTIVE SANDBOXES -->
    <section id="sandboxes" class="section">
      <div class="section-header">
        <div class="section-kicker">{'// PRUEBA ANTES DE COMPRAR · $0 COSTO DE API' if is_es else '// TRY BEFORE YOU BUY · ZERO API KEY REQUIRED'}</div>
        <h2>{'4 Sandboxes Interactivos de Agentes IA en tu Navegador' if is_es else '4 Interactive B2B AI Agent Sandboxes Live in Your Browser'}</h2>
        <p>{'Edita los textos reales o mueve los parámetros para ver resultados determinísticos, JSON limpio y ahorros al instante.' if is_es else 'Edit real inputs or adjust numbers to inspect deterministic outputs, clean JSON/CSV exports, and instant ROI.'}</p>
      </div>

      <div class="tabs" role="tablist">
        <button class="tab-btn active" data-tab="ferrequote" type="button">{'1. FerreQuote AI (Cotizador B2B)' if is_es else '1. FerreQuote AI (B2B RFQ)'}</button>
        <button class="tab-btn" data-tab="docflow" type="button">{'2. DocFlow B2B (Facturas PDF)' if is_es else '2. DocFlow B2B (Invoice PDF)'}</button>
        <button class="tab-btn" data-tab="finops" type="button">{'3. AWS & LLM FinOps Guard' if is_es else '3. AWS & LLM FinOps Guard'}</button>
        <button class="tab-btn" data-tab="clinicflow" type="button">{'4. ClinicFlow AI (Clínicas WhatsApp)' if is_es else '4. ClinicFlow AI (Clinics WhatsApp)'}</button>
      </div>

      <!-- TAB 1 -->
      <div id="tab-ferrequote" class="card sandbox-panel">
        <div class="sandbox-grid">
          <div>
            <label class="field-label" for="fqInput">{'Pega un pedido desordenado por WhatsApp o correo:' if is_es else 'Paste a messy WhatsApp or email material list:'}</label>
            <textarea id="fqInput" rows="7">{esc(fq_default)}</textarea>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:0.75rem;">
              <button id="btnFqRun" class="btn btn-primary" type="button">{'Cotizar al Instante' if is_es else 'Generate B2B Quote'}</button>
              <button id="btnFqExport" class="btn" type="button">{'Descargar CSV' if is_es else 'Download CSV'}</button>
              <a class="btn btn-ghost" href="solutions/hardware-b2b-quoting-agent/">{'Ver solución completa →' if is_es else 'Full architecture →'}</a>
            </div>
          </div>
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
              <span class="tag tag-live" id="fqStatus">{'Cruce SKU listo' if is_es else 'SKU Match Ready'}</span>
              <strong id="fqTotal" class="tabular" style="font-size:1.15rem;">$0.00 USD</strong>
            </div>
            <div id="fqTableWrap"></div>
          </div>
        </div>
      </div>

      <!-- TAB 2 -->
      <div id="tab-docflow" class="card sandbox-panel hidden">
        <div class="sandbox-grid">
          <div>
            <label class="field-label" for="dfInput">{'Texto crudo de Factura u Orden de Compra (edítalo libremente):' if is_es else 'Raw Invoice or Purchase Order Text (editable):'}</label>
            <textarea id="dfInput" rows="8">{esc(df_default)}</textarea>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:0.75rem;">
              <button id="btnDfRun" class="btn btn-primary" type="button">{'Extraer JSON ERP' if is_es else 'Extract ERP JSON'}</button>
              <button id="btnDfDownload" class="btn" type="button">{'Descargar JSON' if is_es else 'Download JSON'}</button>
              <a class="btn btn-ghost" href="solutions/invoice-pdf-extraction-agent/">{'Ver solución completa →' if is_es else 'Full architecture →'}</a>
            </div>
          </div>
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <span class="tag tag-live" id="dfScore">{'Confianza: 99.4% · Sumas Validadas ✓' if is_es else 'Confidence: 99.4% · Math Verified ✓'}</span>
              <span class="tag tag-brand">{'0 Discrepancias' if is_es else '0 Discrepancies'}</span>
            </div>
            <pre id="dfOutput" class="code-out"></pre>
          </div>
        </div>
      </div>

      <!-- TAB 3 -->
      <div id="tab-finops" class="card sandbox-panel hidden">
        <div class="sandbox-grid">
          <div style="display:flex; flex-direction:column; gap:0.8rem;">
            <div>
              <label class="field-label" for="finEbs">{'Almacenamiento EBS huérfano + gp2 legado (GB)' if is_es else 'Unattached + Legacy gp2 EBS Storage (GB)'}</label>
              <input id="finEbs" type="number" min="0" value="750" />
            </div>
            <div>
              <label class="field-label" for="finNat">{'Tráfico mensual NAT Gateway sin S3 Endpoint (GB)' if is_es else 'Monthly NAT Gateway Traffic without S3 Endpoint (GB)'}</label>
              <input id="finNat" type="number" min="0" value="1800" />
            </div>
            <div>
              <label class="field-label" for="finRds">{'Gasto mensual en RDS no productivo ocioso (USD)' if is_es else 'Idle Non-Prod RDS Monthly Spend (USD)'}</label>
              <input id="finRds" type="number" min="0" value="292" />
            </div>
            <div>
              <label class="field-label" for="finLlm">{'Millones de tokens/mes en modelo premium para triaje/extracción' if is_es else 'Monthly Input Tokens (Millions) on Premium Model for Triage'}</label>
              <input id="finLlm" type="number" min="0" value="45" />
            </div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a class="btn btn-primary" href="{FINOPS_REPO}" target="_blank" rel="noopener">{'Clonar CLI + MCP Gratis' if is_es else 'Clone Open-Core CLI + MCP'}</a>
              <a class="btn" href="solutions/aws-finops-guardrails-mcp/">{'Parches Terraform ($49)' if is_es else 'Terraform Auto-Fix ($49)'}</a>
            </div>
          </div>
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.55rem;">
              <span class="tag tag-danger">{'GASTO EVITABLE DETECTADO' if is_es else 'AVOIDABLE SPEND DETECTED'}</span>
              <strong id="finTotal" class="tabular" style="font-size:1.2rem; color:var(--danger);">$0 / mo</strong>
            </div>
            <pre id="finOutput" class="code-out"></pre>
          </div>
        </div>
      </div>

      <!-- TAB 4 -->
      <div id="tab-clinicflow" class="card sandbox-panel hidden">
        <div class="sandbox-grid">
          <div>
            <div class="field-label">{'Haz clic en un mensaje de paciente para probar la respuesta 24/7:' if is_es else 'Click a patient WhatsApp message to test 24/7 autonomous booking:'}</div>
            <div style="display:flex; gap:0.45rem; flex-wrap:wrap; margin-bottom:0.75rem;">
              <button class="btn btn-sm" data-clinic-msg="book" type="button">{'📅 Agendar limpieza viernes' if is_es else '📅 Book Friday cleaning'}</button>
              <button class="btn btn-sm" data-clinic-msg="price" type="button">{'💳 Precio y seguros' if is_es else '💳 Price & insurance'}</button>
              <button class="btn btn-sm" data-clinic-msg="reschedule" type="button">{'🔄 Reprogramar cita' if is_es else '🔄 Reschedule visit'}</button>
              <button class="btn btn-sm" data-clinic-msg="confirm" type="button">{'✅ Confirmar 24h' if is_es else '✅ Confirm 24h'}</button>
            </div>
            <div id="clinicChat" class="chat-box"></div>
          </div>
          <div>
            <span class="tag tag-live">{'CALCULADORA ROI ANTI-INASISTENCIAS' if is_es else 'ANTI-NO-SHOW ROI CALCULATOR'}</span>
            <h3 style="margin:0.5rem 0 0.65rem; font-size:1.05rem;">{'¿Cuánto dinero recupera tu clínica al mes?' if is_es else 'How much revenue does 24/7 WhatsApp recover monthly?'}</h3>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.65rem;">
              <div>
                <label class="field-label" for="clMissed">{'Citas/leads perdidos al mes' if is_es else 'Missed visits/leads per month'}</label>
                <input id="clMissed" type="number" min="1" value="18" />
              </div>
              <div>
                <label class="field-label" for="clTicket">{'Ticket promedio consulta (USD)' if is_es else 'Avg. consultation value (USD)'}</label>
                <input id="clTicket" type="number" min="10" value="65" />
              </div>
            </div>
            <div id="clinicRoi" class="card" style="margin-top:0.85rem; background:var(--surface-2); box-shadow:none; padding:1rem;"></div>
            <div style="margin-top:0.8rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a class="btn btn-primary" href="solutions/clinic-whatsapp-voice-agent/">{'Ver arquitectura clínica →' if is_es else 'See clinic architecture →'}</a>
              <a class="btn" href="{GUMROAD_STORE}" target="_blank" rel="noopener">{'Pack n8n ($39)' if is_es else 'n8n Pack ($39)'}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- BEFORE VS AFTER -->
    <section class="section">
      <div class="section-header">
        <div class="section-kicker">{'// POR QUÉ CAMBIAN LOS EQUIPOS DE OPERACIONES' if is_es else '// WHY OPS & ENGINEERING TEAMS SWITCH'}</div>
        <h2>{'Operación manual o agencias de $3,500/mes vs. Agentes propios' if is_es else 'Manual ops & $3,500/mo SaaS lock-in vs. Ownable AI Agents'}</h2>
      </div>
      <div class="compare-two">
        <div class="compare-col">
          <span class="tag tag-danger">{'Modelo Tradicional / SaaS Rígido' if is_es else 'Legacy Manual / SaaS Lock-In'}</span>
          <ul class="compare-list">
            <li><span>✕</span><div><strong>{'3–4 horas por cotización B2B:' if is_es else '3–4 hours per B2B quote:'}</strong> {'los compradores cierran con el competidor que responde primero.' if is_es else 'buyers close with whoever replies first.'}</div></li>
            <li><span>✕</span><div><strong>{'Pacientes perdidos de noche:' if is_es else 'After-hours patient leaks:'}</strong> {'20–30% de leads por WhatsApp se enfrían antes de abrir agenda.' if is_es else '20–30% of inbound inquiries go cold overnight.'}</div></li>
            <li><span>✕</span><div><strong>{'$300–$1,500/mes por asiento y tarea:' if is_es else '$300–$1,500/mo per-seat & per-task tax:'}</strong> {'Zapier y CRMs te castigan por crecer.' if is_es else 'Zapier & SaaS tools tax every workflow step.'}</div></li>
            <li><span>✕</span><div><strong>{'Cajas negras sin código:' if is_es else 'Black-box vendor lock-in:'}</strong> {'si cancelas la mensualidad, pierdes tus flujos y datos.' if is_es else 'cancel the subscription and lose your workflows.'}</div></li>
          </ul>
        </div>
        <div class="compare-col after">
          <span class="tag tag-live">{'Con TuringTec Agent Studio (BYOK)' if is_es else 'With TuringTec Agent Studio (BYOK)'}</span>
          <ul class="compare-list">
            <li><span>✓</span><div><strong>{'Respuestas y cotizaciones en <45 s:' if is_es else '<45-second quotes & bookings:'}</strong> {'cruza SKUs, valida márgenes e IVA antes de responder.' if is_es else 'matches SKUs, checks margins, and confirms slots 24/7.'}</div></li>
            <li><span>✓</span><div><strong>{'Self-hosted en tu Docker o AWS:' if is_es else 'Self-hosted on your Docker or AWS:'}</strong> {'$0 en licencias por asiento y control total de tus datos.' if is_es else '$0 per-seat markup and full data privacy.'}</div></li>
            <li><span>✓</span><div><strong>{'Pago único ($39–$99) o Piloto fijo ($690):' if is_es else 'One-time kits ($39–$99) or fixed pilot ($690):'}</strong> {'retorno de inversión medible desde la primera semana.' if is_es else 'measurable payback inside the first week.'}</div></li>
            <li><span>✓</span><div><strong>{'Propiedad 100% del código fuente:' if is_es else '100% source code ownership:'}</strong> {'n8n JSONs, servidores MCP, Terraform HCL y skills incluidos.' if is_es else 'every n8n JSON, MCP server, Terraform patch & skill is yours.'}</div></li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 6 SOLUTIONS BENTO -->
    <section id="solutions" class="section">
      <div class="section-header">
        <div class="section-kicker">{'// SOLUCIONES VERTICALES Y SERVIDORES MCP' if is_es else '// VERTICAL SOLUTIONS & MCP SERVERS'}</div>
        <h2>{'Arquitecturas listas para desplegar en tu industria' if is_es else 'Production architectures ready for your industry'}</h2>
        <p>{'Cada solución incluye especificación técnica, flujos BYOK sin llaves quemadas y opción self-hosted o piloto llave en mano.' if is_es else 'Every vertical includes clean BYOK workflows, deterministic guardrails, and both self-hosted kit and turnkey pilot options.'}</p>
      </div>
      <div class="bento-grid">{sol_cards}</div>
    </section>

    <!-- 3 ROI CALCULATORS -->
    <section id="calculators" class="section">
      <div class="section-header">
        <div class="section-kicker">{'// NÚMEROS REALES ANTES DE INVERTIR' if is_es else '// HARD ROI MATH BEFORE YOU SPEND $1'}</div>
        <h2>{'3 Calculadoras Interactivas de Ahorro y Retorno' if is_es else '3 Interactive Savings & Payback Calculators'}</h2>
      </div>
      <div class="bento-grid">{cmp_cards}</div>
    </section>

    <!-- PRICING & PILOTS -->
    <section id="pricing" class="section">
      <div class="section-header">
        <div class="section-kicker">{'// PRECIOS TRANSPARENTES · PAGO ÚNICO SIN SUSCRIPCIONES' if is_es else '// TRANSPARENT PRICING · PAY ONCE, OWN FOREVER'}</div>
        <h2>{'Arranca con kits self-hosted ($39–$99) o delega el piloto en 7 días' if is_es else 'Start with self-hosted kits ($39–$99) or book a 7-day turnkey pilot'}</h2>
        <p>{'Anclado frente a $3,500+/mes de nómina o agencias tradicionales. Entrega inmediata vía Gumroad (Merchant of Record global).' if is_es else 'Anchored against $3,500+/mo manual headcount or agency retainers. Instant delivery via Gumroad (global Merchant of Record).'}</p>
      </div>

      <div class="pricing-grid">
        <article class="price-card">
          <div>
            <span class="tag tag-brand">{'Kits Individuales' if is_es else 'Single Packs'}</span>
            <h3 style="margin:0.55rem 0 0.2rem;">{'15 Workflows n8n o AWS FinOps Pro' if is_es else '15 n8n Workflows or AWS FinOps Pro'}</h3>
            <div class="price-amount">$39–$49 <span>{'pago único' if is_es else 'one-time'}</span></div>
            <ul class="check-list">
              <li><strong>{'15 Flujos n8n ($39):' if is_es else '15 n8n Workflows ($39):'}</strong> {'Clínicas, Cotizador B2B, Facturas, FinOps + Docker.' if is_es else 'Clinics, B2B RFQ, Invoices, FinOps + Docker.'}</li>
              <li><strong>{'AWS FinOps Guard Pro ($49):' if is_es else 'AWS FinOps Guard Pro ($49):'}</strong> {'Parches Terraform HCL + SARIF CI/CD + MCP.' if is_es else 'Terraform HCL patches + CI/CD SARIF + MCP.'}</li>
              <li>{'Código 100% BYOK sin rentas mensuales.' if is_es else '100% BYOK source code, zero monthly fees.'}</li>
            </ul>
          </div>
          <a class="btn" href="{GUMROAD_STORE}" target="_blank" rel="noopener">{'Elegir Kit en Gumroad →' if is_es else 'Pick Your Kit on Gumroad →'}</a>
        </article>

        <article class="price-card featured">
          <div>
            <span class="tag tag-gold">{'Más Elegido · Ahorra 60%' if is_es else 'Most Popular · Save 60%'}</span>
            <h3 style="margin:0.55rem 0 0.2rem;">AI Agent Business-in-a-Box</h3>
            <div class="price-amount">$99 <span>{'pago único · valor $245+' if is_es else 'one-time · $245+ value'}</span></div>
            <ul class="check-list">
              <li><strong>{'Los 15 Workflows n8n' if is_es else 'All 15 n8n AI Workflows'}</strong> + Docker Compose</li>
              <li><strong>{'4 Servidores MCP' if is_es else '4 Production MCP Servers'}</strong> (3 Apify PPE + AWS FinOps)</li>
              <li><strong>{'12 Agent Skills' if is_es else '12 Cross-Platform Skills'}</strong> (Claude, Cursor, Codex, Antigravity)</li>
              <li><strong>{'Licencia Comercial White-Label' if is_es else 'Commercial White-Label Rights'}</strong> {'para clientes ilimitados.' if is_es else 'for unlimited client deployments.'}</li>
            </ul>
          </div>
          <a class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">{'Desbloquear Bóveda ($99) →' if is_es else 'Unlock All-Access Vault ($99) →'}</a>
        </article>

        <article class="price-card">
          <div>
            <span class="tag tag-live">{'Implementación Llave en Mano' if is_es else 'Done-For-You Pilot'}</span>
            <h3 style="margin:0.55rem 0 0.2rem;">{'Auditoría 48h o Piloto 7 Días' if is_es else '48h Audit or 7-Day Pilot'}</h3>
            <div class="price-amount">$299–$690 <span>{'alcance fijo' if is_es else 'fixed scope'}</span></div>
            <ul class="check-list">
              <li><strong>{'Auditoría AWS FinOps 48h ($299):' if is_es else '48h AWS FinOps Audit ($299):'}</strong> {'plan Terraform para recortar 25–60%.' if is_es else 'Terraform roadmap targeting 25–60% cuts.'}</li>
              <li><strong>{'Piloto Vertical 7 Días ($690):' if is_es else '7-Day Vertical Pilot ($690):'}</strong> {'conectamos WhatsApp, ERP o Docs en tu cuenta.' if is_es else 'we wire WhatsApp, ERP, or Docs in your cloud.'}</li>
              <li>{'Soporte opcional $297/mes solo si lo necesitas.' if is_es else 'Optional $297/mo care only if you want it.'}</li>
            </ul>
          </div>
          <a class="btn" href="mailto:gabhack@gmail.com?subject=TuringTec%20B2B%20Pilot%20%2F%20Audit&body={'Hola%20Gabriel%2C%20quiero%20agendar%20un%20Piloto%20o%20Auditor%C3%ADa%20FinOps.' if is_es else 'Hi%20Gabriel%2C%20I%20want%20to%20book%20a%20TuringTec%20Pilot%20or%20FinOps%20Audit.'}">{'Solicitar Piloto / Auditoría →' if is_es else 'Book Audit or Pilot →'}</a>
        </article>
      </div>

      <div class="guarantee-bar">
        <div>
          <strong>{'Garantía Cero Lock-In y Control Total:' if is_es else 'Zero Vendor Lock-In Guarantee:'}</strong>
          <span style="color:var(--muted); font-size:0.9rem;">
            {'Te quedas con el 100% del código, workflows y conectores MCP en tu propia infraestructura. Sin rentas obligatorias.' if is_es else 'You keep 100% of source code, n8n JSON workflows, and MCP connectors on your own stack. No forced subscriptions.'}
          </span>
        </div>
        <a class="btn btn-sm" href="{FINOPS_REPO}" target="_blank" rel="noopener">{'Inspeccionar código en GitHub →' if is_es else 'Inspect Open-Core on GitHub →'}</a>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section">
      <div class="section-header">
        <div class="section-kicker">{'// PREGUNTAS FRECUENTES' if is_es else '// FREQUENTLY ASKED QUESTIONS'}</div>
        <h2>{'Respuestas directas antes de empezar' if is_es else 'Straight answers before you deploy'}</h2>
      </div>
      <div class="faq-list">{faq_html}</div>
    </section>

{render_footer(lang, root_rel)}
  </main>
  <script src="{root_rel}studio.js"></script>
</body>
</html>"""
    return render_head(title, desc, lang, "", "es-home.png" if is_es else "home.png", f"{root_rel}styles.css", json_ld) + "\n" + body


def build_solution_html(sol: dict, lang: str) -> str:
    is_es = lang == "es"
    slug = sol["slug"]
    d = sol[lang]
    root_rel = "../../../" if is_es else "../../"
    home_href = "../../"
    en_href = f"../../../solutions/{slug}/" if is_es else "./"
    es_href = "./" if is_es else f"../../es/solutions/{slug}/"
    rel_path = f"solutions/{slug}/"
    og_file = f"es-{slug}.png" if is_es else f"{slug}.png"

    rows_html = "".join(f"<tr><td><strong>{esc(k)}</strong></td><td>{esc(v)}</td></tr>" for k, v in d["rows"])
    faqs_html = "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in d["faqs"])
    siblings = "".join(
        f'<a class="bento-card" href="../{s["slug"]}/"><div><span class="tag tag-brand">{esc(s[lang]["badge"])}</span><h3>{esc(s[lang]["short_title"])}</h3><p>{esc(s[lang]["card_desc"])}</p></div><div class="bento-foot"><span>{"Ver" if is_es else "Explore"}</span><span>→</span></div></a>'
        for s in SOLUTIONS if s["slug"] != slug
    )[:3000]

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "TuringTec Agent Studio", "item": f"{BASE_URL}/{'es/' if is_es else ''}"},
                    {"@type": "ListItem", "position": 2, "name": d["short_title"], "item": f"{BASE_URL}/{'es/' if is_es else ''}{rel_path}"},
                ],
            },
            {
                "@type": "SoftwareApplication",
                "name": d["short_title"],
                "description": d["meta_desc"],
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Cross-Platform",
                "inLanguage": lang,
            },
            {
                "@type": "FAQPage",
                "inLanguage": lang,
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]],
            },
        ],
    }

    body = f"""<body class="ambient-bg">
{render_navbar(lang, home_href, en_href, es_href)}
  <main class="container">
    <div style="font-size:0.82rem; color:var(--muted); margin-bottom:1rem;">
      <a href="{home_href}" style="color:var(--brand-hover); text-decoration:none;">TuringTec Agent Studio</a> / {esc(d['short_title'])}
    </div>

    <section class="hero-split" style="padding-top:0.25rem;">
      <div>
        <div class="status-pill"><span class="live-dot"></span><span>{esc(d['badge'])}</span></div>
        <h1>{esc(d['title'])}</h1>
        <p class="hero-lead">{esc(d['intro'])}</p>
        <div class="hero-ctas">
          <a class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">{'Comprar Kit Self-Hosted →' if is_es else 'Get Self-Hosted Kit →'}</a>
          <a class="btn" href="{home_href}#sandboxes">{'Probar Sandbox Gratis' if is_es else 'Test Free Sandbox'}</a>
        </div>
      </div>
      <aside class="price-card featured">
        <div>
          <span class="tag tag-gold">{'Acceso Instantáneo · Sin Suscripción' if is_es else 'Instant Access · No Subscription'}</span>
          <div style="margin-top:0.85rem; font-size:0.78rem; color:var(--muted); font-weight:700;">{'KIT SELF-HOSTED' if is_es else 'SELF-HOSTED KIT'}</div>
          <div style="font-size:1.35rem; font-weight:800; margin:0.2rem 0 0.8rem;">{esc(d['price_kit'])}</div>
          <div style="font-size:0.78rem; color:var(--muted); font-weight:700;">{'IMPLEMENTACIÓN LLAVE EN MANO' if is_es else 'TURNKEY DEPLOYMENT'}</div>
          <div style="font-size:1.15rem; font-weight:700; color:var(--live); margin:0.2rem 0 0.9rem;">{esc(d['price_pilot'])}</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:0.55rem;">
          <a class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">{'Abrir Checkout en Gumroad →' if is_es else 'Checkout on Gumroad →'}</a>
          <a class="btn" href="mailto:gabhack@gmail.com?subject={esc(d['short_title'])}">{'Solicitar Piloto B2B' if is_es else 'Book B2B Pilot'}</a>
        </div>
      </aside>
    </section>

    <section class="card section" style="margin-top:1.5rem;">
      <h2 style="margin:0 0 0.6rem; font-size:1.25rem;">{'Arquitectura y Especificaciones de Producción' if is_es else 'Production Architecture & Specifications'}</h2>
      <table class="data-table">
        <thead><tr><th>{'Componente' if is_es else 'Component'}</th><th>{'Especificación' if is_es else 'Production Specification'}</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </section>

    <section class="section">
      <div class="section-header"><h2>{'Preguntas Frecuentes' if is_es else 'Frequently Asked Questions'}</h2></div>
      <div class="faq-list">{faqs_html}</div>
    </section>

    <section class="section">
      <div class="section-header"><h2>{'Otras Soluciones TuringTec' if is_es else 'Explore Other TuringTec Solutions'}</h2></div>
      <div class="bento-grid">{''.join(f'<a class="bento-card" href="../{s["slug"]}/"><div><span class="tag tag-brand">{esc(s[lang]["badge"])}</span><h3>{esc(s[lang]["short_title"])}</h3><p>{esc(s[lang]["card_desc"])}</p></div><div class="bento-foot"><span>{"Ver" if is_es else "Explore"}</span><span>→</span></div></a>' for s in SOLUTIONS if s["slug"] != slug)}</div>
    </section>

{render_footer(lang, root_rel)}
  </main>
  <script src="{root_rel}studio.js"></script>
</body>
</html>"""
    return render_head(f"{d['title']} | TuringTec Agent Studio", d["meta_desc"], lang, rel_path, og_file, f"{root_rel}styles.css", json_ld) + "\n" + body


def build_compare_calc_html_and_js(slug: str, d: dict, lang: str) -> tuple[str, str]:
    is_es = lang == "es"
    if slug == "n8n-vs-zapier-vs-make-calculator":
        calc_html = f"""
    <section class="card section" style="margin-top:1.5rem;">
      <span class="tag tag-brand">{'SLIDERS EN VIVO' if is_es else 'LIVE INTERACTIVE SLIDERS'}</span>
      <h2 style="margin:0.5rem 0 1rem; font-size:1.3rem;">{esc(d['calc_title'])}</h2>
      <div class="sandbox-grid">
        <div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="n8nRuns"><strong>{esc(d['lbl_runs'])}</strong></label><span class="calc-slider-val" id="n8nRunsVal">10,000</span></div>
            <input id="n8nRuns" type="range" min="1000" max="100000" step="1000" value="10000" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="n8nSteps"><strong>{esc(d['lbl_steps'])}</strong></label><span class="calc-slider-val" id="n8nStepsVal">6</span></div>
            <input id="n8nSteps" type="range" min="2" max="15" step="1" value="6" />
          </div>
          <div class="calc-stat">
            <div class="calc-stat-label">{esc(d['lbl_ops'])}</div>
            <div id="n8nTasksTotal" class="calc-stat-val">60,000</div>
          </div>
        </div>
        <div>
          <div class="calc-result-grid">
            <div class="calc-stat danger"><div class="calc-stat-label">Zapier / {'Año' if is_es else 'Year'}</div><div class="calc-stat-val" id="n8nZapierYr">$5,748</div></div>
            <div class="calc-stat"><div class="calc-stat-label">Make / {'Año' if is_es else 'Year'}</div><div class="calc-stat-val" id="n8nMakeYr">$1,284</div></div>
            <div class="calc-stat highlight"><div class="calc-stat-label">n8n Self-Host</div><div class="calc-stat-val" id="n8nSelfYr">$180</div></div>
          </div>
          <div class="calc-stat highlight" style="padding:1.05rem;">
            <div class="calc-stat-label" style="color:var(--live);">{esc(d['lbl_save_head'])}</div>
            <div id="n8nSavingsHeadline" style="font-size:1.35rem; font-weight:800; color:var(--live); margin:0.25rem 0;"></div>
            <div id="n8nPaybackNote" style="font-size:0.84rem; color:var(--muted); margin-bottom:0.85rem;"></div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a id="n8nCtaPack" class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Get 15 n8n Workflows ($39)</a>
              <a class="btn" href="{GUMROAD_STORE}" target="_blank" rel="noopener">{esc(d['cta_box'])}</a>
            </div>
          </div>
        </div>
      </div>
    </section>"""
        calc_js = f"""
    (function() {{
      var isEs = {str(is_es).lower()};
      var runsEl = document.getElementById('n8nRuns'), stepsEl = document.getElementById('n8nSteps');
      if (!runsEl || !stepsEl) return;
      function fmt(n) {{ return '$' + Math.round(n).toLocaleString('en-US'); }}
      function update() {{
        var runs = Number(runsEl.value) || 10000, steps = Number(stepsEl.value) || 6;
        var tasks = runs * steps;
        var zapierMo = Math.max(29, Math.round(tasks * 0.0075 + 29));
        var makeMo = Math.max(11, Math.round(tasks * 0.0016 + 11));
        var n8nMo = 15;
        var zYr = zapierMo * 12, mYr = makeMo * 12, nYr = n8nMo * 12;
        var sZ = Math.max(0, zYr - nYr), sM = Math.max(0, mYr - nYr);
        var days = Math.max(1, Math.round(39 / Math.max(0.5, (zapierMo - n8nMo) / 30)));
        document.getElementById('n8nRunsVal').textContent = runs.toLocaleString('en-US') + (isEs ? ' ejec./mes' : ' runs/mo');
        document.getElementById('n8nStepsVal').textContent = steps + (isEs ? ' pasos' : ' steps');
        document.getElementById('n8nTasksTotal').textContent = tasks.toLocaleString('en-US') + (isEs ? ' tareas/mes' : ' tasks/mo');
        document.getElementById('n8nZapierYr').textContent = fmt(zYr) + (isEs ? '/año' : '/yr');
        document.getElementById('n8nMakeYr').textContent = fmt(mYr) + (isEs ? '/año' : '/yr');
        document.getElementById('n8nSelfYr').textContent = fmt(nYr) + (isEs ? '/año' : '/yr');
        document.getElementById('n8nSavingsHeadline').textContent = isEs
          ? 'Ahorra ' + fmt(sZ) + '/año vs Zapier · ' + fmt(sM) + '/año vs Make'
          : 'Save ' + fmt(sZ) + '/yr vs Zapier · ' + fmt(sM) + '/yr vs Make';
        document.getElementById('n8nPaybackNote').textContent = isEs
          ? 'El Pack de 15 Flujos n8n ($39) se paga solo en ~' + days + ' días de ahorro frente a Zapier.'
          : 'The $39 n8n Workflows Pack pays for itself in ~' + days + ' days of Zapier savings.';
        document.getElementById('n8nCtaPack').textContent = isEs
          ? 'Ahorra ' + fmt(sZ) + '/año — Pack 15 Flujos ($39) →'
          : 'Save ' + fmt(sZ) + '/yr — Get 15 Workflows ($39) →';
      }}
      runsEl.addEventListener('input', update); stepsEl.addEventListener('input', update); update();
    }})();"""
        return calc_html, calc_js

    if slug == "aws-finops-open-source-tools":
        calc_html = f"""
    <section class="card section" style="margin-top:1.5rem;">
      <span class="tag tag-gold">{'ESTIMADOR EN VIVO AWS + LLM' if is_es else 'LIVE AWS + LLM WASTE ESTIMATOR'}</span>
      <h2 style="margin:0.5rem 0 1rem; font-size:1.3rem;">{esc(d['calc_title'])}</h2>
      <div class="sandbox-grid">
        <div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="finAwsSpend"><strong>{esc(d['lbl_aws'])}</strong></label><span class="calc-slider-val" id="finAwsSpendVal">$8,000</span></div>
            <input id="finAwsSpend" type="range" min="1000" max="50000" step="500" value="8000" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="finWastePct"><strong>{esc(d['lbl_pct'])}</strong></label><span class="calc-slider-val" id="finWastePctVal">28%</span></div>
            <input id="finWastePct" type="range" min="10" max="45" step="1" value="28" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="finLlmSpend"><strong>{esc(d['lbl_llm'])}</strong></label><span class="calc-slider-val" id="finLlmSpendVal">$2,400</span></div>
            <input id="finLlmSpend" type="range" min="200" max="20000" step="200" value="2400" />
          </div>
        </div>
        <div>
          <div class="calc-result-grid">
            <div class="calc-stat danger"><div class="calc-stat-label">{'Desperdicio/Mes' if is_es else 'Monthly Waste'}</div><div class="calc-stat-val" id="finMonthlyWaste">$3,080</div></div>
            <div class="calc-stat danger"><div class="calc-stat-label">{'Desperdicio/Año' if is_es else 'Annual Waste'}</div><div class="calc-stat-val" id="finAnnualWaste">$36,960</div></div>
            <div class="calc-stat highlight"><div class="calc-stat-label">{'Retorno $49' if is_es else '$49 Payback'}</div><div class="calc-stat-val" id="finPaybackHrs">11.5 h</div></div>
          </div>
          <div class="calc-stat highlight" style="padding:1.05rem;">
            <div class="calc-stat-label" style="color:var(--live);">{esc(d['lbl_rec'])}</div>
            <div id="finSummaryLine" style="font-size:1.25rem; font-weight:800; margin:0.25rem 0;"></div>
            <div id="finPaybackDetail" style="font-size:0.84rem; color:var(--muted); margin-bottom:0.85rem;"></div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a class="btn" href="{FINOPS_REPO}" target="_blank" rel="noopener">{'Clonar CLI Gratis ($0)' if is_es else 'Clone Free CLI ($0)'}</a>
              <a id="finCtaPro" class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Unlock Pro ($49)</a>
            </div>
          </div>
        </div>
      </div>
    </section>"""
        calc_js = f"""
    (function() {{
      var isEs = {str(is_es).lower()};
      var awsEl = document.getElementById('finAwsSpend'), pctEl = document.getElementById('finWastePct'), llmEl = document.getElementById('finLlmSpend');
      if (!awsEl || !pctEl || !llmEl) return;
      function fmt(n) {{ return '$' + Math.round(n).toLocaleString('en-US'); }}
      function update() {{
        var aws = Number(awsEl.value) || 8000, pct = Number(pctEl.value) || 28, llm = Number(llmEl.value) || 2400;
        var aW = Math.round(aws * (pct / 100)), lW = Math.round(llm * 0.35), mo = aW + lW, yr = mo * 12;
        var hrs = Math.max(0.5, 49 / Math.max(0.1, mo / 720));
        document.getElementById('finAwsSpendVal').textContent = fmt(aws) + (isEs ? '/mes' : '/mo');
        document.getElementById('finWastePctVal').textContent = pct + '%';
        document.getElementById('finLlmSpendVal').textContent = fmt(llm) + (isEs ? '/mes' : '/mo');
        document.getElementById('finMonthlyWaste').textContent = fmt(mo) + (isEs ? '/mes' : '/mo');
        document.getElementById('finAnnualWaste').textContent = fmt(yr) + (isEs ? '/año' : '/yr');
        document.getElementById('finPaybackHrs').textContent = hrs.toFixed(1) + ' h';
        document.getElementById('finSummaryLine').textContent = fmt(aW) + ' AWS + ' + fmt(lW) + ' LLM = ' + fmt(yr) + (isEs ? '/año' : '/yr');
        document.getElementById('finPaybackDetail').textContent = isEs
          ? 'La licencia Pro ($49) se paga sola en ' + hrs.toFixed(1) + ' horas de operación.'
          : 'The $49 Pro License pays back in ' + hrs.toFixed(1) + ' hours of cloud operation.';
        document.getElementById('finCtaPro').textContent = isEs
          ? 'Recupera ' + fmt(yr) + '/año — Desbloquear Pro ($49) →'
          : 'Recover ' + fmt(yr) + '/yr — Unlock Pro ($49) →';
      }}
      [awsEl, pctEl, llmEl].forEach(function(e){{ e.addEventListener('input', update); }}); update();
    }})();"""
        return calc_html, calc_js

    # clinic-whatsapp-ai-bot-roi
    calc_html = f"""
    <section class="card section" style="margin-top:1.5rem;">
      <span class="tag tag-live">{'CALCULADORA EN VIVO PARA CLÍNICAS' if is_es else 'LIVE CLINIC REVENUE CALCULATOR'}</span>
      <h2 style="margin:0.5rem 0 1rem; font-size:1.3rem;">{esc(d['calc_title'])}</h2>
      <div class="sandbox-grid">
        <div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="clInquiries"><strong>{esc(d['lbl_inq'])}</strong></label><span class="calc-slider-val" id="clInquiriesVal">300</span></div>
            <input id="clInquiries" type="range" min="50" max="2000" step="25" value="300" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="clNoShowPct"><strong>{esc(d['lbl_ns'])}</strong></label><span class="calc-slider-val" id="clNoShowPctVal">22%</span></div>
            <input id="clNoShowPct" type="range" min="5" max="45" step="1" value="22" />
          </div>
          <div class="calc-slider-group">
            <div class="calc-slider-head"><label for="clAvgConsult"><strong>{esc(d['lbl_val'])}</strong></label><span class="calc-slider-val" id="clAvgConsultVal">$75</span></div>
            <input id="clAvgConsult" type="range" min="25" max="350" step="5" value="75" />
          </div>
        </div>
        <div>
          <div class="calc-result-grid">
            <div class="calc-stat"><div class="calc-stat-label">{'Citas/Mes' if is_es else 'Visits/Mo'}</div><div class="calc-stat-val" id="clRecVisits">43</div></div>
            <div class="calc-stat highlight"><div class="calc-stat-label">{'Recuperado/Mes' if is_es else 'Monthly'}</div><div class="calc-stat-val" id="clRecMonth">$3,225</div></div>
            <div class="calc-stat highlight"><div class="calc-stat-label">{'Recuperado/Año' if is_es else 'Annual'}</div><div class="calc-stat-val" id="clRecYear">$38,700</div></div>
          </div>
          <div class="calc-stat highlight" style="padding:1.05rem;">
            <div class="calc-stat-label" style="color:var(--live);">{esc(d['lbl_impact'])}</div>
            <div id="clSummaryLine" style="font-size:1.25rem; font-weight:800; margin:0.25rem 0;"></div>
            <div id="clPaybackLine" style="font-size:0.84rem; color:var(--muted); margin-bottom:0.85rem;"></div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <a id="clCtaWorkflow" class="btn btn-primary" href="{GUMROAD_STORE}" target="_blank" rel="noopener">Get Workflow ($39)</a>
              <a class="btn" href="mailto:gabhack@gmail.com?subject=ClinicFlow%207-Day%20Pilot">{'Reservar Piloto 7 Días ($690)' if is_es else 'Book 7-Day Pilot ($690)'}</a>
            </div>
          </div>
        </div>
      </div>
    </section>"""
    calc_js = f"""
    (function() {{
      var isEs = {str(is_es).lower()};
      var inqEl = document.getElementById('clInquiries'), nsEl = document.getElementById('clNoShowPct'), valEl = document.getElementById('clAvgConsult');
      if (!inqEl || !nsEl || !valEl) return;
      function fmt(n) {{ return '$' + Math.round(n).toLocaleString('en-US'); }}
      function update() {{
        var inq = Number(inqEl.value) || 300, ns = Number(nsEl.value) || 22, ticket = Number(valEl.value) || 75;
        var missed = Math.round(inq * (ns / 100)), rec = Math.max(1, Math.round(missed * 0.65));
        var mo = rec * ticket, yr = mo * 12, days = Math.max(1, Math.round(690 / Math.max(1, mo / 30)));
        document.getElementById('clInquiriesVal').textContent = inq.toLocaleString('en-US') + (isEs ? '/mes' : '/mo');
        document.getElementById('clNoShowPctVal').textContent = ns + '%';
        document.getElementById('clAvgConsultVal').textContent = fmt(ticket);
        document.getElementById('clRecVisits').textContent = rec + (isEs ? ' citas' : ' visits');
        document.getElementById('clRecMonth').textContent = fmt(mo) + (isEs ? '/mes' : '/mo');
        document.getElementById('clRecYear').textContent = fmt(yr) + (isEs ? '/año' : '/yr');
        document.getElementById('clSummaryLine').textContent = isEs
          ? 'Recupera ' + fmt(mo) + '/mes (' + fmt(yr) + '/año) de ' + missed + ' espacios perdidos'
          : 'Recover ' + fmt(mo) + '/mo (' + fmt(yr) + '/yr) from ' + missed + ' missed slots';
        document.getElementById('clPaybackLine').textContent = isEs
          ? 'El Piloto de $690 se paga en ~' + days + ' días; el flujo n8n de $39 se paga con el primer paciente.'
          : 'The $690 Pilot pays back in ~' + days + ' days; the $39 n8n workflow pays back on patient #1.';
        document.getElementById('clCtaWorkflow').textContent = isEs
          ? 'Recupera ' + fmt(yr) + '/año — Flujo n8n ($39) →'
          : 'Recover ' + fmt(yr) + '/yr — Get n8n Workflow ($39) →';
      }}
      [inqEl, nsEl, valEl].forEach(function(e){{ e.addEventListener('input', update); }}); update();
    }})();"""
    return calc_html, calc_js


def build_compare_html(cmp_item: dict, lang: str) -> str:
    is_es = lang == "es"
    slug = cmp_item["slug"]
    d = cmp_item[lang]
    root_rel = "../../../" if is_es else "../../"
    home_href = "../../"
    en_href = f"../../../compare/{slug}/" if is_es else "./"
    es_href = "./" if is_es else f"../../es/compare/{slug}/"
    rel_path = f"compare/{slug}/"
    og_file = f"es-{slug}.png" if is_es else f"{slug}.png"

    calc_html, calc_js = build_compare_calc_html_and_js(slug, d, lang)
    ths = "".join(f"<th>{esc(h)}</th>" for h in d["table_headers"])
    trs = "".join("<tr>" + "".join(f"<td>{('<strong>' + esc(c) + '</strong>') if i == 0 else esc(c)}</td>" for i, c in enumerate(r)) + "</tr>" for r in d["table_rows"])
    faqs_html = "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in d["faqs"])

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "TuringTec Agent Studio", "item": f"{BASE_URL}/{'es/' if is_es else ''}"},
                    {"@type": "ListItem", "position": 2, "name": d["short_title"], "item": f"{BASE_URL}/{'es/' if is_es else ''}{rel_path}"},
                ],
            },
            {"@type": "WebApplication", "name": d["title"], "description": d["meta_desc"], "applicationCategory": "BusinessApplication", "inLanguage": lang},
            {"@type": "FAQPage", "inLanguage": lang, "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]},
        ],
    }

    body = f"""<body class="ambient-bg">
{render_navbar(lang, home_href, en_href, es_href)}
  <main class="container">
    <div style="font-size:0.82rem; color:var(--muted); margin-bottom:1rem;">
      <a href="{home_href}" style="color:var(--brand-hover); text-decoration:none;">TuringTec Agent Studio</a> / {esc(d['short_title'])}
    </div>
    <section style="padding:0.25rem 0 1rem; max-width:860px;">
      <div class="status-pill"><span class="live-dot"></span><span>{esc(d['badge'])}</span></div>
      <h1 style="margin:0 0 0.8rem; font-size:clamp(1.85rem, 3.6vw, 2.75rem);">{esc(d['title'])}</h1>
      <p class="hero-lead" style="max-width:74ch;">{esc(d['intro'])}</p>
      <div class="guarantee-bar" style="margin-top:1rem;">
        <div><strong>{'Resumen Ejecutivo:' if is_es else 'Bottom Line:'}</strong> <span style="color:var(--muted); font-size:0.9rem;">{esc(d['bluf'])}</span></div>
      </div>
    </section>
{calc_html}
    <section class="card section" style="margin-top:1.75rem;">
      <h2 style="margin:0 0 0.6rem; font-size:1.25rem;">{'Comparativa Detallada' if is_es else 'Side-by-Side Comparison'}</h2>
      <div style="overflow-x:auto;"><table class="data-table"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>
    </section>
    <section class="section">
      <div class="section-header"><h2>{'Preguntas Frecuentes' if is_es else 'Frequently Asked Questions'}</h2></div>
      <div class="faq-list">{faqs_html}</div>
    </section>
{render_footer(lang, root_rel)}
  </main>
  <script src="{root_rel}studio.js"></script>
  <script>{calc_js}</script>
</body>
</html>"""
    return render_head(f"{d['title']} | TuringTec Agent Studio", d["meta_desc"], lang, rel_path, og_file, f"{root_rel}styles.css", json_ld) + "\n" + body


def main() -> None:
    og_dir = ROOT / "assets" / "og"

    # 1. Homes (EN + ES)
    (ROOT / "index.html").write_text(build_home_html("en"), encoding="utf-8")
    (ROOT / "es").mkdir(exist_ok=True)
    (ROOT / "es" / "index.html").write_text(build_home_html("es"), encoding="utf-8")
    make_og(og_dir / "home.png", "Production AI Agents · BYOK", "Deploy AI Agents That Quote, Book & Cut AWS Waste 24/7", "4 live browser sandboxes + self-hosted n8n kits ($39-$99) + 7-day turnkey pilots.", (37, 99, 235), "en")
    make_og(og_dir / "es-home.png", "Agentes IA B2B · Código Propio", "Agentes IA que Cotizan, Agendan y Podan tu AWS 24/7", "4 demos en vivo sin registro + kits self-hosted n8n ($39-$99) + piloto 7 días.", (37, 99, 235), "es")

    sitemap_pairs: list[tuple[str, str, str]] = [("", "1.0", "home")]
    llms = [
        "# TuringTec Agent Studio — Bilingual (EN + ES) Production B2B AI Agents, MCP Servers & n8n Kits",
        "",
        f"- English Storefront (4 Live Sandboxes): {BASE_URL}/",
        f"- Spanish Storefront (4 Demos en Vivo): {BASE_URL}/es/",
        f"- Gumroad Official Store ($39–$99 Kits): {GUMROAD_STORE}",
        f"- Open-Core AWS FinOps CLI + MCP: {FINOPS_REPO}",
        f"- Apify Dual-Mode MCP Suite: {APIFY_REPO}",
        f"- CloudCert Lab Simulator: {CLOUDCERT_URL}",
        "",
        "## Vertical Solutions (EN & ES)",
    ]
    full = list(llms) + ["", "---", ""]

    # 2. Solutions (6 EN + 6 ES)
    for sol in SOLUTIONS:
        slug = sol["slug"]
        for lang in ("en", "es"):
            out_dir = (ROOT / "es" / "solutions" / slug) if lang == "es" else (ROOT / "solutions" / slug)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(build_solution_html(sol, lang), encoding="utf-8")
            og_name = f"es-{slug}.png" if lang == "es" else f"{slug}.png"
            make_og(og_dir / og_name, sol[lang]["badge"], sol[lang]["short_title"], sol[lang]["meta_desc"], sol["accent"], lang)
        sitemap_pairs.append((f"solutions/{slug}/", "0.9", slug))
        llms.append(f"- [{sol['en']['short_title']} (EN)]({BASE_URL}/solutions/{slug}/) | [Español]({BASE_URL}/es/solutions/{slug}/)")
        full.append(f"### {sol['en']['title']} / {sol['es']['title']}")
        full.append(f"- EN: {BASE_URL}/solutions/{slug}/ | ES: {BASE_URL}/es/solutions/{slug}/")
        full.append(f"- Pricing: {sol['en']['price_kit']} | {sol['en']['price_pilot']}")
        full.append("")

    # 3. Compare ROI Calculators (3 EN + 3 ES)
    llms.append("")
    llms.append("## Interactive ROI Calculators (EN & ES)")
    for cmp_item in COMPARES:
        slug = cmp_item["slug"]
        for lang in ("en", "es"):
            out_dir = (ROOT / "es" / "compare" / slug) if lang == "es" else (ROOT / "compare" / slug)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(build_compare_html(cmp_item, lang), encoding="utf-8")
            og_name = f"es-{slug}.png" if lang == "es" else f"{slug}.png"
            make_og(og_dir / og_name, cmp_item[lang]["badge"], cmp_item[lang]["short_title"], cmp_item[lang]["meta_desc"], cmp_item["accent"], lang)
        sitemap_pairs.append((f"compare/{slug}/", "0.9", slug))
        llms.append(f"- [{cmp_item['en']['short_title']} (EN)]({BASE_URL}/compare/{slug}/) | [Español]({BASE_URL}/es/compare/{slug}/)")
        full.append(f"### {cmp_item['en']['title']} / {cmp_item['es']['title']}")
        full.append(f"- EN: {BASE_URL}/compare/{slug}/ | ES: {BASE_URL}/es/compare/{slug}/")
        full.append(f"- BLUF: {cmp_item['en']['bluf']}")
        full.append("")

    # 4. Multilingual hreflang sitemap.xml (20 URLs)
    url_blocks = []
    for rel, prio, _ in sitemap_pairs:
        en_u = f"{BASE_URL}/{rel}" if rel else f"{BASE_URL}/"
        es_u = f"{BASE_URL}/es/{rel}" if rel else f"{BASE_URL}/es/"
        for loc in (en_u, es_u):
            url_blocks.append(
                f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>{prio}</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{en_u}" />
    <xhtml:link rel="alternate" hreflang="es" href="{es_u}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{en_u}" />
  </url>"""
            )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(url_blocks)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    (ROOT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    (ROOT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (ROOT / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")
    print(f"OK: Generated {len(url_blocks)} bilingual pages (10 EN + 10 ES) + {len(url_blocks)} OG PNGs + hreflang sitemap.xml + llms-full.txt")


if __name__ == "__main__":
    main()
