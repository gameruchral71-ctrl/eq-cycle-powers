# Equivalence covers of powers of cycles, k = 2^m − 1

Problem: Yang, arXiv:2610.15635 (11 Oct 2026). It leaves eq(C_n^k) undecided between m+1 and m+2 when k+1 = 2^m and n is even but not divisible by k+1.

Result (this folder): for k = 3 and k = 7 and every n ≥ 2k+2, eq(C_n^k) = m+1 if (k+1) | n, and m+2 otherwise. A weight lemma valid for all m gives the structure of optimal covers. The general case is a conjecture.

Proposed by Uchral Nyam-Osor; mathematics and computations by Claude (AI). Not peer reviewed.

- `paper/main.tex`, `paper/main.pdf`: the readable write-up.
- `tight.py`: weights and tight sets.
- `satscan.py`: transfer graph via SAT. `python3 satscan.py 2 24 8` (k=3), `python3 satscan.py 3 48 20` (k=7).
- `layerscan.py`, `c/layerscan.cpp`: direct window enumeration. Feasible for k=3 only.
- `eqsat.py`, `upper.py`: SAT covers with independent checks. Certificates are in `witness.tar.gz` (unpacks to `witness/`), logs in `logs/upper*.log`.
- Older exploration scripts: `dual.py`, `frac.py`, `localscan.py`, `structure.py`, `classtypes.py`, `show.py`, `invariant.py`, `local4.py`.
