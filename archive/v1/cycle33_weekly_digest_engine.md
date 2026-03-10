# Weekly Digest Engine v1.0
**Cycle 33** | Erasto | 2026-03-06

---

## Executive Summary
> Score: **2.31/5.0 — DEFENSIVE** (down from 2.62 CAUTIOUS)
> Regime: **ACCUMULATION** (60% confidence)
> Allocation: **20% BTC | 0% Alts | 80% Stables**
> Portfolio: **$9,967 (-0.3%)** vs HODL **(-2.5%)**
> Alpha: **+2.2%** | Max DD: **0.4%** | Wins: **7**

---

## What's New: Weekly Digest Format

Combines ALL v3 systems into one product:
1. **Scoring Engine** (L1-L4 composite)
2. **Regime Classifier** (4-state market ID)
3. **Performance Tracker** (live $10K vs benchmarks)
4. **Sector Heatmap** (12 tokens, 6 sectors)
5. **Phase Transition Alerts** (allocation triggers)

**One message. All systems. 3-minute read. Clear action.**

---

## Phase Transition: CAUTIOUS -> DEFENSIVE

| Level | Previous | Current | Driver |
|-------|----------|---------|--------|
| L1 Liquidity | 4.0 | 4.0 | Stable ($312B stablecoins) |
| L2 Macro | 2.0 | 2.0 | Stable (F&G 18 Extreme Fear) |
| L3 Cycle | 2.0 | 1.75 | DOWN: 30d momentum -6% |
| L4 Sectors | 2.75 | 1.5 | DOWN: only 1/12 positive |
| **Composite** | **2.62** | **2.31** | **-0.31 DOWNGRADE** |

### Rebalance Action
| | CAUTIOUS | DEFENSIVE | Action |
|---|---|---|---|
| BTC | 35% | 20% | **Reduce** -15% |
| Alts | 10% | 0% | **Exit all** |
| Stables | 55% | 80% | **Increase** +25% |

**Key drivers:**
- L4 collapsed to 1.5 (worst recorded). Only HYPE positive on 30d. Sector breadth 8%.
- L3 weakened: BTC -6% 30d, still -46% from $126K ATH.
- L1 holds strong: $312B stablecoin powder keg intact but not deploying.

---

## Regime: ACCUMULATION (60%)

| Signal | Value | Vote |
|--------|-------|------|
| ATH Distance | -46% | ACCUMULATION |
| 30d Momentum | -6% | MARKDOWN |
| Fear & Greed | 18 | ACCUMULATION |
| Stablecoin Flow | +14.7% | ACCUMULATION |
| TVL Trend | -7.4% | MARKDOWN |

3/5 = ACCUMULATION. Deep discount + fear + stablecoin build = textbook.
But TVL declining + momentum negative = the turn hasn't happened yet.

---

## Performance ($10K live tracking)

| Metric | Value | vs C32 |
|--------|-------|--------|
| Portfolio | $9,967 (-0.3%) | Was $9,960 |
| BTC HODL | $9,749 (-2.5%) | Was $9,733 |
| DCA | $9,983 (-0.2%) | Was $9,964 |
| Alpha vs BTC | +2.2% | Was +2.27% |
| Max Drawdown | 0.4% | Same |
| Win Streak | 7 | +1 |

Heavy stablecoin allocation absorbs downturn. -0.3% vs BTC -2.5%.

---

## Sector Heatmap

| Token | Price | 7d | 30d | ATH |
|-------|-------|-----|------|-----|
| HYPE | $31.01 | +1.0% | +5.0% | -35% |
| RNDR | $1.36 | -2.9% | -20.0% | -86% |
| DOGE | $0.11 | -3.0% | -15.0% | -85% |
| ARB | $0.10 | -3.7% | -22.0% | -96% |
| TIA | $0.33 | -3.8% | -25.0% | -97% |
| UNI | $3.83 | -3.9% | -12.0% | -91% |
| ONDO | $0.26 | -3.9% | -15.0% | -85% |
| SOL | $84.61 | -5.1% | -12.0% | -68% |
| LINK | $8.76 | -5.1% | -10.0% | -83% |
| AAVE | $111.58 | -5.8% | -8.0% | -80% |
| SUI | $0.90 | -6.0% | -18.0% | -82% |
| FET | $0.15 | -5.2% | -18.0% | -94% |

**Only HYPE green. Breadth 8%. Everything is on sale.**

---

## Deliverables

| Item | Details |
|------|---------|
| `scripts/weekly_digest.py` | Reusable engine (49 lines) |
| `scripts/run_cycle33.py` | Execution script (24 lines) |
| `data/score_history.csv` | +1 row (C33 DEFENSIVE) |
| `data/performance_history.csv` | +1 row (pv=$9,967) |
| `data/current_market.json` | Updated all metrics |
| Telegram EN + ES | Delivered (200 OK) |

---

## Key Insight

> **First phase downgrade in live tracking.** The model correctly
> shifts defensive when conditions deteriorate. L4 sector collapse
> (2.75 -> 1.5) was the trigger — only 1 of 12 tracked tokens
> positive on 30d.
>
> $312B in stablecoins on sideline. F&G at 18 (extreme fear).
> BTC -46% from ATH. This is textbook accumulation territory.
> But the model says: don't rush. Wait for the turn signal.
>
> **Powder keg loaded. Fuse not lit. Patience = alpha.**

---

## Next
- Regime transition alerts (ACCUMULATION->MARKUP auto-detect)
- Multi-asset alt tracking with entry signals
- Weekly digest auto-scheduling

*Erasto v3 | Not financial advice | 2026-03-06*
*Sources: CoinGecko, Alternative.me, DeFiLlama*
