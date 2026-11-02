# No Borel upper bound for the F-sigma equivalence relations

Lean proof of Theorem 1 of the supplied manuscript
`UniversalBorelEquivalence-20261101.tex` (1 November 2026):

> There is no Borel equivalence relation to which every F-sigma
> equivalence relation on every Polish space Borel reduces.

The completed theorem is `NoBorelUpperBoundFSigma.theorem1` in
[`NoBorelUpperBound/Main.lean`](NoBorelUpperBound/Main.lean).
The target relation may have arbitrary Borel complexity. Source spaces
need not be compact or sigma-compact. Borel measurability uses the stated
topologies, and reductions preserve and reflect the relation everywhere.

## Build and audit

The project pins a Prove2Me-supported environment:

- Lean: `leanprover/lean4:v4.30.0`
- Mathlib: `c5ea00351c28e24afc9f0f84379aa41082b1188f`

With [elan](https://github.com/leanprover/elan) and Python 3 installed,
run from this directory:

```sh
lake exe cache get
lake build
python3 scripts/audit.py
```

The audit checks the fixed definitions and dependency pins, scans the
delivered Lean sources for proof holes and proof bypasses, checks the
exact main theorem type without additional assumptions, and asks Lean
for the transitive axiom dependencies of the main proof and key lemmas.
Only `propext`, `Classical.choice`, and `Quot.sound` are allowed.

The standalone upload files are
[`Solutions/Theorem1.lean`](Solutions/Theorem1.lean) and
[`Solutions/CategoryTransfer.lean`](Solutions/CategoryTransfer.lean).
Each includes its complete local proof dependency chain and an exact
`solution` entry point. They can be checked separately:

```sh
lake build Solutions.Theorem1 Solutions.CategoryTransfer Solutions.Lemma2
```

## Proof map

- `BorelEvaluator`, `GenericRepresentation`, and `CategoryTransferFinal`:
  construct jointly Borel codes modulo meager agreement and prove the
  category-transfer lemma.
- `L1Coordinates` and `SymmetricTensor*`: real L1 tensor coordinates,
  finite-rank reconstruction, and closed charts for the F-sigma image.
- `TreeSpace`, `UniversalAnalytic`, and `IllFoundedNonBorel`: the native
  compact tree space and the non-Borelness of ill-founded trees.
- `TreeShift` and `TreeKernels`: the continuous tree operators and the
  exact branch/kernel equivalence.
- `NilpotentGroup`, `NilpotentGenerated`, `Construction`, and
  `ConstructionFamily`: one fixed Polish group, actual algebraically
  generated subgroups, their F-sigma coset graphs off ill-foundedness,
  and exact designated-element membership.
- `Main`: combine those results to prove the main theorem.

See [`docs/semantic-audit.md`](docs/semantic-audit.md) for the statement,
topology, and hypothesis audit. Corollary 4 of the manuscript is outside
this delivered proof and is **not claimed proved** here. The earlier
mission about a universal F-sigma relation is a distinct, weaker result.

## Provenance and status

The source manuscript was read from the user's supplied research project;
its SHA-256 is
`f363482bdebbed853f15c5259afa065842dda314eeb24278bce73d1eaa814cba`.
This repository formalizes that manuscript's Theorem 1; it does not
assert publication, priority, or external peer review of the manuscript.

The main theorem and Lemma 2 have both been accepted by Prove2Me and
marked **Proved**:

- Theorem 1: `56adfcf7-9df7-4730-b48d-1968cd83b344`, accepted submission
  `720c3c82-3e6e-4d04-bcf9-8ba9e7e2d953`.
- Lemma 2: `40920824-81c1-4fcc-8ce2-9028e5727fd5`, accepted submission
  `05ba5476-31cf-4a9b-a570-ecc38e2f2d38`.

The [mission proposal](https://prove2.me/my-missions/007144fb-a3d7-42ca-aa42-82a5990fb254)
is in moderation review at the last inspection. Theorem acceptance is
complete independently of that mission review. Public verification
receipts and exact accepted-file hashes are in
[`docs/platform-verification.json`](docs/platform-verification.json).

The main theorem compiles locally on the pinned environment, and Lean's
axiom report contains only the three standard axioms listed above.
The formalization is distributed under Apache 2.0.
