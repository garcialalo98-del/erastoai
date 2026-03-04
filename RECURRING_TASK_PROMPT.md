# RECURRING TASK PROMPT — Erasto
# Deploy in MoltStreet as: "Recurring Task"
# Target: ≤1000 characters. Zero overlap with Identity Prompt.
# Count characters carefully before deploying.

---

CYCLE START:
1. Run: `git clone [REPO_URL] /repo && cd /repo`
2. Run: `cat SOUL.md && tail -5 cycles/log.md`
3. Run: `cat BACKLOG.md` — pick top uncompleted task
4. Execute the task. Only read additional files if the task requires them.
5. Save output to `/repo/outputs/[filename].md`
6. Update BACKLOG.md (mark task done)
7. Append to cycles/log.md: `[CYCLE N] [DATE] [TASK] [SCORE CHANGES] [STATUS]`
8. Run: `git add -A && git commit -m "Cycle N: [task]" && git push`
9. Send Telegram to operator: cycle #, task done, macro traffic light, any blockers.

RULES:
- If stuck >2 tries: log [BLOCKED], move to next task, notify operator.
- If credits <$3: push state, log [LOW CREDIT], stop.
- Never read full repo. SOUL.md + log tail only unless needed.

# CHARACTER COUNT TARGET: ~850 chars (leave buffer for repo URL substitution)
