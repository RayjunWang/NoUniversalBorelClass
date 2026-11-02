We prove Theorem 1 of the supplied research note: for every Polish space $Y$,
$$
\neg\exists F\text{ a Borel equivalence relation on }Y\quad
\forall E\text{ an }F_\sigma\text{ equivalence relation on a Polish space},\quad E\leq_B F.
$$

The proof constructs one fixed Polish nilpotent group and a continuous family of subgroup generators indexed by trees. Membership of one designated element in the generated subgroup is exactly ill-foundedness of the tree. On well-founded trees, the subgroup and its coset equivalence relation have $F_\sigma$ graphs. A category-transfer argument shows that a common Borel upper bound for these coset relations would make ill-foundedness Borel, contradicting a universal analytic diagonal argument.

The tree operator acts on the actual Banach space $A=\ell^1(\mathbb N^{<\mathbb N};\mathbb R)$:
$$
(D_Ta)(s)=a(s)-2\sum_{s^\frown n\in T}a(s^\frown n).
$$
A branch gives a summable kernel vector taking value $1$ at the root. Conversely, a nonzero kernel vector has a nonzero successor at each step and therefore gives a branch. Thus $D_T$ is injective for every well-founded tree.

The central coordinate uses symmetric finite-rank tensors in $\ell^1(S\times S)$. Its image is
$$
C_D=\{(K_{oo},(D\otimes\mathrm{id})K): K\text{ symmetric and of finite rank}\}.
$$
For injective $D$, finite-row reconstruction gives a countable family of closed charts covering this exact image. The proof uses no closed-range or bounded-inverse hypothesis. The explicit central extension and commutator identities identify the algebraically generated subgroup and transfer this closed cover to its coset graph.

For category transfer, a countable binary code records an array of open tests. The associated Borel evaluator chooses dense target points and takes their limit when it exists. Every Borel map agrees with some coded evaluator on a comeager set, because each of its countably many open-ball tests agrees with an open set modulo a meager set. Borel category quantification makes the coded generator-invariance and designated-element-separation tests Borel. Their projection is the complement of the generated-subgroup membership set whenever the required reductions exist. The membership set is analytic by finite generator-word witnesses, so analytic separation makes it Borel.

Applying this to a purported upper bound makes the set of ill-founded trees Borel. The formal development proves its non-Borelness directly using a universal analytic set, completing the contradiction. All spaces carry their native topologies and all generated subgroups are algebraic. The target universe is arbitrary, and empty targets are included.
