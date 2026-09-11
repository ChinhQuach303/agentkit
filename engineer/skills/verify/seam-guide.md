# Seam Guide (disclosed reference for `verify`)

A **seam** is the public boundary you test at: the interface where behavior is observed without reaching inside. Tests live at seams, never against internals.

## Confirming seams (do this first)

Before any test is written, write down the seams under test and confirm them with the user: "What's the public interface, and which seams should we test?" No test at an unconfirmed seam. Effort lands on critical paths and complex logic, not every edge case.

## Good seams by stack

- **HTTP API**: route + status + payload shape: `pytest -q tests/test_predict.py -k "status or schema"`, or `curl -s localhost:8000/health | grep -q 200`.
- **CLI**: argv in, stdout/exit-code out: `cmd --input fixture.in; echo $?`, snapshot-diff stdout for regressions.
- **Library function**: public function signature with fixed inputs: `pytest -q tests/test_metrics.py::test_wmape_known_value`.
- **Pipeline step**: staged frame in, staged frame out at partition boundaries; assert row counts + schema, not internals.
- **LLM output**: schema-validated JSON + rubric scores at temperature=0; assert fields and enum values, never prose exact-match.

## Bad seams (false confidence)

- Testing private helpers directly: breaks on refactor while behavior holds.
- Single-caller unit test for a multi-caller chain bug: can't replicate the triggering chain.
- Querying the database instead of using the interface: verifies through a side channel.
