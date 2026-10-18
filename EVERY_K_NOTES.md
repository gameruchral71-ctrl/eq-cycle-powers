# Notes toward the every-k proof (2026-10-18)

Goal: for k = 2^m − 1 and n ≥ 2k+2, an (m+1)-layer equivalence cover of C_n^k exists only if N = 2^m divides n.

## Stronger statement H(m) (designed for induction)
An H(m) system on Z_n (n ≥ 2N) consists of the following:
- one tight set S_v (level m) with left end v, for each v;
- a colour for each class, from a set C, where classes of one colour are disjoint;
- every vertex lies in exactly m+1 classes;
- every pair at distance ≤ k is covered;
- the set M(v) of colours missing at v satisfies M(v) = M(v+N).

With |C| = m+1, an H(m) system is exactly an (m+1)-layer cover (M = ∅).

**Conjecture H:** an H(m) system on Z_n exists only if N | n.

- **m = 1 (proved).** Classes are the edges {v, v+1}. Each vertex sees 2 colours, and M is 2-periodic. If n is odd, M is constant, so the edges of an odd cycle are properly 2-coloured, which is impossible.
- **m = 2, 3 (SAT, `relaxed.py`).** No H(m) system exists for N ∤ n among the tested n: m=2 with extra colours 0–2, n ≤ 22; m=3 with 1 extra colour, n ≤ 26.

## Proposed induction step: decimation (`reduce_test.py`, `relaxed_lib.py`)
1. Keep the vertices of one parity, optionally after reflecting x ↦ −x.
2. Restrict every class to those vertices and drop the singletons.
3. Halve the positions.
4. The colours stay the same.

Each kept vertex loses exactly one class, the dropped singleton, so it lies in m classes. The new missing set is M(x) ∪ {colour of the dropped class}.

Computer check: every H(2) system (n = 8, 12, 16; extra 0–2) and every H(3) system (n = 16, 24; extra 0–2) found reduces to a valid H(m−1) system on n/2. The enumeration blocked repeats of the set sequence only, so not every colouring was tried.

## Observed structure
- In all actual (M = ∅) covers for m = 2, 3, the left ends alternate between end pairs {0,k} and "block-doubled" sets 2S' ∪ (2S'+1).
- Contracting the blocks gives an H(m−1) system. A lemma shows that the end pair entering a block and the end pair leaving it have the same colour, which makes the new M periodic.
- Systems with extra colours can be non-alternating, e.g. all-{0,1,3} for m = 2. These still decimate after reflection.

## What is missing
A proof, for all m, that decimation (or its reflection) always yields an H(m−1) system. This needs a classification of the local set sequences of H(m) systems.
