# Loop Catalog (disclosed reference for `debug`)

Ways to construct a tight feedback loop, roughly in order. Pick the first one that fits; the loop is the skill, everything else is mechanical.

1. **Failing test** at whatever seam reaches the bug: `pytest -q path/test_x.py::test_y`. Unit, integration, or e2e.
2. **HTTP script** against a running dev server: `curl -s localhost:8000/predict -d @fixture.json | diff - expected.json`.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot: `cmd < fixture.in | diff - fixture.good`.
4. **Replay a captured trace.** Save the real request/payload/event log to disk; replay it through the code path in isolation: `python replay.py --trace traces/bug-123.json`.
5. **Throwaway harness.** One service, mocked deps, single function call exercising the bug path. Delete after (see SKILL.md cleanup).
6. **Bisection harness.** Bug appeared between two states? Automate "checkout X, run loop, report" so `git bisect run ./loop.sh` works.
7. **Differential loop.** Same input through old vs new (or two configs), `diff` the outputs.
8. **Fuzz loop.** "Sometimes wrong output"? Run N random inputs and count the failure mode: `python fuzz.py --n 1000`.

Tighten on three dimensions: **faster** (cache setup, narrow scope), **sharper** (assert the exact symptom, not "didn't crash"), **deterministic** (pin time/seed, isolate filesystem). A 2-second deterministic loop is the target; a 30-second flaky one is barely a loop.
