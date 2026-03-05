# Erasto v2 Roadmap — Quant Dashboard Upgrade

**Vision:** Transform Erasto from a research engine into the #1 crypto financial dashboard for retail investors.

**Timeline:** Cycles 12-20 (approximately 9 cycles)  
**Start Date:** March 5, 2026  
**Target Launch:** Cycle 20 (late March / early April 2026)

---

## What v2 Delivers

By Cycle 20, retail investors get:

1. ✅ **One composite score** (1-5) — macro regime clarity
2. ✅ **Exact allocation %** — BTC/alts/stables, no guessing
3. ✅ **Backtest-validated model** — proven against 2020-2026 data
4. ✅ **Live performance tracking** — vs BTC buy-and-hold, 60/40, DCA
5. ✅ **Risk transparency** — max drawdown, Sharpe ratio visible
6. ✅ **Sector rotation heatmap** — where capital is flowing
7. ✅ **Zero external costs** — 100% free data sources, sustainable forever

**The promise:** Open dashboard. Read 3 minutes. Know exactly what to do.

---

## Cycle-by-Cycle Build Plan

### CYCLE 12: Portfolio Allocation Model v1
**Status:** 🔴 NOT STARTED  
**Goal:** Map composite score to concrete portfolio allocation percentages

**What gets built:**
- Allocation formula by score range:
  - **4.5-5.0:** 80% BTC, 15% alts, 5% stables (STRONG BULL)
  - **3.5-4.4:** 60% BTC, 20% alts, 20% stables (BULL)
  - **2.5-3.4:** 40% BTC, 10% alts, 50% stables (CAUTIOUS ACCUMULATION)
  - **1.5-2.4:** 20% BTC, 80% stables (DEFENSIVE)
  - **<1.5:** 100% stables (CRITICAL)
- Rebalancing trigger rules (when does allocation change?)
- Edge case handling (altcoin bifurcation, BTC-only scenarios)

**Output:** `outputs/cycle12_portfolio_allocation_model.md`  
**Validation:** Apply to current score (3.08) → should output 40% BTC, 10% alts, 50% stables

---

### CYCLE 13: Historical Data Collection
**Status:** 🔴 NOT STARTED  
**Goal:** Build the dataset needed for backtesting (2020-2026)

**What gets built:**
- Python script: fetch BTC/ETH monthly price data from CoinGecko free API
- Manual scoring: apply L1-L4 framework to each quarter (2020 Q1 → 2026 Q1)
- CSV format: `Date, BTC_Price, Score, L1, L2, L3, L4, Notes`
- Data validation: cross-check prices with multiple sources

**Output:**  
- `data/historical_data_2020_2026.csv`
- `scripts/data_collector.py`
- `outputs/cycle13_data_collection_report.md` (methodology + sources)

**Validation:** 24 quarters scored, no missing data, prices match historical records

---

### CYCLE 14: Backtest Portfolio Model
**Status:** 🔴 NOT STARTED  
**Goal:** Prove the allocation model works (or doesn't) against historical data

**What gets built:**
- Backtest engine: apply allocation model to historical scores
- Simulate $10,000 portfolio (Jan 2020 → March 2026)
- Calculate: Total return, CAGR, quarterly performance
- Compare vs buy-and-hold BTC (same starting capital)

**Output:**  
- `outputs/cycle14_backtest_results.md`
- Performance table (quarter-by-quarter)
- Return comparison: Erasto model vs BTC buy-and-hold
- Key findings: when model outperformed, when it lagged

**Validation:** Backtest complete, no calculation errors, results make narrative sense

---

### CYCLE 15: Risk Metrics Framework
**Status:** 🔴 NOT STARTED  
**Goal:** Add risk transparency to all future outputs

**What gets built:**
- **Max Drawdown:** Peak-to-trough decline from any historical high
- **Annualized Volatility:** Standard deviation of quarterly returns
- **Win Rate:** % of quarters with positive return
- **Sharpe Ratio:** (Annual Return - 0%) / Annualized Volatility
- Risk calculation script (Python)

**Output:**  
- `outputs/cycle15_risk_metrics_framework.md`
- `scripts/risk_calculator.py`
- Historical risk analysis (applied to backtest data)

**Validation:** All metrics calculated for 2020-2026, risk framework documented

---

### CYCLE 16: Weekly Dashboard v2
**Status:** 🔴 NOT STARTED  
**Goal:** Combine all v2 components into the final dashboard template

**What gets built:**
- One-page dashboard format:
  - **Header:** Composite Score + Regime Label
  - **Allocation:** BTC%, Alts%, Stables% (current recommendation)
  - **Performance:** YTD return, vs BTC buy-and-hold
  - **Risk:** Current drawdown, Sharpe ratio
  - **Alerts:** Active alerts (color-coded)
  - **Sector Rotation:** Top 3 sectors this week
  - **Watch Next:** 3 key signals/thresholds
- Optimized for MoltX posting (readable, scannable, mobile-friendly)

**Output:**  
- `outputs/cycle16_weekly_dashboard_template_v2.md`
- Template file (markdown format, fill-in-the-blank)

**Validation:** Dashboard <= 1 page, readable in 3 minutes, no jargon

---

### CYCLE 17: Sector Performance Tracker
**Status:** 🔴 NOT STARTED  
**Goal:** Track which crypto sectors are absorbing capital (rotation intelligence)

**What gets built:**
- 6 sectors tracked: DeFi, L1/L2, AI Agents, RWA, Gaming, Memecoins
- Weekly performance: 7-day % change (sector index vs BTC)
- Data source: CoinGecko free API (sector market cap aggregation)
- Heatmap visualization (text-based table)
- Rotation signal: which sector is outperforming this week?

**Output:**  
- `outputs/cycle17_sector_tracker.md`
- `scripts/sector_data.py`
- Sector performance table (updated weekly)

**Validation:** All 6 sectors tracked, data refreshes weekly, rotation signal clear

---

### CYCLE 18: Automated Data Collection Script
**Status:** 🔴 NOT STARTED  
**Goal:** Eliminate manual web searches — automate all data fetching

**What gets built:**
- Python script: fetch all required data before each cycle
  - BTC price (CoinGecko)
  - ETH price (CoinGecko)
  - Fear & Greed Index (Alternative.me)
  - Stablecoin supply (DeFiLlama or CoinGecko)
  - M2 money supply (FRED API)
  - Optional: DXY, VIX (if free sources available)
- Output format: JSON (`/data/current_market.json`)
- Error handling, rate limit management
- Cron-ready (can run on schedule)

**Output:**  
- `scripts/automated_data_collector.py`
- `data/current_market.json` (sample)
- `outputs/cycle18_automation_guide.md` (setup instructions)

**Validation:** Script runs successfully, all data fields populated, no API errors

---

### CYCLE 19: Performance vs Benchmarks
**Status:** 🔴 NOT STARTED  
**Goal:** Track how Erasto's allocation model performs vs alternative strategies

**What gets built:**
- Benchmark comparison (same starting capital, same timeframe):
  1. **BTC Buy-and-Hold** (100% BTC, never sell)
  2. **60/40 Portfolio** (60% BTC, 40% stables, rebalance monthly)
  3. **DCA Strategy** (dollar-cost average into BTC weekly)
- Performance table: Return, max drawdown, Sharpe for each strategy
- Update weekly with live data (going forward)

**Output:**  
- `outputs/cycle19_benchmark_comparison.md`
- Performance comparison table (historical + live)

**Validation:** All 3 benchmarks calculated, Erasto model comparison clear

---

### CYCLE 20: Full Quant Dashboard Launch 🚀
**Status:** 🔴 NOT STARTED  
**Goal:** Ship the complete v2 dashboard to MoltX and mark v2 COMPLETE

**What gets shipped:**
- **First complete quant dashboard:**
  - Composite Score: X.XX/5 | REGIME: [label]
  - Allocation: XX% BTC, XX% alts, XX% stables
  - Performance YTD: +X.X% (vs BTC: +Y.Y%)
  - Max Drawdown: -X.X% | Sharpe: X.XX
  - Active Alerts: [count + summary]
  - Sector Rotation: [heatmap]
  - Top 3 Projects to Watch: [L6 gems]
- Spanish version (full translation)
- Post on MoltX with launch announcement

**Output:**  
- `outputs/cycle20_full_quant_dashboard_v1.md`
- MoltX post (live)
- v2 COMPLETE flag in BACKLOG.md

**Validation:** Dashboard live on MoltX, all components functional, retail feedback positive

---

## Success Metrics (Cycle 20 Checklist)

Before marking v2 complete, verify:

- ✅ Portfolio allocation model operational (score → allocation %)
- ✅ Historical backtest complete (2020-2026 validated)
- ✅ Risk metrics live (drawdown, Sharpe, win rate)
- ✅ Performance tracking functional (vs BTC, 60/40, DCA)
- ✅ Sector rotation tracker operational (6 sectors, weekly updates)
- ✅ Data automation complete (zero manual searches required)
- ✅ Dashboard format finalized (3-minute read, zero jargon)
- ✅ Spanish version shipping (bilingual intelligence)
- ✅ Zero external API costs (100% free data sources)
- ✅ MoltX post live (public launch)

**If any checkbox fails, v2 is not complete. Fix before declaring victory.**

---

## What v2 Does NOT Include

(Saving for v3 or later)

- ❌ Real-time push notifications (requires infrastructure)
- ❌ Multi-asset correlation (stocks, bonds, commodities)
- ❌ Mobile app (iOS/Android native)
- ❌ API access for developers
- ❌ Paid data sources (Glassnode, Messari Pro, Nansen)
- ❌ Trading automation / execution layer
- ❌ User accounts / personalized portfolios

**v2 philosophy:** Nail the dashboard first. Scale later.

---

## Risk Factors

**Things that could delay v2:**

1. **Data quality issues** — Free APIs go down, rate limits hit  
   *Mitigation:* Cache data, use multiple sources

2. **Backtest reveals model doesn't work** — Allocation strategy underperforms BTC  
   *Mitigation:* Adjust weights, iterate on scoring formula

3. **Operator capacity constraints** — Eduardo too busy to trigger cycles  
   *Mitigation:* Batch multiple cycles, automate where possible

4. **MoltX platform limitations** — Dashboard format doesn't render well  
   *Mitigation:* Optimize for text-based output, test early

---

## Post-v2 Vision (v3 and Beyond)

Once v2 ships, Erasto becomes:

- **The dashboard retail investors check every Monday** (habit formation)
- **Proven backtest-validated intelligence** (not just opinions)
- **Bilingual crypto research leader** (LATAM underserved market)
- **Zero-cost sustainable model** (can run forever without funding)

**Then we scale:**
- Real-time alerts (push notifications when regime changes)
- Multi-asset support (correlate crypto with macro / equities)
- API access (let developers build on Erasto's intelligence)
- Mobile app (iOS/Android native dashboard)

**But first:** Ship v2. Prove it works. Build the foundation.

---

**Last updated:** Elien — March 5, 2026  
**Status:** v2 roadmap locked, Cycle 12 ready to start
