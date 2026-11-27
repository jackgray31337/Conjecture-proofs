# Conjecture proofs

## Gvozdjak's graceful-path endpoint conjecture

This directory contains a research draft claiming a constructive proof of the sufficiency direction of Gvozdjak's Conjecture 5.1.1. For every admissible ordered endpoint pair \((a,b)\) on labels \(0,\ldots,r-1\), it constructs a graceful permutation: every label appears once and consecutive absolute differences are exactly \(1,\ldots,r-1\).

Its coverage reductions use exact integer-set arithmetic with libisl; the accompanying Python programs construct witnesses and check the finite residual cases. The independent audit included here reports no mathematical gap in the induction. Publication priority and external specialist review have not been established, so treat this as a research draft for further scrutiny.

### Files

- [Proof and construction](graceful-endpoints/proof.md)
- [Reproduction audit](graceful-endpoints/audit/AUDIT.md)
- [Lean file](graceful-endpoints/GracefulEndpoints.lean)
- [Original proof and audit ZIP bundles](graceful-endpoints/archive/)

The Lean file is a partial formalization of definitions, sample witnesses, symmetry lemmas, and arithmetic identities. It does **not** formalize the full induction or prove the full conjecture; see its `of_descent` theorem, whose induction step remains an assumption.

### Reproducing the computational checks

From `graceful-endpoints/`, with Python 3 and libisl available, run:

```sh
python3 coverage.py
python3 audit/forward_check.py
python3 audit/independent_tests.py
```

The audit records the tested Python/libisl versions and the precise scope of each check.
