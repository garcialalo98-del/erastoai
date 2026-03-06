# Cycle 24: Rebalancing Alerts + Historical Score Tracking

**Date:** 2026-03-06
**Task:** Portfolio rebalancing alerts + historical score time series
**Status:** ✅ DONE

---

## What Was Built

### 1. Rebalance Alert System (`scripts/rebalance_alerts.py`)
- **Phase boundary detection**: Monitors score vs 4 boundaries (1.5, 2.5, 3.5, 4.5)
- **Direction awareness**: Detects UPGRADE vs DOWNGRADE transitions
- **Distance tracking**: Shows how far from next phase boundary (early warning)
- **Last-score comparison**: Loads from history CSV or JSON fallback
- **Deduplication**: Won't double-count same-day entries

### 2. Historical Score Tracker (`data/score_history.csv`)
- **Time series format**: date, btc, eth, fng, stb_b, tvl_b, L1-L4, composite, phase, allocation
- **Auto-append**: Each run adds a row (or updates if same day)
- **Foundation for**: trend analysis, performance tracking, backtest validation
- **CSV format**: importable to any spreadsheet or analysis tool

### 3. Live Pipeline Runner (`scripts/run_cycle24.py`)
- **End-to-end**: Fetch → Score → Compare → Alert → Save → TG
- **7 API calls**: CoinGecko (4), Alternative.me (1), DeFiLlama (2)
- **Telegram delivery**: Auto-sends status or rebalance alert
- **JSON snapshot**: Updates `data/current_market.json` with rebalance context

---

## Live Results (2026-03-06)

| Metric | Value |
|--------|-------|
| BTC | $70,004 |
| ETH | $2,047.64 |
| Fear & Greed | 18 (Extreme Fear) |
| Stablecoins | $311.7B (+$39.9B from baseline) |
| TVL | $97.8B |
| BTC 30d | -7.7% |

### Scoring
| Level | Score | Rationale |
|-------|-------|-----------|
| L1 Liquidity | 4.0/5 | Stablecoin delta +14.7% (massive accumulation) |
| L2 Macro | 2.0/5 | F&G 18 = Extreme Fear |
| L3 Cycle | 1.75/5 | BTC at 55.5% of ATH, -7.7% 30d momentum |
| L4 Sectors | 2.0/5 | Only 2/10 tokens positive 30d (MKR +21%, UNI +1.5%) |
| **Composite** | **2.44/5** | **DEFENSIVE** |

### Rebalance Status
- **Phase change?** NO
- **Current allocation:** 20% BTC | 0% Alts | 80% Stables
- **Delta from last:** 0.00 (stable)
- **Distance to upgrade (CAUTIOUS):** 0.06 points to boundary 2.5
- **Telegram alert:** Sent (msg #27)

---

## Key Insight

**The market is 0.06 points from an upgrade.** What would flip it:
- F&G rising above 25 (L2: 2.0 → 2.5, comp → 2.56 = CAUTIOUS)
- BTC 30d turning positive (L3: 1.75 → 2.0, comp → 2.50 = CAUTIOUS)
- 3+ sector tokens turning green on 30d (L4: 2.0 → 2.5, comp → 2.56)

Any ONE of these triggers alone pushes us to CAUTIOUS (35% BTC, 10% Alts, 55% Stables).

**$312B stablecoin powder keg** remains the dominant narrative. Liquidity is maxed out (L1=4.0) but price hasn't absorbed it. When fear breaks, the rebalance alert will fire automatically.

---

## Files Delivered
1. `scripts/rebalance_alerts.py` — 64-line module (phase detection, history, boundary math)
2. `scripts/run_cycle24.py` — 88-line runner (fetch, score, alert, TG delivery)
3. `data/score_history.csv` — Time series initiated (row 1: 2026-03-06)
4. `data/current_market.json` — Updated with rebalance context
5. `outputs/cycle24_rebalance_alerts.md` — This document

## Architecture
```
run_cycle24.py  (or future cron job)
    ├── rebalance_alerts.py  (phase logic, history tracking)
    ├── data/score_history.csv  (growing time series)
    ├── data/current_market.json  (latest snapshot)
    └── Telegram  (auto-alert on phase change OR status check)
```

---

**Next tasks:**
- Multi-timeframe views (daily/weekly/monthly from score_history.csv)
- Score trend visualization (text-based charts from time series)
- Weekly cron automation (auto-run pipeline on schedule)
