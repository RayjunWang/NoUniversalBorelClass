import Solutions.Lemma2
import NoBorelUpperBound.ConstructionFamily
import NoBorelUpperBound.IllFoundedNonBorel

set_option autoImplicit false
noncomputable section
open Set MeasureTheory
universe u

/-- The main theorem using the independently proved category-transfer lemma. -/
theorem solution {Y : Type u} [TopologicalSpace Y] [PolishSpace Y] :
    ¬ ∃ F : Setoid Y,
      NoBorelUpperBoundFSigma.IsBorelRelation F.r ∧
      NoBorelUpperBoundFSigma.IsFSigmaUpperBound F.r := by
  rintro ⟨F,hF,hbound⟩
  letI : MeasurableSpace NoBorelUpperBoundFSigma.Trees.TreeSpace :=
    borel NoBorelUpperBoundFSigma.Trees.TreeSpace
  letI : BorelSpace NoBorelUpperBoundFSigma.Trees.TreeSpace := ⟨rfl⟩
  letI : MeasurableSpace NoBorelUpperBoundFSigma.Construction.G :=
    borel NoBorelUpperBoundFSigma.Construction.G
  letI : BorelSpace NoBorelUpperBoundFSigma.Construction.G := ⟨rfl⟩
  letI : MeasurableSpace NoBorelUpperBoundFSigma.Construction.Axis :=
    borel NoBorelUpperBoundFSigma.Construction.Axis
  letI : BorelSpace NoBorelUpperBoundFSigma.Construction.Axis := ⟨rfl⟩
  have hm := NoBorelUpperBoundFSigma.lemma2_category_transfer
    NoBorelUpperBoundFSigma.Construction.family
    (fun n => (NoBorelUpperBoundFSigma.Construction.continuous_family n).measurable)
    NoBorelUpperBoundFSigma.Construction.continuous_family_fixed
    (fun _ => NoBorelUpperBoundFSigma.Construction.designated) measurable_const F hF
    (by
      intro T hT
      rw [NoBorelUpperBoundFSigma.Construction.generatedSubgroup_family]
      have hT' : ¬ NoBorelUpperBoundFSigma.Trees.HasBranch T := by
        simpa only [NoBorelUpperBoundFSigma.Construction.membershipSet_family,
          NoBorelUpperBoundFSigma.Trees.IF,mem_setOf_eq] using hT
      exact hbound NoBorelUpperBoundFSigma.Construction.G
        (NoBorelUpperBoundFSigma.Construction.cosetSetoid
          (NoBorelUpperBoundFSigma.TreeOperators.operator T))
        (NoBorelUpperBoundFSigma.Construction.isFSigma_cosetGraph _
          (NoBorelUpperBoundFSigma.TreeOperators.operator_injective_of_not_hasBranch T hT')))
  rw [NoBorelUpperBoundFSigma.Construction.membershipSet_family] at hm
  exact NoBorelUpperBoundFSigma.Trees.not_borel_IF hm
