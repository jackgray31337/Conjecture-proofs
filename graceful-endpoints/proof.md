# A computer-assisted proof of Gvozdjak's graceful-path endpoint conjecture

Research draft, 27 November 2026. The coverage lemma below is certified by exact integer-set arithmetic using libisl. The accompanying programs construct individual witnesses and check the coverage of the infinite domain. Independent review of the argument and priority is pending.

## Statement and representation

Write G(r,a,b) for existence of a permutation of 0 through r−1 with endpoints a,b and absolute differences 1 through r−1 each once. Write Adm(r,a,b) for r≥2, distinct labels in the interval, and

    a−b ≡ floor(r/2) (mod 2)
    2|a−b| ≤ r
    r−1 ≤ 2(a+b) ≤ 3(r−1).

We prove that Adm implies G. Necessity is Gvozdjak's Theorem 5.1.5. Reversal exchanges the endpoints. Simultaneously complementing the labels exchanges x with r−1−x. Thus it suffices to treat a<b and a+b≤r−1. Every smaller call in the proof requires Adm; a singleton need never be a seed.

A bipartite graceful path alternates between [0,H] and [H+1,L−1]. Call these its low and high labels. At any join assume the indicated orientation, reversing the inserted path when the marked edge occurs in the opposite direction. Every interval in this note has integer endpoints and includes them.

## A. Even prefix and the bipartite building blocks

Let E(c,u) be a bipartite path of length 2c, threshold c−1, from u to c+u, for 0≤u<c. Kotzig's result gives these paths. Here is an explicit construction as well.

Given E(c,u) and any length-m graceful path from u to v, add m to the high labels of E and concatenate the inner path translated up by c. The label intervals are [0,c−1], [c,c+m−1], [c+m,2c+m−1]. The internal jumps are respectively m+1 through m+2c−1 for the outside block, and 1 through m−1 for the inner block. The join has jump m, between c+u+m and c+u. The endpoints are u,v+c. Call this operation prefixing. If both inputs alternate across their respective halves, with the second starting in its low part, the combined path also alternates across the combined threshold.

For E(h,u), reversal followed by complementation reduces to 2u≤h−1. At u=0 use Walecki, whose entries at positions 2i and 2i+1 are i and L−1−i, whenever those positions exist. Its jumps descend by one. For h=2u+1, cut Walecki of length 2h at its jump h, join the old endpoints 0 and h, and orient the result from u to u+h. The removed edge was (u,u+h), and the new edge has the same jump. In all other positive cases prefix E(floor(h/2),u) to E(ceil(h/2),u). The two smaller parameters exceed u and the result alternates with endpoints u,u+h.

For the odd bipartite path of length 2h+1 with lower majority and distinct endpoints u,h−u, reverse to take u<h/2. Use Walecki if u=0. Otherwise prefix E(h−u,u) to the reversed length-(2u+1) Walecki path from u to 0. The upper-majority variant is its complement. Consequently the following are available, with U<V:

| Length L | Threshold H | Ordered endpoints |
|---|---|---|
| 2h+1 | h | U+V=h, V≤h |
| 2h | h−1 | V=U+h, U<h |
| 2h+1 | h−1 | U+V=3h, U≥h |

## Where the previous reduction stops

For an orientation (u,v) in the four-element symmetry orbit, the even prefix A reduces to G(r−2c,u,v−c). After cancellation of inherited conditions, the necessary and sufficient tests for this specific move on an admissible target are

    c>u,   c≠v−u,   2c≤r−1−u,   c≤min(v,r−1−v),
    4c≤r−2u+2v,     4c≤3(r−1)−2(u+v).

The second old move B uses m=r−4j, inner endpoints a−2j,b−2j and a bipartite block of length 4j. For the endpoint-independent insertion guarantee its exact conditions are

    j≥1,   5j<r≤7j,   2j≤min(a,b,r−1−a,r−1−b),
    4j≤min(r−2|a−b|, 2(a+b)−r+1, 3(r−1)−2(a+b)).

Indeed the inner jump j occurs on some x<y=x+j. If y≥2j and m−1−x≥2j then m−1≥3j, so the indicated range guarantees y<2j after a possible complement. Shift the old path by 2j. At the marked edge insert E(2j,y), with its high labels raised by m. Its ends are y and y+2j+m. Its joins to x+2j and y+2j give j and m. Its internal jumps give [m+1,r−1]. The surviving old jumps give [1,m−1] except j. Low, old, and high vertices fill the three consecutive intervals of lengths 2j,m,2j. Reflection is undone after insertion. This also works for smaller j whenever the location of its edge is known to permit insertion. This distinction will matter on the exceptional progression.

Precisely the pairs failing B and failing A in all four orientations escape the two old arithmetic reductions. For example, when r=4k and (a,b)=(k+1,k+3), k≥4, the low-first orientations in A force c≤k+1 or c≤k−1 by the distance condition, while c must exceed the first endpoint. The other orientations start too high (at k=4, direct substitution gives the same conclusion). B forces j≤2 and 7j≥4k. For r=4k+1 and (a,b)=(k,3k), k≥1, A forces c≤k by the upper sum bound in the only feasible orientation. B cannot shorten a path with this maximal endpoint difference. The latter family already follows by cutting the Walecki path at the edge (k,3k), joining its old endpoints 0,2k and orienting. This is the translation operation of Ollis and Willmott. The first family and its reflected images eventually have neither endpoint in the published fixed-label range 0 through 6.

## C. Odd prefix

Choose c≥u with c≠2u, and put m=r−2c−1. Use an odd lower-majority path from u to c−u. Raise its high labels by m. Append a length-m path from m−1−u to v−c−1, translated by c+1. Equivalently the inner ordered pair after complementing is (u,r−1−c−v). The join has jump m since the first appended label is m+c−u and the last prefix label is c−u. Internal jumps are [m+1,r−1] and [1,m−1]. The prefix uses [0,c] and [c+m+1,r−1], the inner path the intervening interval. The output ends are u,v.

## Marked edges of the bipartite base path

In any of the three rows above, each of the following conditions guarantees that some such path with the given endpoints uses the specified edge i≤H<j. Only one edge is prescribed at a time.

1. i=0, j=L−1. This is the unique possible largest jump.
2. i=H, j=H+1. This is the unique possible unit jump across the threshold.
3. U=0 and i+j=L, or V=L−1 and i+j=L−2. Take Walecki or its complement and reverse as necessary. The conditions on the two labels put the edge in the appropriate alternating list.
4. i+j=L−1 and min(U,L−1−V)<i. Here is the extra flexibility required by the proof.

For 4, normalize the low-majority odd case by reversal, and get the high-majority case by complement. In the even case also allow reverse-complement. Each antidiagonal edge is fixed as an unordered pair by complement. The distinguished lower endpoint after normalization is u=min(U,L−1−V), with u<h/2 in odd length, u≤(h−1)/2 in even length. For u=0 Walecki contains every crossing antidiagonal edge.

In odd length first suppose u<i≤h−u. Use an even prefix of half-length c=i, followed by an odd inner path of length 2(h−c)+1 from u to h−c−u. The largest inner edge translates to (i,L−1−i). If c=h−2u the two inner ends coincide. In that case take c=i+1≤h−u; the prefix unit edge now stretches from c−1 to L−c, giving exactly the requested edge. For i>h−u take c=h−u and the reversed Walecki inner path. Its antidiagonal edges supply all the remaining indices.

In even length, for u<i≤h−u−1 take c=i and use E(h−c,u) for the inner path. For larger i, take c=h−u−1 and use the reverse-complement of Walecki on 2(u+1) as the inner path; it starts at u and contains every crossing antidiagonal there. The latter prefix needs c>u. In the exceptional case h=2u+1 the cut Walecki construction for E(h,u) removed just the antidiagonal edge indexed u. All the required indices are strictly greater. This proves 4.

## Two edge replacements

Both replacements take a carrier from the table and a shorter length-m graceful path from x to y. Here is the explicit bookkeeping.

**D. Replace the edge L−1 to 0.** Require x=L−H−2 and z=H+1+y≥1. Set r=L+m+2z−1. Map a carrier label t to

    f(t)=t+z−1 + m·[t>H].

In the direction from f(L−1) to f(0), traverse the inner path shifted by z+H, then the list

    r−1, 0, r−2, 1, …, r−z, z−1.

The last entry is f(0) itself and is written only once. The unused middle interval is exactly [z+H,z+H+m−1]. The alternating list uses the lowest and highest z labels, overlapping the mapped carrier only at f(0). The retained carrier jumps are [m+1,m+L−2]. The inner jumps are [1,m−1]. The two joins give m and m+L−1, since f(L−1)−(z+H+x)=m and (r−1)−(z+H+y)=m+L−1. The alternating list contributes [m+L,r−1]. Endpoints are f(U),f(V), including when the cut is at a path end.

**E. Replace a marked edge i to j.** Write d=j−i and require

    x=j−H−1,     z=m+j−2i+H+1+y ≥ 1,     r=L+m+2z.

At least one of e=H+1+y and e=H+1+y+d−L must belong to [0,z−1]. Map a carrier label t to

    f(t)=t+z + m·[t>H].

From f(j) toward f(i), insert the inner path shifted by z+H+1, then the reverse of E(z,e) with its high labels increased by L+m. This outer block starts at r−z+e and ends at e. The labels, in increasing order by interval, belong to outer low, carrier low, inner, carrier high, outer high. Their respective sizes are z,H+1,m,L−H−1,z, so there are no repetitions or gaps.

The retained carrier jumps are [m+1,m+L−1] except m+d. The inner jumps are [1,m−1], the stretched outer jumps [L+m+1,r−1]. The first join is m. The remaining joins equal

    L+m+e−H−1−y,      z+i−e.

Their ordered values are (m+L,m+d) for the first choice of e and (m+d,m+L) for the second. This accounts for all jumps, including d=1 and d=L−1. The endpoints are f(U),f(V).

In all five moves the stated inner pair passes the original parity test. Since all the output jumps have been exhibited, the parity of the constructed endpoint difference also follows by summing the jumps modulo 2.

## A progression on which the position of one jump matters

For k≥2 take (r,a,b)=(28k+22,9k+7,13k+10). Set j=4k+3 and m=r−4j=3j+1. The target inner endpoints in B are u=k+1 and 5k+4. B can fail here only if the jump-j edge is (j,2j): the lower endpoint must be at least j and the upper endpoint at most 2j if both orientations fail.

Put c=j+2, q=u+2. On 2c labels construct a bipartite path from u to u+c that omits the edge (c−2,c+1). Begin with the length-six path (1,5,0,3,2,4). Its jumps are 4,5,3,1,2 and it omits (1,4). Prefix E(q−3,1) to it; reverse-complement the result, then prefix E(c−q,u). The parameters are valid because q−3=k>1 and c−q=3k+2>u. The first prefix gives ends 1,q+1; reverse-complement gives ends q−2=u and q+u. In an even path of half-length t the unordered pair (t−2,t+1) is fixed by complement and reversal cannot create it. Each prefix translates the two central labels into the corresponding two central labels of the enlarged path; both lie in the inner label interval and no edge between them can be introduced by a join. Thus the final block omits the promised pair.

By strong induction choose a path on 4k labels from k+1 to k−1. Its difference is 2, sum 2k, and floor(4k/2) is even, so it is admissible for k≥2. Prefix the just-constructed length-2c block to this path. The resulting length is m, and the ends are u and k−1+c=5k+4. The putative edge (j,2j) would have to connect the outer low and outer high intervals. Undoing the stretch by 4k makes it (c−2,c+1), which is absent. Hence B works in one orientation and supplies the required length-r permutation. This argument descends directly to length 4k.

## Computational coverage lemma and conclusion

Let R be the full integer set of normalized admissible triples, with r≥2 and no upper bound. For each formula in coverage.py, variables besides (r,a,b) are integer witnesses. The script projects them out, subtracts the resulting image from R, and coalesces the remaining set. The four orientations used by A and C are (a,b), (r−1−b,r−1−a), (b,a), (r−1−a,r−1−b). B is invariant under the two symmetries. D and E only need the two sorted orientations. Their rows impose the carrier table, the exact shifted endpoint equations, the appropriate join conditions, and Adm(m,x,y). E runs each of the four marked-edge alternatives separately. Finally the script subtracts the certified progression. These are ordinary projections and differences of Presburger-definable integer sets. Disjunctions, floors and parity use integer semantics.

The program checks equality in both directions between the remaining set and the keys of seeds.json, and separately checks the endpoints, length, labels and jumps of the supplied witnesses. The exact residual, grouped by r, is

| r | (a,b) |
|---|---|
| 2 | (0,1) |
| 3 | (0,1) |
| 9 | (3,5) |
| 10 | (3,4), (3,6), (4,5) |
| 13 | (4,8) |
| 15 | (5,8), (6,7) |
| 16 | (5,7) |
| 20 | (6,12) |
| 22 | (7,10), (7,14) |
| 23 | (7,8) |
| 25 | (8,16) |
| 26 | (8,17) |
| 29 | (11,17) |
| 32 | (10,20) |
| 50 | (16,23), (19,30) |

All recursive calls of A through E have strictly smaller length. The special progression goes to 4k. Bipartite carriers are independently constructed as above. Thus a least-length counterexample could be neither a seed nor in any subtracted region, contradicting the coverage lemma.

## Reproduction and prior work

In the extracted directory run the commands below with Python 3 and the integer set library libisl available as a shared library. The second command constructs a member of the exceptional progression. The proof uses the certificate even if no individual example is requested.

    python3 coverage.py
    python3 construct.py 218 70 101

The coverage calculation relies on libisl's exact set operations. The witness constructor independently checks each completed path by sorting the labels and jumps. A proof assistant has not checked the correspondence between program predicates and the constructions in this note.

- P. Gvozdjak, *On the Oberwolfach problem for cycles with multiple lengths*, Conjecture 5.1.1 and Theorem 5.1.5. https://citeseerx.ist.psu.edu/document?doi=6b03aea8634ec12dc9c1be1307310aee045e414c&repid=rep1&type=pdf
- Z. Zhang, Q. Zhang and C. Wang, *On (a,b;n)-graceful labeling of path P_n*, Ars Combinatoria 132 (2017), 105–119. Their n counts edges, so n=r−1 here. https://combinatorialpress.com/article/ars/Volume%20132/volume-132-paper-9.pdf
- M. A. Ollis, *Sequences in dihedral groups with distinct partial products*, Australas. J. Combin. 78 (2020), 35–60. The bipartite ingredient is Lemma 5.5, the insertion is Theorem 5.6 and its automatic range is Lemma 5.8. https://ajc.maths.uq.edu.au/pdf/78/ajc_v78_p035.pdf
- J. Hicks, M. A. Ollis and J. Schmitt, *Distinct partial sums in cyclic groups*, proof of Lemma 4.5, for the even-prefix construction in reverse orientation. https://arxiv.org/abs/1809.02684
- M. A. Ollis and D. T. Willmott, *Twizzler, zigzag and graceful terraces*, for translation at an edge with jump equal to the endpoint difference. https://ajc.maths.uq.edu.au/pdf/51/ajc_v51_p243.pdf
- J. A. Gallian, *A Dynamic Survey of Graph Labeling*, 2026 version, §2, summarizes the fixed-endpoint results of Zhang, Zhang and Wang. https://www.combinatorics.org/files/Surveys/ds6/ds6v29-2026.pdf
