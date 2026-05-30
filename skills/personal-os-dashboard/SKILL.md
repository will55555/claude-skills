---
name: personal-os-dashboard
description: Build production-quality single-file HTML personal operating system dashboards — warm dark / light toggle command centers with tab navigation, data-driven card systems, live calculators, expandable sections, status pipelines, and optional AI-powered routing via the Anthropic API. Use this skill whenever the user wants to build, update, or extend a personal dashboard, command center, OS dashboard, financial OS, system overview, upgrade pipeline tracker, brokerage mandates page, consumer stack tracker, CRR calculator, or any interactive HTML tool that displays personal data across multiple tabs. Also use when the user says "update the page", "add a tab", "fix the colors", "switch the theme", or "update the file" in the context of an existing dashboard. Always use this skill before writing any dashboard HTML — it defines the design system, color tokens, light/dark toggle architecture, component patterns, and update methodology that prevent rework.
---

# Personal OS Dashboard Skill

A methodology for building and maintaining single-file HTML personal operating system dashboards — production-quality, warm-dark / light-toggling, data-driven, and built to evolve without rewriting.

---

## When to use this skill

- Building a new personal dashboard from scratch
- Adding a new tab or section to an existing dashboard
- Updating data, mandates, or rules in an existing dashboard
- Fixing colors, fonts, or layout in an existing dashboard
- Adding a new interactive feature (calculator, router, pipeline)
- Integrating an AI-powered routing feature via Anthropic API

---

## Core philosophy

Every dashboard built with this skill follows three rules:

1. **Single file** — all HTML, CSS, and JS inline in one `.html` file. No dependencies to install, no server to run. Download and open.
2. **Data-driven** — content is defined in JS arrays/objects and rendered by functions. Never hardcode cards or rows as static HTML. Changing data means changing one array, not hunting through markup.
3. **Iterative by design** — the file is built to be updated with surgical `str_replace` edits. The architecture anticipates change.

---

## Step 1 — Design decisions (ask before writing)

Before writing any code, confirm:

| Decision | Options | Notes |
|---|---|---|
| Mode | Dark default + light toggle | Always build both — see Step 2 |
| Colorway | Midnight Blue Red (default) / custom | User may feed a custom palette |
| Primary accent | Crimson (primary accent) / Blue (technical) / Green | Amber is default |
| Tab structure | Top-level tabs + sub-nav | Always two layers |
| Interactive features | Calculator / AI router / Pipeline / CRR tracker | Each has a pattern below |
| AI integration | Yes / No | Requires Anthropic API key modal |
| Data scope | What arrays need rendering | Define before writing HTML |

---

## Step 2 — Color system (always use CSS variables)

### Saved colorways — never overwrite, always add new ones

When the user provides a new colorway, add it here as a named entry. Never replace an existing one. Apply the user's chosen colorway to the files, but keep all previous colorways documented below for future use.

**Process for new colorways:**
1. User describes or names a palette
2. Propose the hex values and get confirmation before applying
3. Apply only after explicit user approval
4. Add the new colorway to this saved list
5. Leave all previous colorways intact

---

#### Colorway 1 — Warm Midnight Amber *(saved, not currently active)*

User-defined. Warm brown-black base with amber as primary accent and warm cream light mode.

```css
/* Dark */
--bg: #110F0A;  --s1: #1C1912;  --s2: #252118;  --s3: #2E2920;
--b1: #3D3526;  --b2: #524A38;
--t1: #F2EDE4;  --t2: #9C8E78;  --t3: #5E5242;
--amber: #F5A623;  --amber-d: #2A1E06;
--blue:  #4A8FE8;  --blue-d:  #0A1628;
--green: #52B96A;  --green-d: #071A0E;
--red:   #E05C5C;  --red-d:   #1E0808;

/* Light */
--bg: #FAF7F2;  --s1: #FFFFFF;  --s2: #F2EDE4;  --s3: #E8E0D4;
--b1: #DDD5C8;  --b2: #C9BFB0;
--t1: #1C1912;  --t2: #6B5E4E;  --t3: #9C8E78;
--amber-d: #FEF3DC;  --blue-d: #EBF2FD;
--green-d: #EDFAF1;  --red-d:  #FDEAEA;
```

---

#### Colorway 2 — Midnight Blue Red *(currently active)*

User-defined. Deep midnight blue base with crimson as primary accent and cool blue-white light mode.

```css
/* Dark */
--bg: #0A0D18;  --s1: #111628;  --s2: #181E32;  --s3: #1F273D;
--b1: #2E3A58;  --b2: #3D4D70;
--t1: #E8ECF8;  --t2: #8895BC;  --t3: #4A5680;
--amber: #E8354A;  --amber-d: #220810;   /* crimson primary */
--blue:  #5B8DEF;  --blue-d:  #080E20;
--green: #52B96A;  --green-d: #071A0E;
--red:   #E8354A;  --red-d:   #220810;

/* Light */
--bg: #F4F6FC;  --s1: #FFFFFF;  --s2: #EBF0FA;  --s3: #DDE4F5;
--b1: #C8D2EC;  --b2: #B0BDE0;
--t1: #0A0D18;  --t2: #4A5680;  --t3: #8895BC;
--amber-d: #FDEAEC;  --blue-d: #E8EEFF;
--green-d: #EDFAF1;  --red-d:  #FDEAEC;
```

---

### Default colorway — Midnight Blue Red + Cool Blue-White Light

The dashboard always ships with both dark and light mode defined. Switching is instant via a JS class toggle on `<html>`.

```css
/* ── DARK MODE (default) — Midnight Blue Red ── */
:root {
  --bg: #0A0D18;      /* deep midnight blue with faint red warmth */
  --s1: #111628;      /* card surface */
  --s2: #181E32;      /* secondary surface / hover */
  --s3: #1F273D;      /* tertiary / selected */
  --b1: #2E3A58;      /* border default — blue-gray */
  --b2: #3D4D70;      /* border hover */
  --t1: #E8ECF8;      /* primary text — cool blue-white */
  --t2: #8895BC;      /* secondary — muted periwinkle */
  --t3: #4A5680;      /* tertiary */

  /* Accents — same across both modes */
  --amber:  #E8354A;  --amber-d:  #220810;
  --blue:   #5B8DEF;  --blue-d:   #080E20;
  --green:  #52B96A;  --green-d:  #071A0E;
  --red:    #E8354A;  --red-d:    #220810;
  --purple: #8B7FE8;  --purple-d: #0E0B1E;
  --teal:   #2BB5A0;
  --r: 8px;  --r-sm: 5px;
}

/* ── LIGHT MODE — Cool Blue-White ── */
html.light {
  --bg: #F4F6FC;      /* cool blue-white */
  --s1: #FFFFFF;      /* card surface */
  --s2: #E8ECF8;      /* secondary surface */
  --s3: #DDE4F5;      /* tertiary */
  --b1: #C8D2EC;      /* border */
  --b2: #B0BDE0;      /* border hover */
  --t1: #111628;      /* deep navy ink */
  --t2: #4A5680;      /* secondary */
  --t3: #8895BC;      /* tertiary */

  /* Accent dark variants flip to light in light mode */
  --amber-d:  #FDEAEC;
  --blue-d:   #E8EEFF;
  --green-d:  #EDFAF1;
  --red-d:    #FDEAEA;
  --purple-d: #F0EEFF;
}
```

### Toggle implementation

**HTML — toggle button in header:**
```html
<button class="theme-btn" onclick="toggleTheme()" id="theme-btn" title="Toggle light/dark">
  🌙
</button>
```

**JS — toggle function:**
```javascript
let isDark = true;

function toggleTheme() {
  isDark = !isDark;
  document.documentElement.classList.toggle('light', !isDark);
  document.getElementById('theme-btn').textContent = isDark ? '🌙' : '☀️';
}
```

**CSS — smooth transition on mode switch:**
```css
*, *::before, *::after {
  transition: background-color .2s ease, border-color .2s ease, color .15s ease;
}
/* Exception — don't transition transforms or layout */
```

### Accepting a custom colorway from the user

When the user provides a custom palette, they will feed it in one of these formats:

**Format A — hex values directly:**
> "Use these colors: bg #1A1A2E, surface #16213E, accent #E94560"

Map them to the variable names in `:root` and update accordingly. Always derive both dark and light variants — if only dark is provided, create a light version by inverting surface lightness and keeping accents.

**Format B — named palette:**
> "I want a forest dark / emerald theme"

Interpret intent and propose a palette before writing code. Show the user the colors and get confirmation.

**Format C — updating existing colorway:**
> "Make the amber warmer / make the background lighter"

Use `sed` for global replacement — never manually hunt hex values:

```bash
# Replace one color across entire file
sed -i "s/#E8354A/#F0950A/g" terra-os.html

# Verify
grep -c "#E8354A" terra-os.html  # should return 0
```

### Rules — always enforced
- Never hardcode hex colors outside `:root` and `html.light` — always `var(--name)`
- Pure black (`#000`, `#060606`) is forbidden — minimum `#0A0D18`
- Pure white (`#FFF` as bg) is too harsh — use `#F4F6FC` minimum
- Accent colors stay consistent across both modes — only surface/text variables change
- When updating colors globally, use `sed` — see Update Patterns section

---

## Step 3 — Typography

Always import from Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
```

| Font | Use | Never use for |
|---|---|---|
| **Syne** | Headings, labels, stat values, logo | Body text |
| **IBM Plex Sans** | Body text, descriptions, buttons | Headings |
| **IBM Plex Mono** | Numbers, tickers, code, mono data | Flowing prose |

Base size: `15px`. Line height: `1.6`.

---

## Step 4 — Navigation architecture

Always use two navigation layers:

```html
<!-- Top-level: Home / Financial / Personal -->
<header class="header">
  <span class="logo">TERRA<span style="color:var(--amber)">OS</span></span>
  <nav class="tnav">
    <button class="tnav-btn act" onclick="showSec('home',this)">Home</button>
    <button class="tnav-btn" onclick="showSec('fin',this)">Financial</button>
  </nav>
</header>

<!-- Sub-nav within a section -->
<div class="sub-nav">
  <button class="snav-btn act" onclick="showSub('fin','capital',this)">Capital OS</button>
  <button class="snav-btn" onclick="showSub('fin','pipeline',this)">Pipeline</button>
</div>
```

Navigation JS:

```javascript
function showSec(id, btn) {
  document.querySelectorAll('.sec').forEach(s => s.classList.remove('act'));
  document.getElementById('s-' + id).classList.add('act');
  document.querySelectorAll('.tnav-btn').forEach(b => b.classList.remove('act'));
  btn.classList.add('act');
}

function showSub(sec, id, btn) {
  const prefix = sec === 'fin' ? 'ff-' : 'fp-';
  document.querySelectorAll('#s-' + sec + ' .fpanel').forEach(p => p.classList.remove('act'));
  document.getElementById(prefix + id).classList.add('act');
  document.querySelectorAll('#s-' + sec + ' .snav-btn').forEach(b => b.classList.remove('act'));
  btn.classList.add('act');
}
```

Panel structure — sections contain panels:

```html
<div class="sec act" id="s-fin">
  <div class="sub-nav">...</div>
  <div class="fpanel act" id="ff-capital"><!-- Capital OS content --></div>
  <div class="fpanel" id="ff-pipeline"><!-- Pipeline content --></div>
</div>
```

---

## Step 5 — Core component patterns

### Stat card

```html
<div class="stat">
  <p class="sl2">Label</p>
  <p class="sv">$465k</p>
  <p class="ss">at 3.87% yield</p>
</div>
```

### Data card with rules

```html
<div class="card" style="padding:10px 14px;">
  <div class="di"><span class="dok">✓</span><span>Allowed rule</span></div>
  <div class="di"><span class="dno">✕</span><span>Prohibited rule</span></div>
</div>
```

### Status tags

```html
<span class="tag t-green">Active</span>
<span class="tag t-amber">Watch</span>
<span class="tag t-gray">Locked</span>
<span class="tag t-blue">Future</span>
<span class="tag t-red">Speculation</span>
```

### Expandable card (accordion)

```html
<div class="rbcard">
  <div class="rbh" onclick="this.nextElementSibling.classList.toggle('open')">
    <p class="rbt">Section title</p>
    <span class="tag t-amber">Label</span>
  </div>
  <div class="rbb">
    <!-- Content shown when open class added -->
  </div>
</div>
```

### Data table

```html
<div class="card" style="padding:0;overflow:hidden;">
  <table class="data-table">
    <thead><tr><th>Column</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Row label</td><td>Value</td></tr>
    </tbody>
  </table>
</div>
```

---

## Step 6 — Data-driven rendering pattern

**Always define data as JS arrays, render via functions. Never hardcode cards as static HTML.**

```javascript
// Define data
const brokerages = [
  {
    id: 'fidelity',
    name: 'Fidelity',
    role: 'Core 25 — automated',
    accent: '#FFB830',
    tags: [['Automated', 't-amber'], ['25 stocks', 't-amber']],
    rules: [
      { ok: true,  t: 'Core 25 stocks — automated recurring from $1' },
      { ok: false, t: 'No speculation stocks' }
    ]
  }
  // ...
];

// Render function
function renderBrokerages() {
  document.getElementById('b-grid').innerHTML = brokerages.map(b => `
    <div class="bcard" onclick="selBrok('${b.id}')">
      <div class="bacc" style="background:${b.accent}"></div>
      <p class="bn">${b.name}</p>
      <p class="br2">${b.role}</p>
      <div>${b.tags.map(t => `<span class="tag ${t[1]}">${t[0]}</span>`).join('')}</div>
    </div>
  `).join('');
}

// Call on load
renderBrokerages();
```

**To update data:** change the array, not the HTML. `renderBrokerages()` handles the rest.

---

## Step 7 — Interactive calculators

### Range slider with live output

```html
<input type="range" id="i-pmt" min="100" max="2000" value="750" step="50"
       oninput="updateCalc()"/>
<span id="i-pmto">$750</span>

<script>
function updateCalc() {
  const val = parseInt(document.getElementById('i-pmt').value);
  document.getElementById('i-pmto').textContent = '$' + val;
  // ... recalculate and update other outputs
}
</script>
```

### Live CRR calculator

```javascript
function calcCRR() {
  const received = parseFloat(document.getElementById('crr-r-in').value) || 0;
  const deployed = parseFloat(document.getElementById('crr-d-in').value) || 0;
  if (received > 0) {
    const rate = Math.round((deployed / received) * 100);
    const el = document.getElementById('crr-rate');
    el.textContent = rate + '%';
    el.style.color = rate >= 75 ? 'var(--green)' : rate >= 50 ? 'var(--amber)' : 'var(--red)';
  }
}
```

### Checkbox progress tracker

```javascript
function togAction(row) {
  row.classList.toggle('done');
  const total = document.querySelectorAll('.arow').length;
  const done  = document.querySelectorAll('.arow.done').length;
  document.getElementById('progress-bar').style.width = Math.round(done/total*100) + '%';
  document.getElementById('progress-text').textContent = done + ' / ' + total + ' complete';
}
```

---

## Step 8 — AI-powered routing (optional)

When the user wants Claude to route inputs to the correct tool or account:

**API key modal:**

```html
<button onclick="document.getElementById('api-modal').classList.add('open')">⚙ API Key</button>

<div class="modal-overlay" id="api-modal">
  <div class="modal">
    <h3>Anthropic API Key</h3>
    <p>Required for AI routing. Used locally only — never stored.</p>
    <input type="password" id="api-key-input" placeholder="sk-ant-api03-..."/>
    <div class="modal-btns">
      <button onclick="document.getElementById('api-modal').classList.remove('open')">Cancel</button>
      <button onclick="saveKey()">Save</button>
    </div>
  </div>
</div>

<script>
let API_KEY = '';
function saveKey() {
  API_KEY = document.getElementById('api-key-input').value.trim();
  document.getElementById('api-modal').classList.remove('open');
}
</script>
```

**AI routing call pattern:**

```javascript
const SYSTEM_PROMPT = `You are a routing engine for [context].
Rules: [define routing rules clearly].
Respond ONLY with JSON: {"destination":"X","confidence":"high","reason":"2 sentences","warning":null}`;

async function route() {
  if (!API_KEY) { document.getElementById('api-modal').classList.add('open'); return; }
  const input = document.getElementById('input-field').value.trim();
  if (!input) return;

  document.getElementById('result-box').style.display = 'none';
  document.getElementById('loading').style.display = 'block';
  document.getElementById('route-btn').disabled = true;

  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 400,
        system: SYSTEM_PROMPT,
        messages: [{ role: 'user', content: input }]
      })
    });
    const data = await res.json();
    if (data.error) throw new Error(data.error.message);
    const j = JSON.parse(
      data.content?.find(b => b.type === 'text')?.text?.replace(/```json|```/g, '') || '{}'
    );
    document.getElementById('result-destination').textContent = j.destination || '';
    document.getElementById('result-reason').textContent = j.reason || '';
    document.getElementById('result-box').style.display = 'block';
  } catch (e) {
    document.getElementById('err').style.display = 'block';
    document.getElementById('err').textContent = 'Error: ' + (e.message || 'Routing failed.');
  } finally {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('route-btn').disabled = false;
  }
}
```

---

## Step 9 — Upgrade pipeline pattern

For tiered product/feature pipelines with unlock triggers:

```javascript
const pipeline = [
  {
    tier: 1,
    label: 'Tier 1 — Quick wins',
    items: [
      {
        id: 'product-id',
        name: 'Product Name',
        status: 'active',   // active | watch | locked
        cost: '$5/month',
        trigger: 'Already active',
        ttype: 'active',    // active | spending | balance | mixed | revenue
        highlight: 'Key benefit · Secondary benefit',
        benefits: ['Full benefit 1', 'Full benefit 2']
      }
    ]
  }
];

const statusCfg = {
  active: { label: 'Active', cls: 't-green' },
  watch:  { label: 'Watch',  cls: 't-amber' },
  locked: { label: 'Locked', cls: 't-gray'  }
};

function renderPipeline() {
  document.getElementById('pipeline-container').innerHTML = pipeline.map(tier => `
    <div style="margin-bottom:28px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
        <span style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
                     letter-spacing:.1em;text-transform:uppercase;color:var(--t3);">
          ${tier.label}
        </span>
        <div style="flex:1;height:1px;background:var(--b1);"></div>
      </div>
      ${tier.items.map(item => `
        <div class="rbcard" style="margin-bottom:8px;">
          <div class="rbh" onclick="this.nextElementSibling.classList.toggle('open')">
            <div>
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                <p style="font-family:'Syne',sans-serif;font-size:13px;font-weight:600;
                          color:var(--t1);margin:0;">${item.name}</p>
                <span class="tag ${statusCfg[item.status].cls}">
                  ${statusCfg[item.status].label}
                </span>
              </div>
              <p style="font-size:11px;color:var(--t2);margin:0;">${item.highlight}</p>
            </div>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;
                         color:var(--t3);flex-shrink:0;">${item.cost}</span>
          </div>
          <div class="rbb">
            <p style="font-size:12px;color:var(--t1);margin:0 0 10px;">
              <strong>Trigger:</strong> ${item.trigger}
            </p>
            ${item.benefits.map(b =>
              `<div class="di"><span class="dok">✓</span><span>${b}</span></div>`
            ).join('')}
          </div>
        </div>
      `).join('')}
    </div>
  `).join('');
}

renderPipeline();
```

---

## Step 10 — Chart.js integration (income/projection charts)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<div style="height:200px;position:relative;"><canvas id="myChart"></canvas></div>

<script>
let chart = null;

function buildChart(labels, data, goalLine) {
  const colors = data.map(v => v >= goalLine ? 'var(--green)' : 'var(--blue)');
  if (chart) {
    chart.data.datasets[0].data = data;
    chart.data.datasets[0].backgroundColor = colors;
    chart.update();
    return;
  }
  const ctx = document.getElementById('myChart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { data, backgroundColor: colors, borderRadius: 4, borderSkipped: false },
        { type: 'line', data: labels.map(() => goalLine),
          borderColor: 'var(--red)', borderWidth: 1.5,
          borderDash: [4, 4], pointRadius: 0, fill: false }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: 'rgba(255,255,255,0.07)' },
             ticks: { color: 'var(--t3)' }, border: { display: false } },
        x: { grid: { display: false },
             ticks: { color: 'var(--t3)' }, border: { display: false } }
      }
    }
  });
}
</script>
```

---

## Update patterns (surgical edits to existing files)

### Adding a new tab to an existing section

1. Add button to sub-nav:
```python
str_replace(
  old='<button class="snav-btn" onclick="showSub(\'fin\',\'rebal\',this)">Rebalancing</button>',
  new='<button class="snav-btn" onclick="showSub(\'fin\',\'rebal\',this)">Rebalancing</button>\n    <button class="snav-btn" onclick="showSub(\'fin\',\'new-tab\',this)">New Tab</button>'
)
```

2. Add panel HTML before the closing `</div>` of the section.

3. Add rendering JS before the closing `</script>` tag.

### Updating color palette globally

Use `sed` for global hex replacement — never manually find/replace:

```bash
# Replace specific old colors with new ones
sed -i "s/#060606/#0D1117/g" terra-os.html
sed -i "s/#5DBB6A/#4ADE80/g" terra-os.html
sed -i "s/#4A9EFF/#60A5FA/g" terra-os.html

# Verify no old colors remain
grep -c "#060606\|#5DBB6A\|#4A9EFF" terra-os.html
# Should return 0
```

### Updating data in an existing rendered section

Change the JS array only — never touch the HTML:

```python
str_replace(
  old="name:'Fidelity',role:'Core 12 — automated'",
  new="name:'Fidelity',role:'Core 25 — automated'"
)
```

### Verifying no duplicate JS declarations after edits

```bash
grep -n "^const pipeline\|^function renderPipeline\|^const statusCfg" file.html
# Each should appear exactly once
```

---

## Required CSS classes reference

Include these in `<style>` — they are referenced throughout the patterns above:

```css
/* Layout */
.sec{display:none;} .sec.act{display:block;}
.fpanel{display:none;} .fpanel.act{display:block;}

/* Cards */
.card{background:var(--s1);border:1px solid var(--b1);border-radius:var(--r);padding:14px 16px;}
.card2{background:var(--s2);border-radius:var(--r);padding:14px 16px;}
.stat{background:var(--s2);border:1px solid var(--b1);border-radius:var(--r);padding:14px;}
.stat .sv{font-family:'Syne',sans-serif;font-size:28px;font-weight:700;color:var(--t1);margin:4px 0 2px;}
.stat .sl2{font-size:10px;color:var(--t3);letter-spacing:.08em;text-transform:uppercase;font-weight:600;}

/* Rules */
.di{font-size:12px;color:var(--t2);display:flex;gap:7px;align-items:flex-start;padding:3px 0;}
.dok{color:var(--green);flex-shrink:0;}
.dno{color:var(--red);flex-shrink:0;}

/* Tags */
.tag{font-size:10px;padding:2px 8px;border-radius:20px;display:inline-block;font-family:'IBM Plex Sans',sans-serif;}
.t-amber{background:var(--amber-d);color:var(--amber);}
.t-blue{background:var(--blue-d);color:var(--blue);}
.t-green{background:var(--green-d);color:var(--green);}
.t-red{background:var(--red-d);color:var(--red);}
.t-purple{background:var(--purple-d);color:var(--purple);}
.t-gray{background:var(--s3);color:var(--t3);}

/* Expandable */
.rbcard{background:var(--s1);border:1px solid var(--b1);border-radius:var(--r);overflow:hidden;margin-bottom:8px;}
.rbh{display:flex;justify-content:space-between;align-items:center;padding:11px 14px;cursor:pointer;}
.rbh:hover{background:var(--s2);}
.rbt{font-family:'Syne',sans-serif;font-size:12px;font-weight:600;color:var(--t1);margin:0;}
.rbb{border-top:1px solid var(--b1);padding:10px 14px;display:none;}
.rbb.open{display:block;}

/* Sub-nav */
.sub-nav{display:flex;gap:0;border-bottom:1px solid var(--b1);margin-bottom:22px;}
.snav-btn{font-size:12px;padding:8px 16px;border:none;background:transparent;color:var(--t3);
          cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;transition:color .15s;}
.snav-btn:hover{color:var(--t2);}
.snav-btn.act{color:var(--t1);border-bottom-color:var(--amber);font-weight:500;}

/* Labels */
.sl{font-family:'Syne',sans-serif;font-size:10px;font-weight:600;letter-spacing:.1em;
    text-transform:uppercase;color:var(--t3);margin:0 0 10px;display:block;}

/* Data table */
.data-table{width:100%;border-collapse:collapse;font-size:12px;}
.data-table th{font-family:'Syne',sans-serif;font-size:9px;font-weight:600;letter-spacing:.1em;
               text-transform:uppercase;color:var(--t3);padding:8px 14px;
               text-align:left;border-bottom:1px solid var(--b1);}
.data-table td{padding:8px 14px;border-bottom:1px solid var(--b1);color:var(--t1);}
.data-table tr:last-child td{border-bottom:none;}

/* Allocation bars */
.alloc-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.alloc-bar-wrap{flex:1;height:4px;background:var(--b1);border-radius:2px;overflow:hidden;}
.alloc-bar{height:100%;border-radius:2px;}

/* Progress */
.pbr{height:2px;background:var(--b1);border-radius:2px;margin:6px 0 10px;overflow:hidden;}
.pf{height:100%;background:var(--green);border-radius:2px;transition:width .3s;}

/* Checklist row */
.arow{display:flex;gap:9px;align-items:flex-start;padding:7px 0;border-bottom:1px solid var(--b1);cursor:pointer;}
.arow:last-child{border-bottom:none;}
.arow.done .atx{text-decoration:line-through;color:var(--t3);}
.achk{width:16px;height:16px;border-radius:50%;border:1px solid var(--b2);display:flex;
      align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;font-size:9px;color:transparent;}
.arow.done .achk{background:var(--green-d);border-color:var(--green);color:var(--green);}
.atx{font-size:12px;color:var(--t1);line-height:1.4;}

/* Buttons */
.route-btn{padding:8px 20px;border:1px solid var(--b2);border-radius:var(--r-sm);
           background:var(--t1);color:var(--bg);font-size:12px;font-weight:500;
           cursor:pointer;font-family:'IBM Plex Sans',sans-serif;transition:opacity .15s;}
.route-btn:hover{opacity:.88;}
.route-btn:disabled{opacity:.3;cursor:not-allowed;}

/* Utility */
.result-box{background:var(--s2);border:1px solid var(--b1);border-radius:var(--r);
            padding:14px 16px;margin-top:10px;display:none;}
.loading-txt{font-size:12px;color:var(--t2);padding:10px 0;display:none;}
.err-txt{font-size:11px;color:var(--red);padding:6px 0;display:none;}
```

---

## Output checklist

Before delivering any dashboard file, verify:

- [ ] All colors use `var(--name)` — no hardcoded hex outside `:root`
- [ ] All content-heavy sections use data arrays + render functions
- [ ] Top-level nav + sub-nav both work (`.sec` / `.fpanel` toggle correctly)
- [ ] No duplicate JS function or const declarations
- [ ] Chart.js loaded from cdnjs if charts are present
- [ ] Google Fonts loaded in `<head>`
- [ ] API key modal present if AI routing is included
- [ ] File is a single `.html` — no external dependencies
- [ ] Present the file with `present_files` after creation

---

## File delivery

Always save to `/mnt/user-data/outputs/` and call `present_files`:

```python
present_files(["/mnt/user-data/outputs/terra-os.html"])
```
