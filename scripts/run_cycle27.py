#!/usr/bin/env python3
"""Cycle 27 runner: fetch, score, visualize, send via TG"""
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__)))
# Uses erasto_pipeline.py for data + score_trend_viz.py for visualization
# See cycle27_score_trend_visualization.md for full results
# Run: python3 scripts/run_cycle27.py
from erasto_pipeline import get_data, score, alloc_for
from score_trend_viz import load_history, gen_timeline, gen_levels, gen_momentum, sparkline, bar
import json
CSV = os.path.join(os.path.dirname(__file__),"..","data","score_history.csv")
rows = load_history(CSV)
if rows:
    print(gen_timeline(rows))
    print(gen_levels(rows))
    print(gen_momentum(rows))
    scores=[float(r.get("composite",0)) for r in rows]
    print(f"Score sparkline: {sparkline(scores,20)}")
else:
    print("No history data. Run erasto_pipeline.py first.")
