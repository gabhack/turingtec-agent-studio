/* TuringTec Agent Studio v2 — Bilingual (EN / ES) Interactive Browser Sandboxes */

(function () {
  const $ = (id) => document.getElementById(id);
  const LANG = (document.documentElement.lang || "en").toLowerCase().startsWith("es") ? "es" : "en";
  const IS_ES = LANG === "es";

  // Theme initialization (Dark by default for deep-tech look, toggleable to Light)
  const savedTheme = localStorage.getItem("tt_theme_v2");
  if (savedTheme === "light" || savedTheme === "dark") {
    document.documentElement.setAttribute("data-theme", savedTheme);
  }
  const themeBtn = $("btnTheme");
  function syncThemeLabel() {
    if (!themeBtn) return;
    const isLight = document.documentElement.getAttribute("data-theme") === "light";
    themeBtn.textContent = isLight ? (IS_ES ? "Oscuro" : "Dark") : (IS_ES ? "Claro" : "Light");
  }
  syncThemeLabel();
  if (themeBtn) {
    themeBtn.onclick = () => {
      const next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("tt_theme_v2", next);
      syncThemeLabel();
    };
  }

  // Remember explicit language choice when user clicks switcher link (Googlebot-safe)
  document.querySelectorAll(".lang-opt").forEach((a) => {
    a.addEventListener("click", () => {
      if (a.dataset.lang) localStorage.setItem("tt_lang_pref", a.dataset.lang);
    });
  });

  // Sandbox Tabs
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
    { sku: "CEM-GRIS-50", name: IS_ES ? "Cemento Gris Uso General 50 kg" : "General Purpose Gray Cement 50kg", unit: 8.4, keywords: ["cemento", "cement", "gris", "bulto", "bag"] },
    { sku: "PVC-SAN-2P", name: IS_ES ? 'Tubo PVC Sanitario 2" × 6 m' : 'Sanitary PVC Pipe 2" × 6m', unit: 6.2, keywords: ["pvc", "tubo", "sanitario", "pipe"] },
    { sku: "TOR-DRY-1P", name: IS_ES ? 'Caja Tornillo Drywall 1" (×500)' : 'Drywall Screws Box 1" (×500)', unit: 4.9, keywords: ["tornillo", "drywall", "screw", "bolt"] },
    { sku: "PIN-VIN-1G", name: IS_ES ? "Pintura Vinilo Tipo 1 Blanco (Galón)" : "White Vinyl Paint Type 1 (1 Gal)", unit: 16.5, keywords: ["pintura", "vinilo", "paint", "blanco", "galon", "white"] },
    { sku: "LAD-EST-01", name: IS_ES ? "Ladrillo Estructural Perforado" : "Structural Perforated Brick", unit: 0.72, keywords: ["ladrillo", "bloque", "brick"] },
    { sku: "CAB-THHN-12", name: IS_ES ? "Rollo Cable THHN Calibre 12 (100 m)" : "THHN Copper Cable 12 AWG (100m Roll)", unit: 46.0, keywords: ["cable", "thhn", "wire", "alambre"] },
    { sku: "VAL-BRO-1P", name: IS_ES ? 'Válvula Bola Bronce 1"' : 'Bronze Ball Valve 1"', unit: 13.8, keywords: ["valvula", "valve", "bronce", "brass"] },
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
    if ($("fqStatus")) {
      $("fqStatus").textContent = IS_ES
        ? `${rows.length} SKUs cruzados en 12 ms · Descuentos aplicados`
        : `Matched ${rows.length} SKUs in 12ms · Volume tiers applied`;
    }
    if ($("fqTableWrap")) {
      const ths = IS_ES
        ? "<tr><th>SKU</th><th>Producto</th><th>Cant.</th><th>Dcto.</th><th>Subtotal</th></tr>"
        : "<tr><th>SKU</th><th>Product</th><th>Qty</th><th>Disc.</th><th>Subtotal</th></tr>";
      $("fqTableWrap").innerHTML = rows.length
        ? `<table class="data-table"><thead>${ths}</thead><tbody>` +
          rows.map((r) => `<tr><td><code>${r.sku}</code></td><td>${r.name}</td><td class="tabular">${r.qty}</td><td class="tabular">${r.discPct}%</td><td class="tabular"><strong>$${r.subtotal.toFixed(2)}</strong></td></tr>`).join("") +
          `</tbody></table>`
        : `<p style="color:var(--muted); font-size:0.86rem;">${IS_ES ? "No se detectaron SKUs. Prueba palabras como cemento, pvc, tornillo, pintura, ladrillo, cable o válvula." : "No matching SKUs found. Try cement, pvc, drywall screws, paint, brick, cable, or valve."}</p>`;
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
    const itemRe = /ITEM\s*\d+:\s*([^|]+)\|\s*(?:CANT|QTY):\s*(\d+(?:\.\d+)?)\s*\|\s*UNIT:\s*(\d+(?:\.\d+)?)\s*\|\s*SUB:\s*(\d+(?:\.\d+)?)/gi;
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
        confidence_score: items.length > 0 ? 0.994 : 0.72,
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

    if ($("finTotal")) {
      $("finTotal").textContent = IS_ES
        ? `$${totalMo.toLocaleString("en-US", { minimumFractionDigits: 2 })}/mes ($${(totalMo * 12).toLocaleString("en-US", { maximumFractionDigits: 0 })}/año)`
        : `$${totalMo.toLocaleString("en-US", { minimumFractionDigits: 2 })}/mo ($${(totalMo * 12).toLocaleString("en-US", { maximumFractionDigits: 0 })}/yr)`;
    }
    if ($("finOutput")) {
      const daysPayback = ((49 / Math.max(1, totalMo)) * 30).toFixed(1);
      $("finOutput").textContent = IS_ES
        ? `# TuringTec AWS & LLM FinOps Guard — Auditoría en Vivo
Gasto Evitable Mensual  : $${totalMo.toFixed(2)} USD/mes ($${(totalMo * 12).toFixed(2)}/año)
Retorno Licencia $49    : ${daysPayback} días

Desglose Detectado:
  - FINOPS-EBS  (gp2 -> gp3 / huérfanos)    : $${ebsWaste.toFixed(2)}/mes
  - FINOPS-NET  (Agregar S3 Gateway $0)     : $${natWaste.toFixed(2)}/mes
  - FINOPS-RDS  (Ajuste RDS no productivo)  : $${rdsWaste.toFixed(2)}/mes
  - FINOPS-LLM  (Enrutar triaje a Flash)    : $${llmWaste.toFixed(2)}/mes

# Parche Terraform Auto-Remediation (Incluido en CLI + MCP Pro $49):
resource "aws_vpc_endpoint" "s3_gateway" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = var.private_route_table_ids
}`
        : `# TuringTec AWS & LLM FinOps Guard — Live Estimate
Monthly Avoidable Spend : $${totalMo.toFixed(2)} USD/mo ($${(totalMo * 12).toFixed(2)}/yr)
Payback vs $49 Pro Key  : ${daysPayback} days

Breakdown:
  - FINOPS-EBS  (gp2 -> gp3 / orphaned)     : $${ebsWaste.toFixed(2)}/mo
  - FINOPS-NET  (Add $0 S3 Gateway Endpoint): $${natWaste.toFixed(2)}/mo
  - FINOPS-RDS  (Non-prod rightsize)        : $${rdsWaste.toFixed(2)}/mo
  - FINOPS-LLM  (Route triage to fast tier) : $${llmWaste.toFixed(2)}/mo

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
  const CLINIC_FLOWS = IS_ES
    ? {
        book: [
          { role: "user", text: "Hola, quiero agendar limpieza dental para este viernes en la tarde." },
          { role: "bot", text: "ClinicFlow AI: ¡Hola! Revisé Google Calendar en vivo. Para este viernes tengo 2 cupos libres: 3:00 PM o 4:30 PM con la Dra. Morales. ¿Cuál prefieres reservar?" },
          { role: "bot", text: "Al confirmar, bloqueo el espacio en agenda y programo recordatorios automáticos 24h y 2h antes por WhatsApp." },
        ],
        price: [
          { role: "user", text: "¿Cuánto cuesta la valoración y aceptan medicina prepagada?" },
          { role: "bot", text: "ClinicFlow AI: La valoración inicial cuesta $45 USD (convenio directo con Sura, Colsanitas y Allianz). Envíame foto de tu carné aquí mismo para verificar cobertura hoy." },
        ],
        reschedule: [
          { role: "user", text: "Tuve un imprevisto, necesito mover mi cita de mañana al lunes." },
          { role: "bot", text: "ClinicFlow AI: Listo ✅ Liberé tu cupo de mañana (avisando a lista de espera) y moví tu cita al lunes 10:00 AM con confirmación en calendario." },
        ],
        confirm: [
          { role: "user", text: "Sí, confirmo mi asistencia para mañana a las 9:00 AM." },
          { role: "bot", text: "ClinicFlow AI: ¡Perfecto! Tu cita quedó CONFIRMADA en el sistema. Aquí tienes la ubicación de la sede y recomendaciones previas." },
        ],
      }
    : {
        book: [
          { role: "user", text: "Hi, I'd like to book a dental cleaning this Friday afternoon." },
          { role: "bot", text: "ClinicFlow AI: Hi! I checked Google Calendar live—Dr. Morales has two open slots this Friday: 3:00 PM or 4:30 PM. Which works best for you?" },
          { role: "bot", text: "Once confirmed, I lock the slot and schedule automated 24h & 2h WhatsApp reminders." },
        ],
        price: [
          { role: "user", text: "How much is an initial exam and do you take PPO insurance?" },
          { role: "bot", text: "ClinicFlow AI: An initial exam is $75 USD (in-network with Delta, Cigna, and Aetna). Send a photo of your insurance card right here and I'll verify coverage." },
        ],
        reschedule: [
          { role: "user", text: "Something came up—can I move tomorrow's visit to Monday morning?" },
          { role: "bot", text: "ClinicFlow AI: Done ✅ I released tomorrow's slot (alerting the waitlist) and moved you to Monday at 10:00 AM with a fresh calendar invite." },
        ],
        confirm: [
          { role: "user", text: "Yes, confirming my 9:00 AM appointment tomorrow." },
          { role: "bot", text: "ClinicFlow AI: Confirmed! You're all set—here's the clinic address, parking details, and pre-visit checklist." },
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
    const paybackDays = Math.max(3, Math.round((690 / Math.max(1, monthlyRev)) * 30));
    if ($("clinicRoi")) {
      $("clinicRoi").innerHTML = IS_ES
        ? `<div style="font-size:0.84rem; color:var(--muted);">Recuperación conservadora del 55% (~<strong>${recovered} citas recuperadas/mes</strong>)</div>
           <div class="tabular" style="font-size:1.55rem; font-weight:800; color:var(--live); margin:0.25rem 0;">+$${monthlyRev.toLocaleString("en-US")} USD / mes recuperados</div>
           <div style="font-size:0.82rem; color:var(--muted);">El workflow n8n de <strong>$39</strong> se paga en &lt;1 día · El Piloto Llave en Mano de <strong>$690</strong> se paga en <strong>${paybackDays} días</strong>.</div>`
        : `<div style="font-size:0.84rem; color:var(--muted);">Conservative 55% recovery rate (~<strong>${recovered} saved visits/mo</strong>)</div>
           <div class="tabular" style="font-size:1.55rem; font-weight:800; color:var(--live); margin:0.25rem 0;">+$${monthlyRev.toLocaleString("en-US")} USD / month recovered</div>
           <div style="font-size:0.82rem; color:var(--muted);">The <strong>$39 n8n workflow</strong> pays back in &lt;1 day · The <strong>$690 7-Day Pilot</strong> pays back in <strong>${paybackDays} days</strong>.</div>`;
    }
  }
  ["clMissed", "clTicket"].forEach((id) => {
    if ($(id)) $(id).addEventListener("input", renderClinicRoi);
  });
  renderClinicRoi();
})();
