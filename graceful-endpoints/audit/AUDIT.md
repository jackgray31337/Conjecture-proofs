# Verification of the graceful-path endpoint proof

The attachment reviewed had SHA-256
`029275f9676e75557e99f1de5fbcc6d8e5cc34c2751d3f242b67fa34457c2911`.
The four original files are included alongside two additional checks. The proof covers the unrestricted admissible endpoints of Gvozdjak's Conjecture 5.1.1. I found no mathematical gap in the induction. Publication priority was outside this verification.

## Reproduction

In the extracted folder run the following with Python 3 and the shared library libisl available. The verification used Python 3.12.14 and isl-0.27-GMP. Run without Python's optimisation flag, since the two additional scripts use assertions.

```sh
python3 coverage.py
python3 forward_check.py
python3 independent_tests.py
```

The first two scripts both give 20 residual triples. The first projects witnesses out of predicates for target triples. The second starts from admissible shorter paths, maps construction parameters to their output triples, and removes these images and their permitted symmetries from the target set. It specifies endpoint parity by the four residue classes of the length and expresses the two splice operations through the actual joins. It uses the same exact integer-set library, and checks equality of the final residual with the supplied seed keys in both directions. Neither script bounds the target length.

The third script verifies the 20 seed paths, 36,852 marked carrier instances of lengths 2 through 80, every one of the 11,050 admissible ordered triples of lengths 2 through 50, and the exceptional-progression construction directly at k = 2 through 19, 37 and 83. It validates permutations returned by the supplied constructors, including the marked edge and alternation where required.

## Mathematical checks

* Subtracting one from Gvozdjak's original labels leaves endpoint differences unchanged and decreases their sum by two. This gives precisely the admissibility inequalities in the archive. Reversal sorts the endpoints, and complement followed by reversal if necessary gives a sum at most r−1.
* In the even and odd prefixes the jump sets of the outer and inner paths are the disjoint intervals above and below m. The join supplies m. Insertion B replaces the old jump j, then reintroduces it at one join and supplies m at the other. If both orientations of its marked edge fail, its smaller label is at least j and at most m−1−2j. This is impossible when m≤3j.
* For each bipartite carrier a maximum jump and the unit jump are forced. The other two edge guarantees follow from the Walecki edge sums and the two prefix constructions in the draft. In the odd diagonal construction, when the choice c=i would force equal inner endpoints, c=i+1 is allowed because u≥1 and i=h−2u. Its stretched unit edge is (i,L−1−i). In the exceptional even case h=2u+1 the only deleted diagonal edge has index u, below every required index.
* In D the two joins give m and m+L−1. The alternating outer list overlaps the mapped carrier exactly at its final vertex. In E the inner path supplies 1 through m−1. The retained carrier edges supply m+1 through m+L−1 with m+d missing, and the outer block supplies L+m+1 through r−1. The three joins give m, m+d and m+L. All block label intervals are disjoint in E.
* For r=28k+22 the shorter B instance has m=3j+1, leaving exactly one obstructing edge (j,2j). In the protected length-2c block it would have to arise from (c−2,c+1). The length-six starting path omits that edge relative to its own centre. Each prefix preserves the omission because both prescribed vertices belong to the translated inner interval, and reverse-complement fixes the unordered pair. The only conjectural instance used to construct this block and its continuation has length 4k<r, with admissible endpoints k+1 and k−1.
* Every reduction strictly shortens the required instance. A least-length counterexample would therefore have to occur among the 20 residual triples, each of which has a verified explicit path.

The audit verifies a computer-assisted mathematical argument. It relies on libisl for unbounded set arithmetic and on mathematical review for the interpretation of its formulas. It is not a proof-assistant formalisation or an external specialist review.

Original statement: https://citeseerx.ist.psu.edu/document?doi=6b03aea8634ec12dc9c1be1307310aee045e414c&repid=rep1&type=pdf

Integer-set arithmetic: https://libisl.sourceforge.io/user.html
