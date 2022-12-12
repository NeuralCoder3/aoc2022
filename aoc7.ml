let str = "
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"

type ('a) tree = Node of 'a * ('a tree) list
type filetype = Dir of string | File of string * int
type command = Cd of string | Ls

let rec insert path data tree = 
  match path,tree with
  | [], Node (f, xs) -> Node (f, data @ xs)
  | p::pr, Node (f, xs) ->
    Node (f, List.map (fun x -> 
        match x with
        | Node (f, xs) -> 
          if f = p then insert pr data x
          else x
      ) xs
    )

let parse_cmd s = 
  let s = String.trim s in
  let cmd, args = 
    s
    |> String.split_on_char ' '
    |> List.map (String.trim)
    |> List.filter (fun s -> s <> "")
    |> (fun l -> (List.hd l, List.tl l))
  in
  match cmd with
  | "cd" -> Cd (List.hd args)
  | "ls" -> Ls
  | _ -> failwith "Invalid command"

let parse_file l =
  let xs=l
    |> String.split_on_char ' '
    |> List.map (String.trim)
    |> List.filter (fun s -> s <> "")
  in
  match xs with
  | "dir"::name::[] -> Dir name
  | size::name::[] -> File (name, int_of_string size)
  | _ -> failwith "Invalid file"

(* returns list of dirs with sizes *)
let rec list_dirs t =
  match t with
  | Node (f, files) -> 
    match f with
    | Dir s -> 
      let xs = List.map list_dirs files in
      let xs = List.concat xs in
      let dirsize = List.fold_left (fun acc (_,size) -> acc + size) 0 xs in
      let size = dirsize + (List.fold_left (fun acc -> function
          | Node (File (_,size), _) -> acc + size
          | _ -> acc
        ) 0 files) in
      (s, size) :: xs
    | File _ -> []

let parse_cmd_line s = 
  s
  |> String.split_on_char '$'
  |> List.map (String.trim)
  |> List.filter (fun s -> s <> "")
  |> List.map (fun s -> 
      s
      |> String.split_on_char '\n'
      |> List.map (String.trim)
      |> List.filter (fun s -> s <> "")
      |> (fun l -> (List.hd l, List.tl l))
    )
  |> List.map (fun (cmd, l) -> 
      (parse_cmd cmd, l)
    )
  |> List.fold_left (fun (tree, dir) (cmd, l) -> 
      match cmd with
      | Cd "/" -> (tree, [])
      | Cd ".." -> (tree, List.rev(List.tl(List.rev dir))) (* Filename.dirname *)
      | Cd s -> (tree, dir @ [s]) (* Filename.concat *)
      | Ls -> insert dir (List.map (fun s -> Node(parse_file s, [])) l) tree
    ) (Leaf "", [])
  |> fst
  |> list_dirs
