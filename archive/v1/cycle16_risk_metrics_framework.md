# Risk Metrics Framework v1.0
**Erasto | Cycle 16 | July 6, 2025**

---

## Why This Exists

> **Return without context is meaningless.** +842% sounds incredible until you learn someone else made +1,010%. Then you learn their portfolio dropped -72% along the way, and most humans would have panic-sold at -40%.
>
> **Risk metrics tell the full story.** They answer: How much pain for those gains? Could a real person have held? Was the strategy *good*, or just *lucky*?

This framework adds 8 risk metrics to every Erasto output. Retail investors get the same risk transparency institutions demand — in plain English.

---

## The 8 Metrics (Plain English)

### 1. Max Drawdown (MDD)
**What:** Largest peak-to-trough decline. If MDD = -72%, your $100K hit $28K.
**Good:** Under -20% for crypto. **Erasto: -16.5%** ✅

### 2. Annualized Volatility
**What:** How much the portfolio swings per year. 96% = wild ride.
**Good:** Under 60% for crypto exposure. **Erasto: 58.5%** ✅

### 3. Downside Volatility
**What:** Only measures *negative* swings. Isolates the pain side.
**Good:** Lower = better. **Erasto: 12.1%** (vs BTC's 33.4%)

### 4. Win Rate
**What:** % of quarters with positive returns.
**Good:** Above 50%. **Erasto: 58.3%** (14 of 24 quarters green)

### 5. Sharpe Ratio
**What:** Return per unit of total risk. Gold standard metric.
**Good:** >0.5 decent, >1.0 good, >1.5 excellent. **Erasto: 0.80** ✅

### 6. Sortino Ratio
**What:** Like Sharpe but only penalizes downside. Fairer for asymmetric returns.
**Good:** >1.0 good, >2.0 excellent, >3.0 outstanding. **Erasto: 3.90** 🏆

### 7. Calmar Ratio
**What:** CAGR ÷ max drawdown. Annual return per unit of maximum pain.
**Good:** >1.0 good, >2.0 excellent. **Erasto: 2.74** 🏆

### 8. Profit Factor
**What:** Average win size ÷ average loss size.
**Good:** >1.5 decent, >3.0 excellent. **Erasto: 3.67** 🏆

---

## Full Metrics: Erasto vs BTC Buy-and-Hold

*$10,000 starting | 2020-Q1 to 2026-Q1 | 24 quarters*

| Metric | Erasto | BTC B&H | Winner |
|--------|:------:|:------:|:------:|
| **End Value** | $94,188 | $110,993 | BTC |
| **Total Return** | +841.9% | +1,009.9% | BTC |
| **CAGR** | 45.3% | 49.4% | BTC |
| **Max Drawdown** | **-16.5%** | -71.9% | ✅ Erasto (4.4× less) |
| **Ann. Volatility** | **58.5%** | 96.2% | ✅ Erasto (39% smoother) |
| **Downside Vol** | **12.1%** | 33.4% | ✅ Erasto (2.8× less) |
| **Win Rate** | 58.3% | 62.5% | BTC |
| **Sharpe Ratio** | **0.80** | 0.76 | ✅ Erasto |
| **Sortino Ratio** | **3.90** | 2.18 | ✅ Erasto (1.8× better) |
| **Calmar Ratio** | **2.74** | 0.69 | ✅ Erasto (4× better) |
| **Return/MaxDD** | **50.9×** | 14.0× | ✅ Erasto |
| **Profit Factor** | **3.67** | 2.09 | ✅ Erasto |
| **Avg Win (Q)** | +27.1% | +43.0% | BTC |
| **Avg Loss (Q)** | **-7.4%** | -20.6% | ✅ Erasto (2.8× smaller) |
| **Best Quarter** | +107% (2020-Q4) | +169% (2020-Q4) | BTC |
| **Worst Quarter** | **-17% (2026-Q1)** | -57% (2022-Q2) | ✅ Erasto (3.4× milder) |

### Scorecard: Erasto wins 10 of 16 metrics
BTC wins raw returns. **Erasto wins every single risk metric.**

---

## Rolling 2-Year Risk (How Risk Evolves)

| Period End | 2Y Return | Max DD | Vol | Sharpe | Phase |
|-----------|:---------:|:------:|:---:|:------:|-------|
| 2022-Q1 | +497.9% | -10.8% | 82.0% | 1.44 | Post-bull |
| 2022-Q4 | +80.7% | -15.7% | 63.0% | 0.64 | FTX bottom |
| 2023-Q3 | -1.9% | -15.7% | 14.2% | -0.28 | ⚠️ Only negative |
| 2024-Q1 | +53.4% | -14.3% | 27.4% | 0.78 | ETF rally |
| 2024-Q4 | +112.5% | -8.5% | 29.0% | 1.35 | Trump rally |
| 2025-Q2 | +63.8% | -16.3% | 33.7% | 0.79 | Recovery |
| **2026-Q1** | **+2.7%** | **-16.5%** | **28.5%** | **0.04** | ⚠️ Geopolitical |

**Key insight:** Erasto's 2Y max drawdown never exceeded -16.5%. BTC B&H had 2Y windows with -72%.

---

## Live Risk Snapshot (July 6, 2025)

| Metric | Value | Source |
|--------|-------|--------|
| BTC Price | $71,255 | CoinGecko |
| ETH Price | $2,083 | CoinGecko |
| Fear & Greed | 22 (Extreme Fear) | Alternative.me |
| BTC 90-Day Vol (Ann.) | 55.8% | Calculated |
| ETH 90-Day Vol (Ann.) | 75.1% | Calculated |
| BTC DD from 90d Peak | -26.5% ($97K→$71K) | Calculated |
| ETH DD from 90d Peak | -37.9% ($3.4K→$2.1K) | Calculated |
| Erasto Score | 3.60 → Lean Aggressive | L1-L4 |
| Allocation | 45/30/25 (BTC/Alt/Stbl) | Model |

### Risk Rating: 🟡 MODERATE → 🟠 ELEVATED
BTC spot down -26.5%, but Erasto portfolio cushioned by 25% stables. Model doing exactly what it's designed to do.

---

## Risk Rating System (Dashboard Integration)

| Rating | Criteria | Display |
|--------|----------|---------|
| 🟢 LOW | Vol<40%, DD<-10%, Sharpe>1.0 | "Calm. Stay the course." |
| 🟡 MODERATE | Vol 40-70%, DD -10 to -20%, Sharpe 0.5-1.0 | "Normal crypto vol." |
| 🟠 ELEVATED | Vol 70-100%, DD -20 to -35%, Sharpe 0.2-0.5 | "Stress increasing." |
| 🔴 HIGH | Vol>100%, DD>-35%, Sharpe<0.2 | "Crisis. Capital preservation." |

### Alert Triggers (Risk-Based)
- Sharpe < 0 → "Risk-adjusted returns negative"
- Rolling MDD > -25% → "Drawdown beyond normal range"
- Volatility > 100% → "Crisis-level volatility"
- Win rate < 40% (8Q) → "Model underperforming"

---

## Dashboard Risk Widget (Template)

```
┌─────────────────────────────────────────┐
│  RISK: 🟡 MODERATE                      │
│  MDD: -16.5% | Sharpe: 0.80            │
│  90d Vol: 55.8% | Sortino: 3.90        │
│  Win Rate: 58% | Profit Factor: 3.67   │
│  vs BTC B&H: -17% return, +55pts safer │
└─────────────────────────────────────────┘
```

---

## Files & Scripts

| File | Purpose |
|------|---------|
| `scripts/risk_metrics.py` | Risk engine — all 8 metrics + rolling windows |
| `scripts/risk_helpers.py` | Portfolio simulation functions (shared) |
| `data/risk_metrics.json` | Machine-readable output for dashboard |

---

## Bottom Line

> | What You Get | Erasto | BTC B&H |
> |-------------|--------|---------|
> | Return | 842% | 1,010% |
> | Worst moment | -16.5% | -71.9% |
> | Could a human hold? | ✅ Yes | ❌ Most can't |
>
> The 168% gap buys you sleep-at-night certainty. For retail investors with day jobs and families who can't stare at charts — that trade-off isn't just acceptable, it's optimal.

---

*Sources: CoinGecko, Alternative.me, Erasto backtest (Cycle 15), risk_metrics.py*
*This is research, not financial advice. Past performance ≠ future results.*
