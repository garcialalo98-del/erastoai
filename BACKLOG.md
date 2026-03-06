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

### CYCLE 18: Automated Data Collection Script
**Goal:** Eliminate manual searches, automate data feeds
**Deliverables:**
- Python script: fetch BTC, ETH, Fear & Greed, stablecoin supply
- Save to `/data/current_market.json`
- Run before each cycle (cron-ready)
- Error handling, rate limit management
**Output:** `cycle18_data_collector.py` + documentation

---

### CYCLE 19: Performance vs Benchmarks
**Goal:** Track how allocation model performs vs alternatives
**Deliverables:**
- Compare vs: BTC buy-and-hold, 60/40 BTC/stables, DCA
- Update weekly with live data
- Performance chart (text-based table)
**Output:** `cycle19_benchmark_comparison.md`

---

### CYCLE 20: Full Quant Dashboard Launch 🚀
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

## 🟢 PRIORITY 2 — Future Enhancements (Post-v2)

- [ ] **Mobile-optimized dashboard** (responsive text format)
- [ ] **Weekly email digest** (automated reports)
- [ ] **Discord bot integration** (post updates automatically)
- [ ] **Portfolio rebalancing alerts** (push notifications when allocation drifts)
- [ ] **Multi-timeframe analysis** (daily/weekly/monthly views)
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

**Last updated:** Elien — March 5, 2026 (v2 roadmap defined)
