# Cycle 29: Custom Watchlist System v1.0

**Date:** 2025-07-27 | **Score:** 2.44/5.0 → DEFENSIVE  
**Allocation:** 20% BTC | 0% Alts | 80% Stables

---

## What Was Built

Custom Watchlist — a configurable token tracking system that:
1. Reads `data/watchlist_config.json` (user-editable sectors + tokens)
2. Fetches live price, momentum, ATH data for all tokens (CoinGecko free API)
3. Scores each token 0-100 on **Opportunity Score** (ATH discount + 7d momentum + 30d oversold)
4. Generates sector-level heatmap (7d/30d averages)
5. Fires configurable alerts (deep value, hot momentum, oversold)
6. Delivers via Telegram in EN + ES

## Files Created

| File | Purpose | Lines |
|------|---------|-------|
| `scripts/custom_watchlist.py` | Reusable watchlist engine | 118 |
| `scripts/run_cycle29.py` | Full pipeline: dashboard + watchlist | 64 |
| `data/watchlist_config.json` | Editable config (6 sectors, 14 tokens) | 20 |
| `data/watchlist_snapshot.json` | Latest market snapshot | auto |

## Top Opportunities (Opportunity Score)

| Rank | Token | Price | 7d | 30d | ATH% | Score |
|------|-------|-------|----|-----|------|-------|
| 1 | ARB | $0.0998 | +0.5% | -23.8% | -96% | 77 |
| 2 | SUI | $0.901 | +0.2% | -17.7% | -83% | 72 |
| 3 | TIA | $0.329 | +3.2% | -10.3% | -98% | 70 |
| 4 | PENDLE | $1.21 | -3.2% | -18.5% | -84% | 65 |
| 5 | LINK | $8.78 | +1.2% | -6.1% | -83% | 60 |
| 6 | UNI | $3.84 | +3.4% | +1.0% | -91% | 60 |

## Sector Heatmap

| Sector | 7d | 30d | Signal |
|--------|----|----|--------|
| 🟢 AI/DePIN | +5.5% | -12.4% | Recovering |
| 🟢 L1/L2 | +2.0% | -15.1% | Stabilizing |
| 🟢 RWA | +0.2% | -6.4% | Resilient |
| 🟡 DeFi | -0.0% | -9.2% | Flat |
| 🟡 Meme | -5.0% | -16.9% | Weak |
| 🔴 Gaming | -5.1% | -12.7% | Lagging |

## Key Alerts Fired

- 🔥 **HYPE +14.8% 7d** — Strongest momentum on the watchlist
- 🟢 **9 tokens at >80% ATH discount** — Broad deep value zone
- 🧊 **ARB -23.8%, EIGEN -25.6% 30d** — Most oversold

## Opportunity Scoring Logic

```
ATH Discount (0-40pts): >90% off = 40pts (max contrarian value)
7d Momentum (0-30pts): >15% = 30pts (recovery confirmation)  
30d Oversold (0-30pts): <-25% = 30pts (capitulation zone)
Total: 0-100 (higher = better risk/reward NOW)
```

## How to Use

1. **Edit** `data/watchlist_config.json` — add/remove tokens per sector
2. **Run** `python3 scripts/custom_watchlist.py --send` for Telegram delivery
3. **Integrate** with pipeline: `run_cycle29.py` runs both dashboard + watchlist
4. Opportunity Scores are relative — compare tokens, not absolute thresholds

## Market Context

- **BTC $68,152** (-46% ATH) | **F&G 18** (Extreme Fear)
- **$311.7B stablecoins** (+$40B from baseline) — powder keg
- **L1 Liquidity 4.0/5** strongest level — money parked, waiting
- **L2-L4 all below 2.5** — sentiment, cycle, sectors still bearish
- **Phase: DEFENSIVE** — capital preservation, accumulate quality only

## Telegram Delivery

- ✅ Dashboard EN (msg 38) + ES (msg 39)
- ✅ Watchlist EN (msg 40) + ES (msg 41)
- 4 messages, all <4096 chars, mobile-optimized

---

*Erasto v3 | Not financial advice | Data: CoinGecko, Alternative.me, DeFiLlama*
