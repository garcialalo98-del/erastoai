# Cycle 23: Automated Data Pipeline v1.0
**Erasto v3** | 2026-03-06 | Fetch → Score → Allocate → Format → Send

---

## What Was Built
`scripts/erasto_pipeline.py` (124 lines) — End-to-end automation:

1. **Fetches** 7 API calls: BTC/ETH/SOL prices, F&G, global data, stablecoins, TVL, BTC 30d chart, 10 sector tokens
2. **Scores** L1-L4 with quantified rules (no manual input needed)
3. **Maps** composite → allocation % (v2 model)
4. **Formats** mobile dashboard (EN + ES, <2K chars)
5. **Sends** via Telegram bot
6. **Saves** JSON snapshot to `data/current_market.json`

### Usage
```
python3 scripts/erasto_pipeline.py --dry-run   # Display only
python3 scripts/erasto_pipeline.py --send       # Full pipeline + Telegram
```

### Scoring Rules (Automated)
| Level | Input | Thresholds |
|-------|-------|-----------|
| L1 Liquidity | Stablecoin Δ% vs baseline | >10%=4, >5%=3.5, >0%=3, neg=2 |
| L2 Macro | Fear & Greed Index | ≥75=4, ≥50=3.5, ≥25=2.5, ≥10=2, <10=1 |
| L3 Cycle | BTC/ATH ratio + 30d momentum | Avg of ATH distance + momentum |
| L4 Sectors | % of 10 alts positive 30d | >70%=3.5 ... <10%=1.5 |

---

## Live Results (2026-03-06)

**Score: 2.44/5.0 → DEFENSIVE (20% BTC / 0% Alts / 80% Stables)**

| Metric | Value | vs C21 |
|--------|-------|--------|
| BTC | $70,109 | -$200 (flat) |
| ETH | $2,048 | -$3 (flat) |
| F&G | 18 Extreme Fear | unchanged |
| Stablecoins | $311.7B | +$39.9B (+14.7%) ⚡ |
| DeFi TVL | $97.9B | flat |
| BTC Dominance | 57.0% | +1% |
| Score | 2.44 | +0.19 (L1 upgrade) |

### The $312B Powder Keg
Stablecoins surged +$40B since C21 while BTC stayed flat at $70K. This is the largest liquidity build in Erasto's history. L1 scores 4.0/5 (most bullish level) but L3-L4 show ongoing capitulation. Historical pattern: this divergence resolves violently.

**Watch trigger:** F&G crossing 25 → shift to CAUTIOUS (35% BTC).

### Sector Heatmap
- 🟢 MKR +21.7% (DeFi governance = only sector working)
- 🟢 UNI +1.8%
- 🟡 LINK -5.2%, ONDO -6.7%, AAVE -9.7%
- 🔴 RENDER -10.2%, IMX -12.6%, DOGE -13.1%, PEPE -18%, ARB -24.3%

Only 2/10 alts positive = broad capitulation. No alt season signal.

---

## Telegram Delivery
- ✅ EN: Message ID 25
- ✅ ES: Message ID 26

## Architecture
- Runtime: ~30s (7 API calls, 4s delays)
- Dependencies: Python 3 stdlib only (no pip installs)
- Rate limit safe: 4s between CoinGecko calls
- Cron-ready for weekly automation
