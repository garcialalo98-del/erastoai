# Cycle 31: Market Regime Classifier v1.0
**Date:** 2026-03-06 | **Agent:** Erasto v3.1

---

## Executive Summary

**REGIME: ACCUMULATION** (67% confidence, 4/6 signals)
**SCORE: 3.08/5.0 -> CAUTIOUS** (upgraded from 2.44 DEFENSIVE)
**KEY:** $312B stablecoin powder keg + Extreme Fear + BTC -44% ATH = textbook accumulation zone.

---

## New Engine: Market Regime Classifier

Classifies crypto into 4 phases using 6 signals:

| Regime | When | Strategy |
|--------|------|----------|
| ACCUMULATION | After drawdowns, extreme fear | DCA, patience |
| MARKUP | Breakout, positive momentum | Increase exposure |
| DISTRIBUTION | Near tops, greed | Take profits |
| MARKDOWN | Bear market, panic | Capital preservation |

---

## Live Market Data (2026-03-06)

| Metric | Value | Context |
|--------|-------|---------|
| BTC | $68,006 | -4.9% 24h, -44% from $122K ATH |
| ETH | $1,975 | -5.7% 24h |
| SOL | $85 | -5.6% 24h |
| Fear and Greed | 18 | Extreme Fear (sustained weeks) |
| Stablecoins | $311.7B | +$42B vs baseline (+15.4%) |
| TVL | $95.8B | Stable |
| 30d Momentum | -6.4% | War-week rally faded |
| BTC ETFs | $228M outflow Mar 5 | Mixed: $1B+ in recently, now reversing |

Sources: CoinGecko, Alternative.me, DeFiLlama, CoinDesk

---

## Signal Breakdown (6 signals -> 67% ACCUMULATION)

| Signal | Reading | Label | Lean |
|--------|---------|-------|------|
| ATH Distance | -44% | DEEP DISCOUNT | ACCUMULATION |
| 30d Momentum | -6.4% | DOWN | MARKDOWN |
| Fear and Greed | 18 | EXTREME FEAR | ACCUMULATION |
| Stablecoin Flow | +15.4% | STRONG INFLOW | ACCUMULATION |
| TVL Trend | -2.0% 7d | STABLE | ACCUMULATION |
| ETF/Institutional | $228M outflow | SELLING | DISTRIBUTION |

4 signals ACCUMULATION, 1 MARKDOWN (momentum drag), 1 DISTRIBUTION (ETF caution).
Translation: Accumulation zone but floor not confirmed. Patient capital wins.

---

## Scoring (L1-L4)

| Level | Score | Status |
|-------|-------|--------|
| L1 Liquidity | 4.78 | Near max. $312B powder keg. |
| L2 Macro | 2.00 | Extreme Fear, geopolitical risk |
| L3 Cycle | 2.39 | -44% ATH, negative momentum |
| L4 Flows | 2.75 | High stables + stable TVL |
| **Composite** | **3.08** | **CAUTIOUS (up from 2.44 DEFENSIVE)** |

Score jumped +0.64 pts. L1 Liquidity carrying the model.

---

## Allocation (ACCUMULATION Regime)

| Asset | Alloc | Rationale |
|-------|-------|-----------|
| BTC | 30-40% | Core. DCA weekly. Deep discount. |
| Alts | 5-10% | Small conviction only |
| Stables | 50-65% | Dry powder for dips/MARKUP |

Rules: DCA, keep 50%+ stables, no leverage, no FOMO.
Watch: F&G > 25 + positive momentum = MARKUP trigger.

---

## Regime Change Triggers

| Trigger | Change | Probability |
|---------|--------|-------------|
| BTC momentum positive + F&G > 25 | -> MARKUP | Medium |
| BTC > $80K + ETF inflows | -> MARKUP | Medium-Low |
| BTC < $60K + stablecoin outflows | -> MARKDOWN | Low |
| Fed rate cut | Boosts MARKUP | TBD |

---

## Macro Context

- Fed: QT ended Nov 2025. Balance sheet +$93B. Net liquidity expanding.
- Rates: Watching for cut signals. Next FOMC imminent.
- Geopolitics: War-week rally faded. Risk appetite suppressed.
- ETFs: $1B+ inflows absorbed by basis trade arbitrage. $228M outflow Mar 5.

---

## Deliverables

| File | Description |
|------|-------------|
| scripts/market_regime.py | Regime classification engine (43 lines) |
| scripts/run_cycle31.py | Full pipeline (71 lines) |
| data/score_history.csv | +1 row |
| data/current_market.json | Updated with regime field |
| Telegram EN + ES | 200 OK both |

---

## 3-Minute Takeaway

1. ACCUMULATION phase. BTC -44% from highs. Extreme fear. Where wealth is built.
2. Allocation: 35% BTC, 5% alts, 60% stables. DCA weekly.
3. $312B powder keg. $42B more stablecoins than months ago. Deployment = price move.
4. Watch for MARKUP: F&G > 25 + positive momentum = increase exposure.

Be patient. Be positioned. Accumulate quietly.

*Research only, not financial advice.*
