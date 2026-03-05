# cycles/log.md — Erasto Cycle History
# APPEND-ONLY. Never delete entries.
# Format: [CYCLE N] [DATE UTC] [TASK COMPLETED] [SCORE SUMMARY] [STATUS]

[CYCLE 0] [2026-03-04] [REPO INITIALIZED BY OPERATOR] [Scores: pending] [READY — awaiting Cycle 1]

[CYCLE 1] [2026-03-04 UTC] [RESEARCH BRIEF #001 — FRAMEWORK SNAPSHOT L1-L4] [L1:MIXED L2:CAUTIOUS L3:BEAR L4:SELECTIVE] [COMPLETE]
- Task: Understand 6-level framework, research current state, begin publishing
- Output: outputs/cycle1_framework_snapshot_2026-03-04.md (181 lines, 12K)
- Key finding: Global M2 at ATH ($22.44T), but bear market conditions persist (BTC ~$73K, -35% from $111K ATH). Tactical bounce today on US-Iran haven demand. CryptoQuant bear bottom est. ~$55K. AI Agents, RWA, DePIN identified as infrastructure narratives leading next cycle.
- Sources: 13 cited (CryptoQuant, CoinTelegraph, CoinDesk, TradingEconomics, BlockEden, etc.)
- Blockers: None

[CYCLE 1 — ADDENDUM] Telegram notification: BLOCKED — "chat not found" error. Bot @erastoaibot is valid and authenticated. TELEGRAM_CHAT_ID var is set but the target chat is not reachable (possible: operator has not started a conversation with the bot, or chat ID format issue). Operator must send /start to @erastoaibot to initialize the chat. This is a one-time setup action.

[CYCLE 3] [2025-06-27 UTC] [RESEARCH BRIEF #002 — SECTOR PROTOCOL MAP L4->L5] [RWA:STRONG DePIN:STRONG AI-AGENTS:MOMENTUM] [COMPLETE]
- Task: Deep-dive 3 winning narratives (AI Agents, RWA, DePIN). Top 5 protocols per sector with real traction.
- Output: outputs/cycle3_sector_protocol_map_2025-06-27.md (192 lines)
- Key finding: RWA/DePIN/AI Agents are 3 access points to 1 AI mega-trend. AI needs DATA+COMPUTE+AGENTS+CAPITAL — crypto is building the full stack.
- L5 leaders: Ondo (TVL ATH 1.4B), Akash (#1 DePIN revenue), Bittensor (AI infra), Render (GPU compute), Virtuals (agent momentum)
- Macro update: BTC 107K — bull market confirmed. Stagflation risk at L2 but liquidity expansion dominates.
- Sources: 13 cited (CoinDesk, Messari, Binance Research, DePIN Space, Blockonomi, BlockEden, etc.)
- Blockers: Sandbox ephemeral (re-clone each cycle). Telegram chat may need /start from operator.

---
[CYCLE 4] [2025-06-27] [TASK: Develop repeatable scoring system for 6-level framework] [STATUS: DONE]
- Output: outputs/cycle4_scoring_system_2025-06-27.md
- Key finding: Erasto Scoring System v1.0 locked. 16 indicators across L1-L4. Composite formula: (L1x0.30)+(L2x0.25)+(L3x0.25)+(L4x0.20). Live score: 3.24/5.0 = CAUTIOUS OPPORTUNITY.
- L1=3.5 (M2 ATH $142T but rates elevated), L2=2.25 (stagflation risk, Fed trapped), L3=3.5 (14mo post-halving, BTC $107K, belief phase), L4=3.75 (AI/RWA/DePIN all active)
- Signal: Selective deployment. Quality L5 protocols (Ondo, Akash, Render). Not blanket exposure.
- Blockers: None. Sandbox ephemeral — re-clone each cycle. Telegram delivery to be confirmed.

---
[CYCLE 12] [2026-03-05 UTC] [TASK: Portfolio Allocation Model v1.0] [STATUS: DONE]
- Output: outputs/cycle12_portfolio_allocation_model.md (162 lines)
- Key finding: Score-to-Allocation matrix locked. 5 phases map composite score (1-5) to exact BTC/Alts/Stables percentages.
- Live score: 2.58/5.0 = CAUTIOUS -> 35% BTC / 10% Alts / 55% Stables
- Score delta: -0.66 from 3.24 (Jun 2025). Drivers: US-Iran war (L2=1.75), DXY surge (L1=2.75)
- Market: BTC $71,313 (-36% ATH), F&G 22 (Extreme Fear), DeFi TVL $98.4B, Stablecoins $265B
- Rebalancing rules: Phase boundary cross, delta>=0.50, emergency<1.5, 14-day minimum
- Alt rules: Score>=2.5, top-3 sector, vol>$10M, no memes, max 5% each
- Watchlist: Ondo (HOLD), Akash (HOLD), Render (WATCH)
- Blockers: None. Next = Cycle 13 historical data collection for backtesting.

---

### [CYCLE 14] [2026-03-05] [Historical Data Collection]
- **Task:** Build backtesting dataset (2020 Q1 → 2026 Q1) with quarterly BTC/ETH prices + L1-L4 scores
- **Finding:** 25 quarterly data points. Score range 1.50-4.25. All composites math-verified.
- **Key insight:** L1 leads BTC price 1-2 quarters. Score ≥3.5 = profitable next Q (8/9). Score <2.0 = capital destruction.
- **Distribution:** 44% Cautious, 36% Lean Aggressive, 16% Defensive, 4% Max Offense
- **2025 Q2-Q4 flagged estimated (~)** — need verified data to refine
- **Files:** `data/historical_quarterly_2020_2026.csv`, `scripts/data_collector.py`, `outputs/cycle14_historical_data_2020_2026.md`
- **Status:** ✅ DONE
- **Next:** Cycle 15 = Backtest portfolio model ($10K sim vs BTC buy-and-hold, CAGR, drawdown)

---

### [CYCLE 15] [2025-06-29] [Backtest Portfolio Model]
- **Task:** Validate Erasto allocation model against 25 quarters of historical data (2020-Q1 to 2026-Q1)
- **Engine:** Built `scripts/backtest_engine.py` — simulates $10K portfolio across 3 strategies
- **Finding — Erasto Model:** $10K → $94,188 (+842%), CAGR 45.3%, Max DD -16.5%, Sharpe 0.80
- **Finding — BTC B&H:** $10K → $110,993 (+1,010%), CAGR 49.4%, Max DD -71.9%, Sharpe 0.76
- **Finding — 60/40 Static:** $10K → $66,228 (+562%), CAGR 37.0%, Max DD -46.9%, Sharpe 0.73
- **Key Insight:** Erasto captures 83% of BTC returns with only 23% of drawdown risk. Best Sharpe ratio of all three.
- **Bear market edge:** In 2022, Defensive mode (20% BTC, 80% stables) limited losses to -16.5% while BTC B&H lost -71.9%
- **Bull market tradeoff:** Model lags during explosive rallies due to lagging score confirmation — acceptable for retail risk management
- **Data note:** 2025-Q2 through 2026-Q1 uses estimated scores from Cycle 14. Core backtest (2020-Q1 to 2025-Q1) = verified.
- **Current signal:** Score 3.60 → Lean Aggressive → 45% BTC / 30% Alts / 25% Stables
- **Files:** `outputs/cycle15_backtest_results.md`, `scripts/backtest_engine.py`
- **Status:** ✅ DONE
- **Next:** Cycle 16 = Risk Metrics Framework (formalize drawdown/Sharpe/volatility tracking)
