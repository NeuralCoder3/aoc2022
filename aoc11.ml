(* alternative the operation can be a polynomial *)

type 'a monkey = {
  name: 'a;
  items: int list;
  op: int -> int;
  test: int -> bool;
  testtrue: 'a;
  testfalse: 'a;
}

(*
Monkey 0:
  Starting items: 73, 77
  Operation: new = old * 5
  Test: divisible by 11
    If true: throw to monkey 6
    If false: throw to monkey 5

Monkey 1:
  Starting items: 57, 88, 80
  Operation: new = old + 5
  Test: divisible by 19
    If true: throw to monkey 6
    If false: throw to monkey 0

Monkey 2:
  Starting items: 61, 81, 84, 69, 77, 88
  Operation: new = old * 19
  Test: divisible by 5
    If true: throw to monkey 3
    If false: throw to monkey 1

Monkey 3:
  Starting items: 78, 89, 71, 60, 81, 84, 87, 75
  Operation: new = old + 7
  Test: divisible by 3
    If true: throw to monkey 1
    If false: throw to monkey 0

Monkey 4:
  Starting items: 60, 76, 90, 63, 86, 87, 89
  Operation: new = old + 2
  Test: divisible by 13
    If true: throw to monkey 2
    If false: throw to monkey 7

Monkey 5:
  Starting items: 88
  Operation: new = old + 1
  Test: divisible by 17
    If true: throw to monkey 4
    If false: throw to monkey 7

Monkey 6:
  Starting items: 84, 98, 78, 85
  Operation: new = old * old
  Test: divisible by 7
    If true: throw to monkey 5
    If false: throw to monkey 4

Monkey 7:
  Starting items: 98, 89, 78, 73, 71
  Operation: new = old + 4
  Test: divisible by 2
    If true: throw to monkey 3
    If false: throw to monkey 2
*)

let monkeys = [
  {
    name = 0;
    items = [73; 77];
    op = (fun old -> old * 5);
    test = (fun x -> x mod 11 = 0);
    testtrue = 6;
    testfalse = 5
  };
  {
    name = 1;
    items = [57; 88; 80];
    op = (fun old -> old + 5);
    test = (fun x -> x mod 19 = 0);
    testtrue = 6;
    testfalse = 0
  };
  {
    name = 2;
    items = [61; 81; 84; 69; 77; 88];
    op = (fun old -> old * 19);
    test = (fun x -> x mod 5 = 0);
    testtrue = 3;
    testfalse = 1
  };
  {
    name = 3;
    items = [78; 89; 71; 60; 81; 84; 87; 75];
    op = (fun old -> old + 7);
    test = (fun x -> x mod 3 = 0);
    testtrue = 1;
    testfalse = 0
  };
  {
    name = 4;
    items = [60; 76; 90; 63; 86; 87; 89];
    op = (fun old -> old + 2);
    test = (fun x -> x mod 13 = 0);
    testtrue = 2;
    testfalse = 7
  };
  {
    name = 5;
    items = [88];
    op = (fun old -> old + 1);
    test = (fun x -> x mod 17 = 0);
    testtrue = 4;
    testfalse = 7
  };
  {
    name = 6;
    items = [84; 98; 78; 85];
    op = (fun old -> old * old);
    test = (fun x -> x mod 7 = 0);
    testtrue = 5;
    testfalse = 4
  };
  {
    name = 7;
    items = [98; 89; 78; 73; 71];
    op = (fun old -> old + 4);
    test = (fun x -> x mod 2 = 0);
    testtrue = 3;
    testfalse = 2
  }
]


let test = [
  {
    name = 0;
    items = [79; 98];
    op = (fun old -> old * 19);
    test = (fun x -> x mod 23 = 0);
    testtrue = 2;
    testfalse = 3
  };
  {
    name = 1;
    items = [54; 65; 75; 74];
    op = (fun old -> old + 6);
    test = (fun x -> x mod 19 = 0);
    testtrue = 2;
    testfalse = 0
  };
  {
    name = 2;
    items = [79; 60; 97];
    op = (fun old -> old * old);
    test = (fun x -> x mod 13 = 0);
    testtrue = 1;
    testfalse = 3
  };
  {
    name = 3;
    items = [74];
    op = (fun old -> old + 3);
    test = (fun x -> x mod 17 = 0);
    testtrue = 0;
    testfalse = 1
  }
]

let map_of_list key_fun xs = 
  fun key ->
    List.find (fun x -> key_fun x = key) xs

let update f key new_val = fun k ->
  if k = key then new_val else f k

  (* test = key = key_fun x *)
let update_list xs test xs new_val =
  List.map (fun x -> if test x then new_val else x) xs

let rec iter k f a = 
  if k = 0 then a else iter (k - 1) f (f a)

(* let modulus = 3 *)

let round modulus (trace,monkeys) =
  List.fold_left (fun (trace,monkeys) id ->
    let monkey = List.find (fun m -> m.name = id) monkeys in
    List.fold_left (fun (trace,monkeys) item ->
      let new_item = monkey.op item in
      (* let new_item = new_item / 3 in *)
      let new_item = new_item mod modulus in
      let new_id = if monkey.test new_item then monkey.testtrue else monkey.testfalse in
      let new_monkeys = List.map (fun m -> if m.name = new_id then {m with items = m.items @ [new_item]} else m) monkeys in
      ((id,new_id,item,new_item)::trace, new_monkeys)
    ) (trace,List.map (fun m -> if m.name = id then {m with items = []} else m) monkeys) monkey.items
  )
  (trace, monkeys)
  (List.map (fun m -> m.name) monkeys)

let runs k monkeys =
  let modulus = 11*19*5*3*13*17*7*2 in
  (* let modulus = 23*19*13*17 in *)
  iter k (round modulus) ([],monkeys)

let accumulate (trace,monkeys) =
  List.map (fun m ->
    (m, List.length (List.filter (fun (id,_,_,_) -> id = m.name) trace))
  ) monkeys
  |> List.sort (fun (_,a) (_,b) -> b - a)

(* 
   #use "aoc11.ml";; 
   *)

let _ =
  (* test *)
  monkeys
  |> runs 10000
  |> accumulate
  |> List.iter (fun (m,n) -> Printf.printf "Monkey %d: %d\n" m.name n)
