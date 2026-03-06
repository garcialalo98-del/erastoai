# Cycle 19: Automated Data Collection Script
**Date:** 2026-03-06 | **Task:** BACKLOG CYCLE 18 — Automated Data Feeds

---

## Summary

Built and deployed `data/data_collector.py` — a cron-ready Python script that fetches all market data Erasto needs from 100% free APIs. Zero API keys. Zero cost. Runs in ~8 seconds.

**Status:** ✅ ALL 5 FEEDS OPERATIONAL — tested live 2026-03-06

---

## What It Collects

| # | Feed | Source | Data Points |
|---|------|--------|-------------|
| 1 | **Prices** | CoinGecko | BTC, ETH, SOL: price, 24h change, market cap, volume |
| 2 | **Global** | CoinGecko | BTC/ETH dominance, total market cap, 24h volume, mcap change |
| 3 | **Stablecoins** | CoinGecko | USDT, USDC, DAI market caps + total supply |
| 4 | **Fear & Greed** | Alternative.me | Current value, classification, 7-day avg, 7-day history |
| 5 | **DeFi TVL** | DeFiLlama | Total TVL, 7-day change %, 30-day change % |

---

## Architecture

```
data/
├── data_collector.py          # Main script (147 lines)
├── current_market.json        # Latest data (overwritten each run)
└── snapshots/
    └── market_YYYY-MM-DD.json # Daily snapshots (append-only history)
```

### Key Design Decisions
- **Rate limiting:** 2.5s delay between CoinGecko calls (3 calls total = ~8s runtime)
- **Retry logic:** 3 attempts per endpoint with exponential backoff on 429s
- **Graceful degradation:** If 1-2 feeds fail, marks status "partial" — still saves what works
- **Summary block:** Pre-computed dashboard-ready values (no parsing needed downstream)
- **Snapshot history:** Daily files enable week-over-week delta tracking

---

## Usage

```bash
# Standard run (saves to data/ folder)
python3 data/data_collector.py

# Verbose mode
python3 data/data_collector.py --verbose

# Custom output directory
python3 data/data_collector.py --output /path/to/dir

# Cron (run daily at 8:00 UTC)
0 8 * * * cd /path/to/erastoai && python3 data/data_collector.py >> /var/log/erasto.log 2>&1
```

---

## Live Test Results (2026-03-06)

```
==================================================
  ERASTO COLLECTOR — 2026-03-06
==================================================
  BTC: $70,523 (-3.5%)
  ETH: $2,064 | SOL: $88
  F&G: 18 (Extreme Fear) | 7d avg: 14.1
  Dom: 57.0% | MCap: $2.47T
  TVL: $98.01B (+2.9% 7d)
  Stables: $265.5B tracked
  Status: OK (all 5 feeds)
==================================================
```

---

## Output Schema (current_market.json)

```json
{
  "meta": { "version", "ts", "date", "status", "errors" },
  "prices": { "btc_price", "btc_24h_change", "btc_market_cap", "btc_24h_vol", ... },
  "global": { "btc_dominance", "eth_dominance", "total_mcap_usd", "total_vol_24h" },
  "stablecoins": { "usdt_mcap", "usdc_mcap", "dai_mcap", "total", "total_b" },
  "fng": { "value", "label", "avg_7d", "hist_7d" },
  "defi": { "tvl", "tvl_b", "chg_7d", "chg_30d" },
  "summary": { /* pre-computed dashboard values */ }
}
```

---

## How This Feeds the Dashboard

Before this script, every cycle required 5+ manual API calls. Now:

1. **Pre-cycle:** Run `python3 data/data_collector.py` (~8 seconds)
2. **During cycle:** Read `current_market.json` — all data ready
3. **Score calculation:** `summary` block maps directly to scoring inputs
4. **Delta tracking:** Compare today's snapshot vs last week's snapshot
5. **Cycle 20 dashboard:** Will consume this file directly

---

## Integration with current_score.json

The collector output maps to scoring inputs:

| Collector Field | Score Input | Level |
|----------------|-------------|-------|
| `fng.value` / `fng.avg_7d` | Fear & Greed | L1 |
| `stablecoins.total_b` | Stablecoin supply growth | L1 |
| `global.btc_dominance` | BTC dominance | L3 |
| `defi.tvl_b` / `defi.chg_7d` | DeFi TVL momentum | L4 |
| `prices.btc_24h_change` | Short-term momentum | L3 |
| `global.total_mcap_usd` | Total market cap | L1 |

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Single API timeout | Retry 3x with backoff, mark error, save rest |
| Rate limited (429) | Wait 10-30s, retry with increasing delays |
| 2 feeds fail | Status = "partial" — dashboard shows warning |
| 3+ feeds fail | Status = "degraded" — dashboard flags critical |
| All feeds fail | Status = "degraded", empty sections saved |

---

## What's Next

- **Cycle 20:** Full Quant Dashboard Launch — will consume `current_market.json` directly
- **Future:** Add FRED data (DXY, US10Y) when free endpoint identified
- **Future:** Sector token prices in one batch call (for sector tracker automation)

---

*Built by Erasto AI — Cycle 19 | Institutional intelligence, zero cost.*
