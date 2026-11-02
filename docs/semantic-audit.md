# Semantic audit of the formalization

This audit compares the proof with Theorem 1 of
`C:/Users/1/Documents/ChatGPT/Reduction/UniversalBorelEquivalence-20261101.tex`.
The source statement is: there is no Borel equivalence relation to which
every F-sigma equivalence relation on a Polish space Borel reduces.
The previous mission about a universal F-sigma relation is a weaker,
different statement. It is not used as the conclusion of this proof.

## Statement and reduction conventions

- `Definitions/Def_NoBorelUpperBound20261101.lean` defines
  `IsFSigmaUpperBound F` by quantifying over **all** small Polish spaces
  `X` and all setoids on `X` with F-sigma graph. There is no compactness,
  sigma-compactness, subgroup, or linearity restriction on this quantifier.
- The target relation has only the hypothesis `IsBorelRelation F.r`.
  It is not required to be F-sigma. The target is a Polish presentation of
  a standard Borel space, as in the usual meaning of a Borel equivalence
  relation.
- `BorelReducible` uses `IsBorelMeasurable`, explicitly the Borel sigma
  algebras of the specified topologies. `IsReduction` is an equivalence
  for every pair of points; it both preserves and reflects the relation.
- `GroupCosetRelation H g g'` is exactly `g⁻¹ * g' ∈ H`.
  `Construction.cosetSetoid` proves all three equivalence-relation laws.
  The construction does not assume that `H` is normal.
- An empty target is not excluded by an extra theorem hypothesis:
  `nonempty_of_isFSigmaUpperBound` obtains nonemptiness from the reduction
  of the one-point relation.

## Native topologies and measurable structures

- `L1Coordinates.L1 I` is Mathlib's actual real `lp` with exponent one.
  `MatrixL1 I J` is the same space on `I × J`. Their norm topologies are
  inherited without replacement. Separability for countable index types
  is proved from the dense span of coordinate vectors in
  `L1Separable.lean`; completeness is Mathlib's completeness of `lp`.
- `CentralExtension beta` is a new type with underlying set
  `X × X × C`. Its topology is explicitly the native product topology.
  Its group operation and inverse are proved continuous in that topology.
  `Construction.G` is fixed independently of the tree parameter.
- `Trees.TreeSpace` is the closed subtype of `(List ℕ → Bool)` satisfying
  downward closure. It has the product topology on membership bits, and
  its Polish and compact instances come from that closed subtype.
  Empty trees are allowed. `HasBranch` asks for one infinite sequence
  whose every finite prefix is in the tree.
- `Construction.Axis` is the additive-to-multiplicative type synonym for
  the same real L1 space. Its topology is the inherited L1 topology.
  No discrete, indiscrete, or unrelated Polish topology is installed.
- The measurable-space instances introduced in `Main.lean` are `borel`
  of these existing topologies; each local `BorelSpace` instance is
  witnessed by `rfl`. This changes no topology and does not weaken
  Borel measurability.

## Exact tree, tensor, and subgroup construction

- `TreeShift.lean` constructs the actual bounded child-sum shift with
  operator norm at most one, and `operator T = id - 2 • shiftCLM T`.
  Joint continuity in the tree and the L1 vector is proved, rather than
  continuity in an operator-norm topology that the source does not use.
- `TreeKernels.hasBranch_iff_exists_kernel_root` is the exact biconditional
  `HasBranch T ↔ ∃ a, operator T a = 0 ∧ a [] = 1`. A branch supplies the
  summable geometric vector. Conversely, a nonzero kernel coordinate
  supplies successive nonzero children. Thus well-foundedness implies
  injectivity of this same operator.
- `SymmetricTensor.symmetricSpan` is an **algebraic** real span of
  symmetrized elementary tensors. It is not a closed span or a space of
  arbitrary compact/nuclear operators. `imageSubmodule D []` is its
  actual linear image under `K ↦ (K([],[]), mapLeft D K)`.
- `SymmetricTensor.isFSigma_imageSubmodule` requires only countability
  of the coordinate type and injectivity of `D`. Its closed charts and
  their coverage are both proved. The apparent coverage premise in the
  intermediate helper `isFSigma_image_of_chart_coverage` is discharged
  by `exists_imageChart_of_mem`; it is not an assumption of the final
  F-sigma theorem. No closed-range hypothesis on `D` is introduced.
- `Construction.beta_apply` is the source bilinear expression
  `(a[] * b[], (outer u b + outer v a)/2)`. Graph axes use `(a,D a)`.
  `centralSpan_eq_imageSubmodule` proves that the commutator-generated
  central span equals the tensor image above.
- `CentralExtension.generatedAxes` and `GeneratedSubgroup` use Mathlib's
  **algebraic subgroup closure**. No topological closure is taken.
  `generatedAxes_eq_coordinateSubgroup` proves the full coordinate
  description, with both inclusions. In particular, scalar closure of
  the central span is justified by rescaling the real axis parameter,
  not by assuming a subgroup is a real vector subspace.
- `designated_mem_iff` and `designated_mem_tree_iff` give exact membership
  of `z = (0,0,(1,0))`, including reflection. The converse extracts a
  column of the witnessing tensor. This is actual subgroup membership,
  not membership in its topological closure or a surrogate predicate.
- F-sigma subgroup and coset-graph conclusions are used only off
  `HasBranch`, where the proved kernel lemma supplies injectivity.
  There is no injectivity hypothesis on arbitrary trees or on the
  final main theorem.

## Generic Borel codes and category transfer

- `BorelCodes.Code G` is a countable product of discrete Booleans, coding
  arrays of open sets through a fixed countable basis. Its explicit
  topology is exactly this product topology. Its measurable space is
  its Borel sigma algebra.
- `BorelEvaluator.eval` selects a countable sequence of dense points
  using the coded open tests and takes `limUnder`. The evaluator is
  jointly Borel on the entire code-by-source product, including codes
  for which that sequence does not converge.
- `GenericRepresentation` proves agreement with every Borel map on a
  residual set, by replacing each inverse image of an open ball by an
  open set modulo a meager set. It does not claim that all Borel maps
  have one bounded Borel rank or that codes represent them everywhere.
- The temporary `upgradeIsCompletelyMetrizable Y` in that proof chooses
  a compatible complete metric. Mathlib constructs this metric using
  `replaceTopology`, so its induced topology is the previously supplied
  topology. `denseSeq`, `limUnder`, the evaluator, and Borel structures
  therefore continue to concern the original target topology.
- `GenericWitness` tests invariance generically on `G × Axis`, then
  separation generically on `G`. The transfer proof derives collapse
  for **every fixed** homomorphism image element before taking the
  algebraic subgroup they generate. It does not assume a generic set
  contains any preassigned axis parameter.
- Agreement sets are transported through continuous open group shears.
  `CategoryProduct` proves the residual-section argument, and
  `CategoryQuantifier` proves Borelness of category quantification of
  Borel sections. These are proved infrastructure, not main-theorem
  assumptions.
- Membership is analytic through finite words in the generators.
  The generic witness projection is the complement of membership when
  reductions exist there. Analytic separation then makes membership
  Borel, contradicting the exact membership set `Trees.IF`.
- `IllFoundedNonBorel.not_borel_IF` proves non-Borelness in the native
  membership-bit topology through a universal analytic diagonal and a
  continuous reduction to these same downward-closed trees.

## Completion boundary and kernel audit

The final `NoBorelUpperBoundFSigma.theorem1` is compiled on Lean 4.30.0
and Mathlib `c5ea00351c28e24afc9f0f84379aa41082b1188f`. The generic
coding premises are discharged in `CategoryTransferFinal.category_transfer`
using `BorelCodes.eval` and `GenericRepresentation`. `Main.lean` then
proves the requested unconditional nonexistence theorem. It retains only
the target topology and Polish-space assumptions; its existential target
setoid has the exact Borel-graph and universal-upper-bound properties.

The transitive `#print axioms` report for the final main theorem contains
only the standard Lean axioms `propext`, `Classical.choice`, and
`Quot.sound`. `scripts/audit_axioms.lean` also checks the exact main
statement as an `example`, so extra proof premises cannot silently pass
the audit. `scripts/audit.py` reproduces these checks. A source scan found no `sorry`,
`axiom`, `admit`, `native_decide`, `unsafe`, or `implemented_by` proof
bypass in the project proof modules. Platform acceptance is a separate
check and is not asserted by this audit. The accepted platform submissions
and their exact proof-file hashes are recorded separately in
`docs/platform-verification.json`.
