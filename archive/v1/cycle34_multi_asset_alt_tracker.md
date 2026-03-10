# Cycle 34: Multi-Asset Alt Portfolio Tracker v1.0

**Date:** 2026-03-06 | **Score:** 2.31 DEFENSIVE | **Regime:** ACCUMULATION (80%)

## What Was Built

Previously "X% alts" tracked only ETH. Now: real 5-token basket selected by opportunity score.

### New Components
- `scripts/alt_basket_tracker.py` (65 lines) — Reusable engine: opp scoring, basket construction, P&L tracking
- `scripts/run_cycle34.py` (75 lines) — Full pipeline: fetch>score>select>track>TG
- `data/alt_basket.json` — Live basket with per-position data

## Alt Basket Selection (Top 5 of 14)

| Rank | Token | Score | ATH Disc | 7d | 30d |
|------|-------|-------|----------|-----|------|
| 1 | ARB | 75.4 | -95.8% | +0.1% | -22.0% |
| 2 | SUI | 70.1 | -83.1% | +0.6% | -16.2% |
| 3 | UNI | 65.1 | -91.4% | +3.5% | +2.3% |
| 4 | HYPE | 64.8 | -47.7% | +14.2% | -11.5% |
| 5 | DOGE | 64.1 | -87.5% | -2.1% | -11.2% |

**Selection logic:** Opp Score = ATH discount (40%) + 7d momentum (30%) + oversold bounce (20%) + market cap size (10%). ARB tops due to extreme -96% ATH discount with stabilizing momentum.

## Basket Status: PAPER MODE

DEFENSIVE phase = 0% alt allocation. Basket tracked in paper ($1K sim).
Deploys real capital at CAUTIOUS (score >= 2.50): 10% to alts = $1K across 5 tokens.

## Portfolio Performance

| Metric | Value |
|--------|-------|
| Portfolio | $9,969.06 |
| BTC HODL | $9,759.73 |
| Alpha vs BTC | +2.09% |
| Max Drawdown | 0.4% |
| Win Streak | 8 cycles |

## Market Scores

| Level | Score | Signal |
|-------|-------|--------|
| L1 Liquidity | 4.0 | $312B stablecoins — BULLISH |
| L2 Macro | 2.0 | F&G 18 Extreme Fear — BEARISH |
| L3 Cycle | 1.75 | BTC -46% ATH, 30d -5.9% — BEARISH |
| L4 Sectors | 1.5 | 2/14 positive (UNI, HYPE) — BEARISH |
| **Composite** | **2.31** | **DEFENSIVE** |

## Key Finding

Score 2.31 DEFENSIVE. Alt basket LIVE in paper mode. ARB (75.4), SUI (70.1), UNI (65.1) top picks by opportunity score. 0.19pts from CAUTIOUS which deploys real alt positions. $312B stablecoin powder keg + 80% ACCUMULATION. Portfolio $9,969 (+2.09% alpha vs BTC, 8W streak). System ready to rotate into alts the moment conditions improve.

## Sources
CoinGecko (prices, ATH, 7d/30d), Alternative.me (F&G), DeFiLlama (stablecoins, TVL)
