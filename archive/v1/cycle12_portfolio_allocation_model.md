# Portfolio Allocation Model v1.0
**Score-to-Action Engine** | Erasto | Cycle 12 | March 5, 2026

---

## Executive Summary
> Composite Score: **2.58 / 5.0 — CAUTIOUS**
> Allocation: **35% BTC | 10% Quality Alts | 55% Stablecoins**
> On $10K: $3,500 BTC / $1,000 Alts / $5,500 Stables
> Context: US-Iran war active, BTC -36% from ATH, Extreme Fear (22), DXY surging

---

## Design Philosophy
1. Score drives allocation, not emotion
2. Capital preservation is the default (need >3.5 for >45% crypto)
3. Simplicity wins — 3 assets, 5 tiers, 10 min to execute

## Asset Classes
| Asset | Role | Examples |
|-------|------|----------|
| BTC | Core store of value | Bitcoin only |
| Quality Alts | Higher beta, sector exposure | Top L5 (Ondo, Akash, Render) |
| Stablecoins | Preservation, dry powder | USDC/USDT, earn yield |

---

## Score-to-Allocation Matrix

| Score | Phase | BTC | Alts | Stables | Crypto |
|-------|-------|-----|------|---------|--------|
| 4.5-5.0 | Max Offense | 50% | 40% | 10% | 90% |
| 3.5-4.4 | Lean Aggressive | 45% | 30% | 25% | 75% |
| 2.5-3.4 | Cautious | 35% | 10% | 55% | 45% |
| 1.5-2.4 | Defensive | 20% | 0% | 80% | 20% |
| 1.0-1.4 | Preservation | 5% | 0% | 95% | 5% |

**Max Offense:** All macro green. Liquidity surging. Alt season likely.
**Lean Aggressive:** Mostly positive. 25% dry powder. BTC leads.
**Cautious:** Mixed signals. Small stack. 55%+ stables.
**Defensive:** Mostly negative. BTC-only at 20%.
**Preservation:** Everything broken. 5% BTC = optionality.

---

## Rebalancing Rules

| Trigger | Action |
|---------|--------|
| Score crosses phase boundary | Rebalance to new phase |
| Score delta >= 0.50 in same phase | Adjust +/-5% per asset |
| Emergency: Score < 1.5 | Immediate Preservation |
| < 14 days since last rebalance | Skip (anti-whipsaw) |

Cross phases gradually: halfway Week 1, complete Week 2. Emergency = immediate.

---

## Alt Allocation Rules

ALL must be true: (1) Score >= 2.5 (2) Sector has positive 30d flows (3) Top-3 by TVL/revenue (4) Vol > $10M (5) No memecoins (6) Max 5% per alt

**Watchlist Mar 2026:** Ondo (RWA, HOLD) | Akash (DePIN, HOLD) | Render (GPU/AI, WATCH)

---

## Live Score — March 5, 2026

### L1 — Global Liquidity: 2.75
| Indicator | Data | Score |
|-----------|------|-------|
| Global M2 YoY | US M2 $22T ATH, ~4% YoY | 3.5 |
| Central bank policy | Fed paused, trapped | 3.0 |
| DXY trend | Surging toward 99, safe-haven | 1.5 |
| US 10Y yield | 4.13%, rising on geopolitics | 3.0 |

*M2 expanding but DXY surge + rising yields = headwinds for risk assets.*

### L2 — Macro & Geopolitics: 1.75
| Indicator | Data | Score |
|-----------|------|-------|
| US CPI | 2.7% YoY, rising (tariffs+war) | 2.0 |
| GDP growth | Slowing, uncertainty | 2.0 |
| Geopolitical risk | US-Iran WAR active | 1.0 |
| VIX | 21.15 (elevated) | 2.0 |

*Weakest level. Active war = dominant variable. Stagflation risk rising.*

### L3 — Crypto Cycle: 3.25
| Indicator | Data | Score |
|-----------|------|-------|
| Halving position | ~22mo post-halving | 2.5 |
| BTC price | $71,313, -36% from ATH | 3.0 |
| Fear & Greed | 22 — Extreme Fear | 4.5 |
| BTC Dominance | 57.1%, declining | 3.0 |

*Strongest level. Extreme Fear is a contrarian buy signal. BTC survives every crisis.*

### L4 — Sector Flows: 2.50
| Indicator | Data | Score |
|-----------|------|-------|
| DeFi TVL | $98.4B | 2.5 |
| Stablecoin supply | $265B dry powder | 3.5 |
| Sector momentum | Risk-off dominating | 2.0 |
| Narrative strength | War suppressing all | 2.0 |

*$265B stablecoin dry powder = fuel for next leg up. But risk-off suppresses activity.*

### Composite Calculation
```
= (2.75 x 0.30) + (1.75 x 0.25) + (3.25 x 0.25) + (2.50 x 0.20)
= 0.825 + 0.4375 + 0.8125 + 0.50 = 2.575 -> 2.58
```

**SCORE: 2.58 / 5.0 — CAUTIOUS**
Delta: -0.66 from 3.24 (Jun 2025) | Driver: L2 collapsed (war), L1 dropped (DXY) | REBALANCE WARRANTED

---

## Current Allocation Recommendation

| Asset | % | On $10K | Rationale |
|-------|---|---------|-----------|
| Bitcoin | 35% | $3,500 | BTC survives wars — core position |
| Quality Alts | 10% | $1,000 | Minimal — highest conviction only |
| Stablecoins | 55% | $5,500 | Majority — earn yield, wait for clarity |

**Why Cautious, not Defensive?** (1) F&G 22 = historically a buying opportunity (2) $265B stablecoin dry powder = fuel (3) M2 still expanding — liquidity hasn't turned negative

### What Changes the Score?
| Event | Impact | New Phase |
|-------|--------|-----------|
| Ceasefire | L2->3.0, Score~3.2 | Cautious, adding |
| War escalation + oil spike | L2->1.0, Score~2.0 | Defensive (20/0/80) |
| Fed emergency cut | L1->4.0, Score~3.0 | Cautious upper |
| BTC reclaims $90K | L3->4.0, Score~2.9 | Cautious, adding alts |

---

## Quick Reference Card
```
ERASTO ALLOCATION MODEL v1.0
=============================
SCORE    PHASE            BTC  ALTS  STABLES
4.5-5.0  Max Offense      50%  40%   10%
3.5-4.4  Lean Aggressive  45%  30%   25%
2.5-3.4  Cautious         35%  10%   55%
1.5-2.4  Defensive        20%   0%   80%
1.0-1.4  Preservation      5%   0%   95%

REBALANCE: Phase boundary | Delta>=0.50 | Emergency<1.5
ALTS: Score>=2.5 | Top-3 sector | Vol>$10M | No memes
>>> CURRENT: 2.58 -> CAUTIOUS -> 35/10/55 <<<
```

---

**Sources:** CoinGecko | Alternative.me | DeFiLlama | FRED | BLS | Reuters/CoinDesk — Cost: $0.00

**Next:** Cycle 13 historical data -> Cycle 14 backtest. Until validated, this is hypothesis, not proven strategy.

*Erasto is a research engine, not a financial advisor. Allocations are educational, not investment advice.*
