---
name: debug
description: "Prove the root cause of a failure with a tight red-capable feedback loop. Use when the user reports something broken, throwing, failing, or slow, or says diagnose/debug this."
---

# Debug Skill (Root Cause Proof)

A discipline for hard bugs. Skip phases only when explicitly justified. The loop is the skill: with a tight pass/fail signal for *this* bug you will find the cause; without one, no amount of staring at code saves you.

## Hard Rules
- **ZERO CODE EDITS**: Never edit implementation code while in debug mode. Probes and throwaway harnesses live outside the tree or die in cleanup.
- **LOOP BEFORE HYPOTHESIS**: Jumping straight to a theory before a red-capable command exists is the exact failure this skill prevents.
- **MINIMISE BEFORE FIX**: A minimal repro shrinks the hypothesis space and becomes the regression test.

## Redact
This skill shows commands, outputs, and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place, keep credentials in env vars, quote only the lines carrying the signal. If redacted output is insufficient to diagnose, say so and ask the user — never proceed on unredacted secrets.

## Protocol
1. **Build the feedback loop**:
   - Pick the first fitting construction from `loop-catalog.md` (failing test → HTTP script → CLI fixture → trace replay → harness → bisect → differential → fuzz).
   - Spend disproportionate effort here. Be aggressive: refuse to give up on loop-less bugs.
   - Genuinely impossible? Stop and say so: list what you tried and ask for (a) access to a reproducing env, (b) a redacted captured artifact (log dump, HAR, traceback), or (c) permission for temporary instrumentation.
   - **Completion criterion:** one named command (script path, `pytest -q ...`, `curl ...`) already run at least once with redacted output shown, that is red-capable (drives the bug path, asserts the user's exact symptom), deterministic, fast (seconds), and agent-runnable.
2. **Reproduce + minimise**:
   - Confirm the loop shows the *user's* failure, not a nearby one; reproducible across runs (or a pinned high rate for flakes: loop 100×, parallelise, stress timing).
   - Shrink to the smallest scenario still red: cut inputs, callers, config, data one at a time, re-running after each cut.
   - **Completion criterion:** every remaining element is load-bearing — removing any one turns the loop green.
3. **Hypothesise**:
   - Generate 3–5 ranked, falsifiable hypotheses before testing any: format "If <cause>, then <probe> will make the bug disappear/worsen." No prediction = vibe, discard it.
   - Show the ranked list to the user first (they re-rank instantly from deploy memory); proceed with your ranking if AFK.
   - Trace the failing symbol with GitNexus (`impact`, `query`) or call-stack inspection to ground each hypothesis; check dynamic dispatch before ruling anything dead.
   - **Completion criterion:** ranked falsifiable list shown, each mapped to a probe.
4. **Instrument**:
   - One variable per probe. Preference: debugger/REPL breakpoint first, then targeted logs at hypothesis boundaries — never "log everything and grep".
   - Tag every debug log with a unique prefix (`[DEBUG-a4f2]`) so cleanup is one `grep`.
   - Perf branch: measure first (timing harness, profiler, query plan via `rtk psql` + `EXPLAIN`), then bisect. Logs are usually wrong for regressions.
   - **Completion criterion:** exactly one surviving hypothesis, evidenced by probe output.
5. **Deliverable**:
   - Root Cause Proof Report: exact line numbers and failing symbols, proven mechanism with reproduction command, the hypothesis that held, and a hand-off recommendation to `fix`.
   - Cleanup before declaring done: repro no longer reproduces after a fix is applied elsewhere (or note it still does), all `[DEBUG-...]` tags removed (`grep -r "DEBUG-"`), throwaway harnesses deleted.
   - **Completion criterion:** report exists, cleanup verified by `grep`, `fix` can start with zero re-derivation.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Same contract as official `ak:debug` (prove cause before touching code); interchangeable.
