## Erasto AI v2 Upgrade — Instructions for Elien

### What's Happening

Erasto is being upgraded from a bot that sends score updates to a full market intelligence agent that delivers: framework scores, alpha opportunities, a model portfolio, and a monthly watchlist. The goal is to make Erasto useful enough that 100,000 Spanish-speaking retail investors rely on him to make investment decisions.

### What v2 Delivers (That v1 Didn't)

1. **Alpha Hunting** — Every cycle, Erasto scans for volume spikes, DeFi yield opportunities, narrative momentum, and upcoming catalysts. Max 3 picks per cycle, each with data backing and risk score.

2. **Portafolio Erasto** — A public model portfolio starting at $10,000 hypothetical capital. Positions change only when the framework zone shifts or a catalyst triggers. Tracked in outputs/portfolio.json.

3. **Monthly Watchlist** — 5-10 tokens Erasto is monitoring but hasn't added to the portfolio yet. Each has a specific entry trigger condition. Published on the 1st of every month.

4. **Agent Architecture** — Plan → Execute → Validate → Answer. Erasto now checks his own output before shipping. Every score must match defined thresholds. Every number must have a source and date.

5. **Real API Data** — CoinGecko, DeFiLlama, Alternative.me instead of 8-12 web searches. Max 4 external calls per cycle.

6. **Bilingual Telegram** — Spanish first, English second. Structured format with score + allocation + alpha + portfolio + catalysts every single cycle.

### Telegram Output Example (What It Looks Like Now)

```
🟡 Erasto Score: 3.1/5 (→) | CAUTIOUS
💼 25% stables | 30% BTC | 20% ETH | 25% alts

🔥 ALPHA
• $VIRTUAL +47% 7d — AI agents narrative, TVL 2x [riesgo 4/5]
• Morpho USDC 8.2% APY — mejor yield risk-adjusted en DeFi
• $ARB unlock Mar 16: 1.1B tokens — presión de venta probable

💼 PORTAFOLIO ERASTO
BTC 30% | ETH 20% | USDC 25% | VIRTUAL 8% | AAVE 7% | ARB 5% | ONDO 5%
Sin cambios esta semana.

📌 MVRV 1.1 — a un dip de la mejor señal de compra en 2 años
👀 Fed Mar 19 | ETH Pectra Mar 26 | ARB unlock Mar 16

---

[English translation]
```

---

## GitHub Push Instructions

### Repository
`https://github.com/garcialalo98-del/erastoai`

### Source Files Location
Eduardo's storage: **Erasto Yields AI → Erasto v2 GitHub Files**

That folder contains 6 files:
- `SOUL.md` → goes to repo root
- `BACKLOG.md` → goes to repo root
- `dashboard_data.json` → goes to outputs/
- `portfolio.json` → goes to outputs/
- `watchlist_march2026.md` → goes to outputs/
- `PROMPTS.md` → DO NOT PUSH (Eduardo's reference only)

### Steps

**Step 1 — Clone**
```bash
git clone https://github.com/garcialalo98-del/erastoai.git
cd erastoai
```

**Step 2 — Archive v1 (move, don't delete)**
```bash
mkdir -p archive/v1
mv SOUL.md archive/v1/SOUL_v1.md 2>/dev/null
mv BACKLOG.md archive/v1/BACKLOG_v1.md 2>/dev/null
mv outputs/* archive/v1/ 2>/dev/null
```

**Step 3 — Place new v2 files**
```bash
mkdir -p outputs
mkdir -p cycles
touch cycles/log.md

# From "Erasto v2 GitHub Files" folder, place:
# SOUL.md → erastoai/SOUL.md (repo root)
# BACKLOG.md → erastoai/BACKLOG.md (repo root)
# dashboard_data.json → erastoai/outputs/dashboard_data.json
# portfolio.json → erastoai/outputs/portfolio.json
# watchlist_march2026.md → erastoai/outputs/watchlist_march2026.md
```

**Step 4 — Verify structure**
```
erastoai/
├── SOUL.md                          ← NEW v2
├── BACKLOG.md                       ← NEW v2
├── README.md                        ← keep existing
├── cycles/
│   └── log.md                       ← keep v1 history
├── outputs/
│   ├── dashboard_data.json          ← NEW v2 empty schema
│   ├── portfolio.json               ← NEW v2 empty portfolio
│   └── watchlist_march2026.md       ← NEW v2 empty watchlist
└── archive/
    └── v1/
        ├── SOUL_v1.md
        ├── BACKLOG_v1.md
        └── [old output files]
```

**Step 5 — Commit and push**
```bash
git add -A
git commit -m "v2: Agent architecture + Model Portfolio + Alpha Hunting + Watchlist"
git push
```

**Step 6 — Verify**
- SOUL.md has "Portafolio Erasto" and "Alpha Hunting" sections
- BACKLOG.md first task is "Initialize Portafolio Erasto"
- outputs/portfolio.json exists with empty positions array
- outputs/watchlist_march2026.md exists
- archive/v1/ has old files

### DO NOT PUSH
- `PROMPTS.md` — this is Eduardo's reference for MoltStreet settings, stays local

### After Push
Eduardo will update MoltStreet Identity & Recurring Task prompts manually. Once both the repo and MoltStreet are updated, Cycle 12 will run with the full v2 agent architecture.
