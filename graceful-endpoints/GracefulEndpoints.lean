import Lean

namespace GracefulEndpoints

def gap (x y : Nat) := (x - y) + (y - x)

def jumpsFrom (prev : Nat) : List Nat → List Nat
  | [] => []
  | x :: xs => gap prev x :: jumpsFrom x xs

def jumps : List Nat → List Nat
  | [] => []
  | x :: xs => jumpsFrom x xs

def realizes (r a b : Nat) (p : List Nat) : Bool :=
  p.head? == some a && p.getLast? == some b &&
  p.length == r && (List.range r).all (fun x => p.contains x) &&
  (List.range (r - 1)).all (fun x => (jumps p).contains (x+1))

def Admissible (r a b : Nat) : Prop :=
  2 ≤ r ∧ a < r ∧ b < r ∧ a ≠ b ∧
  (a + b) % 2 = (r / 2) % 2 ∧ 2 * gap a b ≤ r ∧
  r - 1 ≤ 2 * (a + b) ∧ 2 * (a + b) ≤ 3 * (r - 1)

def FullConjecture : Prop :=
  ∀ r a b, Admissible r a b → ∃ p, realizes r a b p = true

theorem seed_2_0_1 : ∃ p, realizes 2 0 1 p = true :=
  ⟨[0, 1], by rfl⟩

theorem seed_3_0_1 : ∃ p, realizes 3 0 1 p = true :=
  ⟨[0, 2, 1], by rfl⟩

theorem seed_9_3_5 : ∃ p, realizes 9 3 5 p = true :=
  ⟨[3, 4, 2, 6, 1, 7, 0, 8, 5], by rfl⟩

theorem seed_10_3_4 : ∃ p, realizes 10 3 4 p = true :=
  ⟨[3, 6, 5, 9, 0, 8, 1, 7, 2, 4], by rfl⟩

theorem seed_10_3_6 : ∃ p, realizes 10 3 6 p = true :=
  ⟨[3, 4, 9, 0, 8, 1, 7, 5, 2, 6], by rfl⟩

theorem seed_10_4_5 : ∃ p, realizes 10 4 5 p = true :=
  ⟨[4, 6, 3, 2, 7, 1, 8, 0, 9, 5], by rfl⟩

theorem seed_13_4_8 : ∃ p, realizes 13 4 8 p = true :=
  ⟨[4, 7, 6, 12, 0, 11, 1, 10, 2, 9, 5, 3, 8], by rfl⟩

theorem seed_15_5_8 : ∃ p, realizes 15 5 8 p = true :=
  ⟨[5, 7, 6, 9, 14, 0, 13, 1, 12, 2, 11, 3, 10, 4, 8], by rfl⟩

theorem seed_15_6_7 : ∃ p, realizes 15 6 7 p = true :=
  ⟨[6, 5, 8, 4, 10, 3, 11, 2, 12, 1, 13, 0, 14, 9, 7], by rfl⟩

theorem seed_16_5_7 : ∃ p, realizes 16 5 7 p = true :=
  ⟨[5, 10, 8, 4, 11, 3, 12, 2, 13, 1, 14, 0, 15, 9, 6, 7], by rfl⟩

theorem seed_20_6_12 : ∃ p, realizes 20 6 12 p = true :=
  ⟨[6, 10, 7, 13, 8, 9, 11, 19, 0, 18, 1, 17, 2, 16, 3, 15, 4, 14, 5, 12], by rfl⟩

theorem seed_22_7_10 : ∃ p, realizes 22 7 10 p = true :=
  ⟨[7, 14, 9, 13, 21, 0, 20, 1, 19, 2, 18, 3, 17, 4, 16, 5, 15, 6, 12, 11, 8, 10], by rfl⟩

theorem seed_22_7_14 : ∃ p, realizes 22 7 14 p = true :=
  ⟨[7, 10, 11, 9, 15, 5, 16, 4, 17, 3, 18, 2, 19, 1, 20, 0, 21, 12, 8, 13, 6, 14], by rfl⟩

theorem seed_23_7_8 : ∃ p, realizes 23 7 8 p = true :=
  ⟨[7, 14, 6, 16, 5, 17, 4, 18, 3, 19, 2, 20, 1, 21, 0, 22, 13, 11, 10, 15, 9, 12, 8], by rfl⟩

theorem seed_25_8_16 : ∃ p, realizes 25 8 16 p = true :=
  ⟨[8, 12, 11, 13, 10, 17, 6, 18, 5, 19, 4, 20, 3, 21, 2, 22, 1, 23, 0, 24, 14, 9, 15, 7, 16], by rfl⟩

theorem seed_26_8_17 : ∃ p, realizes 26 8 17 p = true :=
  ⟨[8, 15, 9, 14, 25, 0, 24, 1, 23, 2, 22, 3, 21, 4, 20, 5, 19, 6, 18, 10, 13, 11, 12, 16, 7, 17], by rfl⟩

theorem seed_29_11_17 : ∃ p, realizes 29 11 17 p = true :=
  ⟨[11, 15, 10, 16, 13, 14, 12, 19, 8, 20, 7, 21, 6, 22, 5, 23, 4, 24, 3, 25, 2, 26, 1, 27, 0, 28, 18, 9, 17], by rfl⟩

theorem seed_32_10_20 : ∃ p, realizes 32 10 20 p = true :=
  ⟨[10, 19, 13, 16, 12, 17, 15, 14, 22, 8, 23, 7, 24, 6, 25, 5, 26, 4, 27, 3, 28, 2, 29, 1, 30, 0, 31, 18, 11, 21, 9, 20], by rfl⟩

theorem seed_50_16_23 : ∃ p, realizes 50 16 23 p = true :=
  ⟨[16, 32, 49, 0, 48, 1, 47, 2, 46, 3, 45, 4, 44, 5, 43, 6, 42, 7, 41, 8, 40, 9, 39, 10, 38, 11, 37, 12, 36, 13, 35, 14, 34, 15, 33, 18, 30, 17, 31, 20, 28, 19, 29, 22, 26, 21, 27, 24, 25, 23], by rfl⟩

theorem seed_50_19_30 : ∃ p, realizes 50 19 30 p = true :=
  ⟨[19, 29, 17, 28, 20, 27, 21, 26, 22, 25, 23, 24, 33, 18, 31, 49, 0, 48, 1, 47, 2, 46, 3, 45, 4, 44, 5, 43, 6, 42, 7, 41, 8, 40, 9, 39, 10, 38, 11, 37, 12, 36, 13, 35, 14, 34, 15, 32, 16, 30], by rfl⟩

theorem admissible_swap {r a b : Nat} (h : Admissible r a b) :
    Admissible r b a := by
  unfold Admissible gap at *
  omega

theorem admissible_reflect {r a b : Nat} (h : Admissible r a b) :
    Admissible r (r - 1 - a) (r - 1 - b) := by
  unfold Admissible gap at *
  omega

end GracefulEndpoints

namespace GracefulEndpoints

-- Length induction. Its hypothesis is the substantive remaining obligation.
theorem of_descent
    (step : ∀ r a b, Admissible r a b →
      (∀ m, m < r → ∀ x y, Admissible m x y → ∃ p, realizes m x y p = true) →
      ∃ p, realizes r a b p = true) : FullConjecture := by
  intro r
  induction r using Nat.strongRecOn with
  | ind r ih =>
    intro a b hab
    exact step r a b hab ih

-- These identities use signed coordinates so subtraction is exact.
theorem replacement_D_joins (L H m z x y : Int)
    (hx : x = L-H-2) (hz : z=H+1+y) :
    (L-1+z-1+m)-(z+H+x)=m ∧
      (L+m+2*z-2)-(z+H+y)=m+L-1 := by omega

theorem replacement_E_joins (L H m z i j x y e : Int)
    (hx : x=j-H-1) (hz : z=m+j-2*i+H+1+y)
    (he : e=H+1+y ∨ e=H+1+y+j-i-L) :
    (j+z+m)-(z+H+1+x)=m ∧
    ((L+m+e-H-1-y=m+L ∧ z+i-e=m+j-i) ∨
     (L+m+e-H-1-y=m+j-i ∧ z+i-e=m+L)) := by omega

theorem insertion_edge (m j x : Int) (h : m ≤ 3*j)
    : x+j < 2*j ∨ m-1-x < 2*j := by omega

theorem exceptional_edge (j x : Int) (h₁ : 2*j ≤ x+j)
    (h₂ : 2*j ≤ 3*j-x) : x=j := by omega

end GracefulEndpoints
