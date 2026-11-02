import NoBorelUpperBound.CategoryTransferFinal

set_option autoImplicit false
open MeasureTheory
universe u v w z

/-- The exact published category-transfer mission statement. -/
theorem NoBorelUpperBoundFSigma.lemma2_category_transfer
    {P : Type u} [MeasurableSpace P] [StandardBorelSpace P]
    {G : Type v} [Group G] [TopologicalSpace G] [IsTopologicalGroup G] [PolishSpace G]
    {A : ℕ → Type w} [∀ n, Group (A n)] [∀ n, TopologicalSpace (A n)]
    [∀ n, IsTopologicalGroup (A n)] [∀ n, PolishSpace (A n)]
    {Y : Type z} [TopologicalSpace Y] [PolishSpace Y]
    (h : ∀ n, P → (A n →* G))
    (h_joint : ∀ n, @Measurable (P × A n) G
      ((inferInstance : MeasurableSpace P).prod (borel (A n))) (borel G)
      (fun pa => h n pa.1 pa.2))
    (h_cont : ∀ n p, Continuous (h n p))
    (z0 : P → G) (hz : @Measurable P G inferInstance (borel G) z0)
    (F : Setoid Y) (hF : NoBorelUpperBoundFSigma.IsBorelRelation F.r)
    (h_bound : ∀ p, p ∉ NoBorelUpperBoundFSigma.MembershipSet h z0 →
      NoBorelUpperBoundFSigma.BorelReducible
        (NoBorelUpperBoundFSigma.GroupCosetRelation
          (NoBorelUpperBoundFSigma.GeneratedSubgroup h p)) F.r) :
    MeasurableSet (NoBorelUpperBoundFSigma.MembershipSet h z0) := by
  letI : MeasurableSpace G := borel G
  letI : BorelSpace G := ⟨rfl⟩
  letI : ∀ n, MeasurableSpace (A n) := fun n => borel (A n)
  letI : ∀ n, BorelSpace (A n) := fun _ => ⟨rfl⟩
  exact NoBorelUpperBoundFSigma.category_transfer h h_joint h_cont z0 hz F hF h_bound
