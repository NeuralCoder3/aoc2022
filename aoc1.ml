let file = "aoc1.txt"

let read_lines file =
    let lines = ref [] in
    let chan = open_in file in
    try
        while true; do
            lines := input_line chan :: !lines
        done; !lines
    with End_of_file ->
        close_in chan;
        List.rev !lines

open List;;

let sum = fold_left (+) 0

let rec take n = function
    | [] -> []
    | x :: xs -> if n = 0 then [] else x :: take (n - 1) xs

let elfes n = 
  let rec group aux xs =
    match xs with  
    | None::xr -> rev aux::(group [] xr)
    | Some x::xr -> group (x::aux) xr
    | [] -> if aux = [] then [] else [rev aux]
  in
  file 
  |> read_lines
  |> map (fun x -> if x = "" then None else Some (int_of_string x))
  |> group []
  |> map sum
  |> sort (fun x y -> Int.compare y x)
  |> take n 
  |> sum
  |> string_of_int
  |> print_endline

let () = 
  elfes 1;
  elfes 3
