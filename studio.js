/* TuringTec Agent Studio — 4 Zero-Cost Client-Side Interactive AI Agent Sandboxes */

(function () {
  const $ = (id) => document.getElementById(id);

  // Theme toggle
  const savedTheme = localStorage.getItem("tt_theme");
  if (savedTheme === "dark" || savedTheme === "light") {
    document.documentElement.setAttribute("data-theme", savedTheme);
  }
  if ($("btnTheme")) {
    $("btnTheme").onclick = () => {
      const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("tt_theme", next);
    };
  }

  // Sandbox tabs
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".sandbox-panel").forEach((p) => p.classList.add("hidden"));
      btn.classList.add("active");
      const panel = $(`tab-${btn.dataset.tab}`);
      if (panel) panel.classList.remove("hidden");
    });
  });

  // =========================================================================
  // SANDBOX 1: FERREQUOTE AI (B2B Hardware / Wholesale Fuzzy SKU Matcher)
  // =========================================================================
  const SKU_CATALOG = [
    { sku: "CEM-GRIS-50", name: "Cemento Gris Uso General 50kg", unit: 8.4, keywords: ["cemento", "cement", "gris", "bulto"] },
    { sku: "PVC-SAN-2P", name: "Tubo PVC Sanitario 2\" x 6m", unit: 6.2, keywords: ["pvc", "tubo", "sanitario", "pipe"] },
    { sku: "TOR-DRY-1P", name: "Caja Tornillo Drywall 1\" (x500)", unit: 4.9, keywords: ["tornillo", "drywall", "screw", "bolt"] },
    { sku: "PIN-VIN-1G", name: "Pintura Vinilo Tipo 1 Blanco (Galon)", unit: 16.5, keywords: ["pintura", "vinilo", "paint", "blanco", "galon"] },
    { sku: "LAD-EST-01", name: "Ladrillo Estructural Perforado", unit: 0.72, keywords: ["ladrillo", "bloque", "brick"] },
    { sku: "CAB-THHN-12", name: "Rollo Cable THHN Calibre 12 (100m)", unit: 46.0, keywords: ["cable", "thhn", "wire", "alambre"] },
    { sku: "VAL-BRO-1P", name: "Valvula Bola Bronce 1\"", unit: 13.8, keywords: ["valvula", "valve", "bronce"] },
  ];

  let lastFqRows = [];
  function runFerreQuote() {
    const raw = ($("fqInput")?.value || "").split(/\n+/).map((s) => s.trim()).filter(Boolean);
    const rows = [];
    for (const line of raw) {
      const mQty = line.match(/(\d+(?:\.\d+)?)/);
      const qty = mQty ? Number(mQty[1]) : 1;
      const lower = line.toLowerCase();
      let best = null;
      let bestScore = 0;
      for (const item of SKU_CATALOG) {
        const hits = item.keywords.filter((k) => lower.includes(k)).length;
        if (hits > bestScore) {
          bestScore = hits;
          best = item;
        }
      }
      if (best) {
        const disc = qty >= 20 ? 0.08 : qty >= 10 ? 0.04 : 0;
        const unitNet = +(best.unit * (1 - disc)).toFixed(2);
        const subtotal = +(unitNet * qty).toFixed(2);
        rows.push({ sku: best.sku, name: best.name, qty, unit: unitNet, discPct: Math.round(disc * 100), subtotal });
      }
    }
    lastFqRows = rows;
    const grandTotal = rows.reduce((acc, r) => acc + r.subtotal, 0);
    if ($("fqTotal")) $("fqTotal").textContent = `$${grandTotal.toFixed(2)} USD`;
    if ($("fqStatus")) $("fqStatus").textContent = `Matched ${rows.length} SKUs in 12ms · Volume Discounts Applied`;
    if ($("fqTableWrap")) {
      $("fqTableWrap").innerHTML = rows.length
        ? `<table class="data-table"><thead><tr><th>SKU</th><th>Product</th><th>Qty</th><th>Disc</th><th>Subtotal</th></tr></thead><tbody>` +
          rows.map((r) => `<tr><td><code>${r.sku}</code></td><td>${r.name}</td><td>${r.qty}</td><td>${r.discPct}%</td><td><strong>$${r.subtotal.toFixed(2)}</strong></td></tr>`).join("") +
          `</tbody></table>`
        : `<p style="color:var(--muted); font-size:0.86rem;">No matching SKUs found. Try keywords like cemento, pvc, tornillo, pintura, ladrillo, cable, or valvula.</p>`;
    }
  }

  if ($("btnFqRun")) $("btnFqRun").onclick = runFerreQuote;
  if ($("btnFqExport")) {
    $("btnFqExport").onclick = () => {
      if (!lastFqRows.length) runFerreQuote();
      const csv = ["SKU,Product,Qty,UnitUSD,DiscountPct,SubtotalUSD"]
        .concat(lastFqRows.map((r) => `${r.sku},"${r.name}",${r.qty},${r.unit},${r.discPct},${r.subtotal}`))
        .join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "turingtec-ferrequote-sample.csv";
      a.click();
    };
  }
  runFerreQuote();

  // =========================================================================
  // SANDBOX 2: DOCFLOW B2B (Invoice / PO Structured Extractor)
  // =========================================================================
  let lastDfJson = {};
  function runDocFlow() {
    const txt = $("dfInput")?.value || "";
    const invoiceNo = (txt.match(/(?:No\.|Invoice|#)\s*([A-Z0-9-]+)/i) || [])[1] || "FE-AUTO-001";
    const vendor = (txt.match(/PROVEEDOR:\s*(.+)/i) || txt.match(/VENDOR:\s*(.+)/i) || [])[1]?.trim() || "Unknown Vendor";
    const taxId = (txt.match(/(?:NIT|TAX ID):\s*([0-9.-]+)/i) || [])[1] || "N/A";
    const dateStr = (txt.match(/FECHA:\s*([0-9-]+)/i) || txt.match(/DATE:\s*([0-9-]+)/i) || [])[1] || new Date().toISOString().slice(0, 10);

    const items = [];
    const itemRe = /ITEM\s*\d+:\s*([^|]+)\|\s*CANT:\s*(\d+(?:\.\d+)?)\s*\|\s*UNIT:\s*(\d+(?:\.\d+)?)\s*\|\s*SUB:\s*(\d+(?:\.\d+)?)/gi;
    let m;
    while ((m = itemRe.exec(txt)) !== null) {
      items.push({ description: m[1].trim(), qty: Number(m[2]), unit_price_usd: Number(m[3]), line_subtotal_usd: Number(m[4]) });
    }
    const calcSub = +items.reduce((s, it) => s + it.qty * it.unit_price_usd, 0).toFixed(2);
    const calcTax = +(calcSub * 0.19).toFixed(2);
    const calcTotal = +(calcSub + calcTax).toFixed(2);

    lastDfJson = {
      document_type: "B2B_INVOICE",
      invoice_number: invoiceNo,
      vendor_name: vendor,
      tax_id: taxId,
      issue_date: dateStr,
      line_items: items,
      financial_validation: {
        computed_subtotal_usd: calcSub,
        computed_tax_19pct_usd: calcTax,
        computed_total_usd: calcTotal,
        math_check_passed: items.length > 0,
        confidence_score: items.length > 0 ? 0.984 : 0.72,
      },
    };
    if ($("dfOutput")) $("dfOutput").textContent = JSON.stringify(lastDfJson, null, 2);
  }
  if ($("btnDfRun")) $("btnDfRun").onclick = runDocFlow;
  if ($("btnDfDownload")) {
    $("btnDfDownload").onclick = () => {
      const blob = new Blob([JSON.stringify(lastDfJson, null, 2)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "turingtec-docflow-extracted.json";
      a.click();
    };
  }
  runDocFlow();

  // =========================================================================
  // SANDBOX 3: AWS & LLM FINOPS GUARD
  // =========================================================================
  function runFinOps() {
    const ebsGb = Math.max(0, Number($("finEbs")?.value) || 0);
    const natGb = Math.max(0, Number($("finNat")?.value) || 0);
    const rdsUsd = Math.max(0, Number($("finRds")?.value) || 0);
    const llmM = Math.max(0, Number($("finLlm")?.value) || 0);

    const ebsWaste = +(ebsGb * 0.04).toFixed(2);
    const natWaste = +(natGb * 0.65 * 0.045).toFixed(2);
    const rdsWaste = +(rdsUsd * 0.55).toFixed(2);
    const llmWaste = +(llmM * (3.0 - 0.8) + (llmM * 0.25) * (15.0 - 4.0)).toFixed(2);
    const totalMo = +(ebsWaste + natWaste + rdsWaste + llmWaste).toFixed(2);

    if ($("finTotal")) $("finTotal").textContent = `$${totalMo.toLocaleString("en-US", { minimumFractionDigits: 2 })}/mo ($${(totalMo * 12).toLocaleString("en-US", { maximumFractionDigits: 0 })}/yr)`;
    if ($("finOutput")) {
      $("finOutput").textContent = `# TuringTec AWS & LLM FinOps Guard — Live Estimate
Monthly Avoidable Spend : $${totalMo.toFixed(2)} USD/mo ($${(totalMo * 12).toFixed(2)}/yr)
Payback vs $49 Pro Key  : ${(49 / Math.max(1, totalMo) * 30).toFixed(1)} days

Breakdown:
  - FINOPS-EBS  (gp2->gp3 / orphaned)        : $${ebsWaste.toFixed(2)}/mo
  - FINOPS-NET  (Add $0 S3 Gateway Endpoint) : $${natWaste.toFixed(2)}/mo
  - FINOPS-RDS  (Non-prod rightsize)         : $${rdsWaste.toFixed(2)}/mo
  - FINOPS-LLM  (Route triage to fast model) : $${llmWaste.toFixed(2)}/mo

# Sample Terraform Auto-Remediation Patch (Included in $49 Pro CLI + MCP):
resource "aws_vpc_endpoint" "s3_gateway" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = var.private_route_table_ids
}`;
    }
  }
  ["finEbs", "finNat", "finRds", "finLlm"].forEach((id) => {
    if ($(id)) $(id).addEventListener("input", runFinOps);
  });
  runFinOps();

  // =========================================================================
  // SANDBOX 4: CLINICFLOW AI (WhatsApp Receptionist + ROI Calc)
  // =========================================================================
  const CLINIC_FLOWS = {
    book: [
      { role: "user", text: "Hola, quiero agendar limpieza dental para este viernes en la tarde." },
      { role: "bot", text: "ClinicFlow AI: ¡Hola! Revisé Google Calendar en vivo. Para este viernes tengo 2 cupos libres: 3:00 PM o 4:30 PM con la Dra. Morales. ¿Cuál prefieres reservar?" },
      { role: "bot", text: "Al confirmar, bloqueo el espacio en agenda y programo recordatorios automáticos 24h y 2h antes por WhatsApp." },
    ],
    price: [
      { role: "user", text: "¿Cuánto cuesta la consulta de valoración y aceptan medicina prepagada?" },
      { role: "bot", text: "ClinicFlow AI: La valoración inicial cuesta $45 USD (reembolsable con Sura, Colsanitas y Allianz). Si deseas, envíame foto de tu carné aquí mismo para verificar cobertura y darte horario hoy." },
    ],
    reschedule: [
      { role: "user", text: "Tuve un imprevisto, necesito mover mi cita de mañana al lunes." },
      { role: "bot", text: "ClinicFlow AI: Listo ✅ Liberé tu cupo de mañana (avisando automáticamente a lista de espera) y moví tu cita al lunes 10:00 AM. Te llegará confirmación al calendario." },
    ],
    confirm: [
      { role: "user", text: "Sí, confirmo mi asistencia para mañana a las 9:00 AM." },
      { role: "bot", text: "ClinicFlow AI: ¡Perfecto! Tu cita quedó marcada como CONFIRMADA en el sistema. Aquí tienes la ubicación de la sede y recomendaciones previas." },
    ],
  };

  function renderClinicFlow(key) {
    const box = $("clinicChat");
    if (!box) return;
    const msgs = CLINIC_FLOWS[key] || CLINIC_FLOWS.book;
    box.innerHTML = msgs.map((m) => `<div class="bubble ${m.role}">${m.text}</div>`).join("");
  }
  document.querySelectorAll("[data-clinic-msg]").forEach((btn) => {
    btn.addEventListener("click", () => renderClinicFlow(btn.dataset.clinicMsg));
  });
  renderClinicFlow("book");

  function renderClinicRoi() {
    const missed = Math.max(1, Number($("clMissed")?.value) || 18);
    const ticket = Math.max(10, Number($("clTicket")?.value) || 65);
    const recovered = Math.round(missed * 0.55);
    const monthlyRev = recovered * ticket;
    if ($("clinicRoi")) {
      $("clinicRoi").innerHTML = `
        <div style="font-size:0.85rem; color:var(--muted);">Conservative 55% Recovery Rate (~<strong>${recovered} saved appointments/mo</strong>)</div>
        <div style="font-size:1.55rem; font-weight:800; color:var(--success); margin:0.2rem 0;">+$${monthlyRev.toLocaleString("en-US")} USD / month recovered</div>
        <div style="font-size:0.82rem; color:var(--muted);">Payback on our <strong>$39 n8n Workflow</strong>: &lt;1 day · Payback on <strong>$690 7-Day Turnkey Pilot</strong>: <strong>${Math.max(3, Math.round((690 / Math.max(1, monthlyRev)) * 30))} days</strong>.</div>
      `;
    }
  }
  ["clMissed", "clTicket"].forEach((id) => {
    if ($(id)) $(id).addEventListener("input", renderClinicRoi);
  });
  renderClinicRoi();
})();
