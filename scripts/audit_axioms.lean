import NoBorelUpperBound

set_option autoImplicit false
universe u

/-- This checks that the exported theorem needs no extra mathematical premise. -/
example {Y : Type u} [TopologicalSpace Y] [PolishSpace Y] :
    ¬ ∃ F : Setoid Y,
      NoBorelUpperBoundFSigma.IsBorelRelation F.r ∧
      NoBorelUpperBoundFSigma.IsFSigmaUpperBound F.r :=
  NoBorelUpperBoundFSigma.theorem1

#print axioms NoBorelUpperBoundFSigma.theorem1
#print axioms NoBorelUpperBoundFSigma.not_isFSigmaUpperBound
#print axioms NoBorelUpperBoundFSigma.category_transfer
#print axioms NoBorelUpperBoundFSigma.Trees.not_borel_IF
#print axioms NoBorelUpperBoundFSigma.Construction.membershipSet_family
#print axioms NoBorelUpperBoundFSigma.SymmetricTensor.isFSigma_imageSubmodule
#print axioms NoBorelUpperBoundFSigma.TreeOperators.hasBranch_iff_exists_kernel_root
#print axioms NoBorelUpperBoundFSigma.CentralExtension.generatedAxes_eq_coordinateSubgroup
