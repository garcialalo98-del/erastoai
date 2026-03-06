# BACKLOG.md — Erasto's Research Agenda (v2)

**Instructions:** Pick the top item from PRIORITY 1. Move to PRIORITY 2 only when Priority 1 is empty. Mark tasks ✅ when done.

---

## ✅ v1 COMPLETED (Cycles 1-11)

- [x] **Understand the framework** — Cycle 1
- [x] **Begin publishing** — Cycle 1
- [x] **Sector Protocol Map (L4->L5)** — Cycle 3
- [x] **Scoring System v1.0** — Cycle 4
- [x] **Build Delta Tracker** — Cycle 5
- [x] **Identify high-signal data sources** — Cycle 6
- [x] **Live Score Updates** — Cycle 7
- [x] **Alert System v1.0** — Cycle 8
- [x] **Level 6 Hidden Gems** — Cycle 9
- [x] **Spanish Research Brief** — Cycle 10
- [x] **Output Design Guide** — Cycle 11

**v1 Status:** 5 output types LIVE. Scoring system validated. Alert infrastructure deployed. Ready for quant upgrade.

---

## 🔴 PRIORITY 1 — v2 Quant Analyst Upgrade (Cycles 12-20)

### ✅ CYCLE 12: Portfolio Allocation Model v1 (DONE — Cycle 13 execution)
**Goal:** Map composite score → concrete allocation percentages
**Deliverables:**
- Allocation formula by score range (4.5-5.0, 3.5-4.4, 2.5-3.4, 1.5-2.4, <1.5)
- Rebalancing trigger rules (score delta threshold)
- Asset classes: BTC%, Alts%, Stablecoins%
**Output:** `cycle12_portfolio_allocation_model.md`

---

### ✅ CYCLE 13: Historical Data Collection (DONE — Cycle 14 execution)
**Goal:** Build dataset for backtesting (2020-2026)
**Deliverables:**
- BTC/ETH monthly price data (CoinGecko free API)
- Manual quarterly scoring using existing L1-L4 framework
- CSV format: Date, BTC Price, Score, L1, L2, L3, L4
- Data collection script (Python)
**Output:** `cycle13_historical_data_2020_2026.csv` + `data_collector.py`

---

### ✅ CYCLE 14: Backtest Portfolio Model (DONE — Cycle 15 execution)
**Goal:** Validate allocation model against historical data
**Deliverables:**
- Apply allocation rules to 2020-2026 scores
- Simulate $10K portfolio performance
- Compare vs buy-and-hold BTC
- Calculate total return, CAGR
**Output:** `cycle14_backtest_results.md` (performance table + analysis)

---

### ✅ CYCLE 15: Risk Metrics Framework (DONE — Cycle 16 execution)
**Goal:** Add risk transparency to all outputs
**Deliverables:**
- Max drawdown calculation
- Annualized volatility
- Win rate (% of profitable quarters)
- Simple Sharpe approximation (return/volatility)
**Output:** `cycle15_risk_metrics_framework.md`

---

### ✅ CYCLE 16: Weekly Dashboard v2 (DONE — Cycle 17 execution)
**Goal:** Combine all v2 components into one-page dashboard
**Deliverables:**
- Score + Allocation % + Alerts + Risk Metrics
- One-page format optimized for MoltX
- Clear, scannable, actionable
**Output:** `cycle16_weekly_dashboard_template_v2.md`

---

### ✅ CYCLE 17: Sector Performance Tracker (DONE — Cycle 18 execution)
**Goal:** Track sector rotation in real-time
**Deliverables:**
- 6 sectors: DeFi, L1/L2, AI Agents, RWA, Gaming, Memecoins
- 7-day % change vs BTC (CoinGecko free API)
- Heatmap visualization (text-based)
- Rotation signal (which sectors absorbing capital)
**Output:** `cycle17_sector_tracker.md`

---

### ✅ CYCLE 18: Automated Data Collection Script (DONE — Cycle 19 execution)
**Goal:** Eliminate manual searches, automate data feeds
**Deliverables:**
- Python script: fetch BTC, ETH, Fear & Greed, stablecoin supply
- Save to `/data/current_market.json`
- Run before each cycle (cron-ready)
- Error handling, rate limit management
**Output:** `cycle18_data_collector.py` + documentation

---

### ✅ CYCLE 19: Performance vs Benchmarks (DONE — Cycle 20 execution)
**Goal:** Track how allocation model performs vs alternatives
**Deliverables:**
- Compare vs: BTC buy-and-hold, 60/40 BTC/stables, DCA
- Update weekly with live data
- Performance chart (text-based table)
**Output:** `cycle19_benchmark_comparison.md`

---

### ✅ CYCLE 20: Full Quant Dashboard Launch 🚀 (DONE — Cycle 20 execution)
**Goal:** Ship complete v2 dashboard to MoltX
**Deliverables:**
- Composite score + allocation recommendation
- YTD performance vs benchmarks
- Risk metrics (drawdown, Sharpe)
- Sector heatmap
- Top 3 projects to watch
- Spanish version
**Output:** `cycle20_full_quant_dashboard_v1.md` (MoltX post)

---


## 🔵 v3 IN PROGRESS — Distribution & Automation (Cycles 21+)

### ✅ CYCLE 21: Telegram Dashboard Delivery + Live Update (DONE)
**Goal:** Ship mobile-optimized dashboard via Telegram bot
**Deliverables:**
- Mobile-first dashboard format (< 4096 chars, emoji-coded)
- Live market data refresh (all 6 levels scored)
- Telegram bot delivery (EN + ES)
- Reusable message template for future cycles
**Output:** `cycle21_telegram_dashboard_delivery.md`
**Finding:** Score 2.25 DEFENSIVE. BTC $70,311 (-44% ATH). Stables $271.8B ATH (+$6.3B). Extreme Fear 18. Liquidity bullish but price hasn't absorbed yet. $272B powder keg.

---


### ✅ CYCLE 23: Automated Data Pipeline v1.0 (DONE)
**Goal:** End-to-end automation: one command fetches data, scores L1-L4, generates allocation, formats dashboard, sends via Telegram
**Deliverables:**
- `scripts/erasto_pipeline.py` (124 lines, Python stdlib only)
- 7 free API calls: CoinGecko (4), Alternative.me (1), DeFiLlama (2)
- Auto-scoring engine: L1 (stablecoin delta), L2 (F&G), L3 (ATH+momentum), L4 (sector %)
- Telegram delivery EN + ES (<2K chars, mobile-optimized)
- JSON snapshot saved to `data/current_market.json`
**Output:** `cycle23_automated_pipeline.md`
**Finding:** Score 2.44 DEFENSIVE. Stablecoins $311.7B (+$40B vs C21) = largest liquidity build tracked. $312B powder keg.

---

### ✅ CYCLE 24: Rebalancing Alerts + Historical Score Tracking (DONE)
**Goal:** Auto-detect phase boundary crossings and track score time series
**Deliverables:**
- `scripts/rebalance_alerts.py` (64 lines, phase detection + boundary math + CSV history)
- `scripts/run_cycle24.py` (88 lines, end-to-end: fetch→score→compare→alert→TG)
- `data/score_history.csv` (time series tracking initiated)
- Telegram delivery of status/rebalance alerts
- Score 2.44 DEFENSIVE confirmed — 0.06pts to CAUTIOUS upgrade
**Output:** `cycle24_rebalance_alerts.md`
**Finding:** Score 2.44 DEFENSIVE. 0.06pts from upgrade. $312B stablecoin powder keg. Any single trigger flips to CAUTIOUS.

### ✅ CYCLE 26: Multi-Timeframe Analysis (DONE)
**Goal:** Build daily/weekly/monthly scoring views + divergence detection
**Deliverables:**
- `scripts/multi_timeframe.py` (74 lines, reusable scoring engine)
- `scripts/run_cycle26.py` (execution with live data)
- 3 timeframe scores: Daily 1.92, Weekly 2.69, Monthly 1.94
- Divergence detector (3 cross-timeframe signals)
- Score history CSV updated with daily+monthly columns
- Telegram delivery EN + ES
**Output:** `cycle26_multi_timeframe_analysis.md`
**Finding:** PHASE UPGRADE! Weekly 2.69 CAUTIOUS (from 2.44 DEFENSIVE). 30d BTC momentum +7.9% was trigger. New alloc: BTC 35%, Alts 10%, Stables 55%.

---


---

## 🟢 PRIORITY 2 — Future Enhancements (Post-v2)

- [x] **Mobile-optimized dashboard** (responsive text format) — ✅ Cycle 21
- [ ] **Weekly email digest** (automated reports)
- [x] **Telegram bot integration** (post updates automatically) — ✅ Cycle 21
- [x] **Portfolio rebalancing alerts** (push notifications when allocation drifts) — ✅ Cycle 24
- [x] **Multi-timeframe analysis** (daily/weekly/monthly views) — ✅ Cycle 26
- [ ] **Custom watchlists** (user-configurable project tracking)

---

## 🎯 v2 Success Metrics

**By Cycle 20, Erasto must:**
1. ✅ Publish actionable allocation % weekly (not vague "bullish/bearish")
2. ✅ Backtest-validated model (proven against 2020-2026 data)
3. ✅ Performance tracking live (vs BTC, 60/40, DCA)
4. ✅ Risk transparency (max drawdown, Sharpe visible)
5. ✅ Zero external API costs (100% free data sources)
6. ✅ 3-minute read time (retail-friendly dashboard format)

**Vision:** Retail investors worldwide check Erasto every Monday morning. Not because it's hype. Because it works.

---

**Last updated:** March 6, 2026 — v3 Pipeline LIVE. Auto fetch+score+send operational.
