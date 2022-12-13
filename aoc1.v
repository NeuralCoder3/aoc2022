Require Import List Lia.
Require Import ExtLib.Data.Monads.OptionMonad.

Require Import ExtLib.Structures.Monads.
Import MonadNotation.
Local Open Scope monad_scope.

(*
We skip parsing as this would realistically done externally 
and is of no further theoretical interest.

We also only use the most basic standard library functions
and interpret the exercise literally (without implicit optimization).

Furthermore, we refrain from advanced automation to keep the proof readable.

There is surely a shorter, more elegant solution even with spelling out every detail.
*)

Definition sum xs := fold_left plus xs 0.
Definition calories elf := sum elf.

Definition arg_max {A} (f: A -> nat) (l: list A) : option A :=
  fold_right (fun b ao => 
    match ao with 
    | None => Some b
    | Some a => ret (if Nat.leb (f a) (f b) then b else a)
    end
  ) None l.

(* non-unique *)
(* Lemma arg_left_char {A} f (xs:list A) a:
  arg_left f l = Some a <-> In a l /\ forall b, In b l -> f a >= f b. *)

Ltac leb_to_le H :=
    first [apply PeanoNat.Nat.leb_le in H|apply PeanoNat.Nat.leb_gt in H].

Lemma non_empty_arg_max {A} (f: A -> nat) (l: list A):
  l <> nil -> 
  {a | arg_max f l = Some a /\ In a l /\ forall b, In b l -> f a >= f b}.
Proof.
  intros.
  induction l;simpl.
  - now contradict H.
  - destruct l.
    + exists a. simpl. intuition. subst. lia.
    + destruct IHl as [b (->&H2&H3)];[easy|].
    (* Search Nat.leb. *)
      destruct Nat.leb eqn: Hleb;
        leb_to_le Hleb;
        simpl; eexists; repeat split;try tauto.
      all:intros ? [<-|?%H3];lia.
Qed.

(*
faster computation
*)


Lemma arg_max_comm {A} (f:A->nat) xs:
    option_map f (arg_max f xs) = arg_max (fun x => x) (map f xs).
Proof.
  induction xs;simpl.
  - reflexivity.
  - rewrite <- IHxs.
    destruct arg_max;simpl.
    + now destruct Nat.leb.
    + reflexivity.
Qed.

Definition arg_left {A} (f: A -> nat) (l: list A) : option A :=
  fold_left (fun ao b => 
    match ao with 
    | None => Some b
    | Some a => ret (if Nat.leb (f a) (f b) then b else a)
    end
  ) l None.

Lemma leb_max a b:
  (if Nat.leb a b then b else a) = Nat.max a b.
Proof.
  destruct Nat.leb eqn: H;leb_to_le H;lia.
Qed.

Definition arg_max_one {A} f (a b:A) :=
  if Nat.leb (f a) (f b) then b else a.

Lemma fold_arg_max_one {A} f (a b:A):
  (if Nat.leb (f a) (f b) then b else a) = arg_max_one f a b.
Proof.
  reflexivity.
Qed.

Lemma arg_max_one_comm {A} f (a b:A):
  f(arg_max_one f a b) = f(arg_max_one f b a).
Proof.
  unfold arg_max_one.
  destruct Nat.leb eqn: H;leb_to_le H;
  destruct Nat.leb eqn: H2;leb_to_le H2;firstorder;
  lia.
Qed.

Lemma arg_max_one_assoc {A} f (a b c:A):
  arg_max_one f a (arg_max_one f b c) = arg_max_one f (arg_max_one f a b) c.
Proof.
  unfold arg_max_one.
  repeat (
    let H := fresh in
    destruct Nat.leb eqn: H;leb_to_le H
  );firstorder;lia.
Qed.

Lemma if_apply {A B} (f: A -> B) (c:bool) a b:
  f(if c then a else b) = if c then f a else f b.
Proof.
  destruct c;reflexivity.
Qed.

Lemma arg_alt {A} f (xs:list A):
  option_map f (arg_left f xs) = option_map f (arg_max f xs).
Proof.
  unfold arg_left, arg_max.
  match goal with
  | |- context [fold_left ?f _ _] => 
    remember f as g1
  end.
  match goal with
  | |- context [fold_right ?f _ _] => 
    remember f as g2
  end.
  assert(forall b ao, g1 ao b = g2 b ao) as Hg by (intros;now subst).
  generalize (@None A) as x.
  induction xs;intros;simpl.
  - reflexivity.
  - rewrite IHxs, Hg.
    clear g1 Heqg1 IHxs Hg.
    (* g2 is commutative under f *)
    induction xs;simpl.
    + reflexivity.
    + destruct (fold_right g2 (g2 a x) xs) eqn: H;simpl in IHxs;
      destruct (fold_right g2 x xs) eqn: H2;simpl in IHxs;
        subst;cbn in *;try congruence.
      * injection IHxs as H3.
        repeat rewrite fold_arg_max_one in *.
        now unfold arg_max_one at 2;
        rewrite if_apply, (arg_max_one_comm f a2 a0), <- if_apply, fold_arg_max_one, <- arg_max_one_assoc;
        unfold arg_max_one at 2;
        rewrite if_apply, <- H3, <- if_apply, fold_arg_max_one, arg_max_one_comm.
      * injection IHxs as H3.
        repeat rewrite fold_arg_max_one in *.
        now rewrite arg_max_one_comm;unfold arg_max_one;do 2 rewrite (if_apply f);rewrite H3.
Qed.

Definition id {A} (a:A) := a.
Lemma option_map_id {A} (a:option A):
  option_map id a = a.
Proof.
  now destruct a.
Qed.

Corollary arg_alt_id (xs:list nat):
  arg_left id xs = arg_max id xs.
Proof.
  rewrite <- option_map_id at 1.
  rewrite arg_alt, option_map_id.
  reflexivity.
Qed.

Lemma arg_left_id (xs:list nat):
  xs <> nil ->
  arg_left (fun x => x) xs = Some (fold_left max xs 0).
Proof.
  intros H.
  rewrite arg_alt_id, fold_symmetric.
  2,3: lia.
  induction xs;simpl.
  - now contradict H.
  - destruct xs.
    + now rewrite PeanoNat.Nat.max_0_r.
    + now rewrite IHxs;[|easy];rewrite leb_max, PeanoNat.Nat.max_comm.
Qed.

(*
we want to find the sum of the calories of the elf that caries the most calories.
max (sum (map calories elf))
*)

Definition solution elves := fold_left max (map calories elves) 0.

(* if we trust arg_max *)
Lemma most_calories_carried_arg_max (elves: list (list nat)):
  elves <> nil ->
  {n:nat & {max_elf & 
    n = calories max_elf /\
    arg_max calories elves = Some max_elf 
  }}.
Proof.
  intros.
  destruct (non_empty_arg_max calories elves) as [max_elf (->&H2&H3)];[easy|].
  exists (calories max_elf), max_elf.
  split;reflexivity.
Qed.

(* if we want the property explicitely *)
Lemma most_calories_carried (elves: list (list nat)):
  elves <> nil ->
  {n:nat | 
  solution elves = n /\
  exists max_elf,
    calories max_elf = n /\
    In max_elf elves /\
    forall elf, In elf elves -> calories max_elf >= calories elf
  }.
Proof.
  intros Hnil.
  pose (c := solution elves).
  exists c;split;[reflexivity|].
  unfold solution in c.
  destruct (non_empty_arg_max calories elves) as [max_elf (HSome&HIn&Hmax)];[assumption|];exists max_elf. 
  firstorder.
  enough (Some (calories max_elf) = Some c) by congruence; subst c.
  replace (Some (calories max_elf)) with (option_map calories (Some max_elf));[|reflexivity].
  rewrite <- HSome, arg_max_comm, <- arg_alt_id, arg_left_id;[reflexivity|].
  intros ?%map_eq_nil;easy.
Qed.

Import ListNotations.

Definition testElves := [
  [1000;
  2000;
  3000];
      
  [4000];
      
  [5000;
  6000];
      
  [7000;
  8000;
  9000];

  [10000]
].
Compute solution testElves.
Eval vm_compute in (solution testElves).

Require Import Extraction.
Extraction Language Haskell.

Require Import ExtrHaskellBasic.
Require Import ExtrHaskellNatInt.
Recursive Extraction solution.
