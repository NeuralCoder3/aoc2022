// automatically transpiled from python using semantical preservation

use std::collections::HashMap;
use regex::Regex;
use std::fs;
use std::env::args;
use rayon::prelude::*;

pub fn main() {
  // from command line
    let file = args().nth(1).expect("No file name given");
    let contents = fs::read_to_string(file).expect("Error reading file");
    let lines: Vec<&str> = contents.split("\n").collect();
    let pattern = Regex::new(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.").unwrap();
    let mut blueprints = vec![];
    for line in lines {
        if let Some(captures) = pattern.captures(line) {
            let num: i32 = captures[1].parse().unwrap();
            let ore_ore: i32 = captures[2].parse().unwrap();
            let clay_ore: i32 = captures[3].parse().unwrap();
            let obsidian_ore: i32 = captures[4].parse().unwrap();
            let obsidian_clay: i32 = captures[5].parse().unwrap();
            let geode_ore: i32 = captures[6].parse().unwrap();
            let geode_obsidian: i32 = captures[7].parse().unwrap();
            blueprints.push((num, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian));
        }
    }

    // let time = 24;
    // let time = 32;
    let time = args().nth(2).unwrap_or("24".to_string()).parse().unwrap();
    println!("Emulate for {}min", time);
    // only keep three blueprints
    let blueprints = blueprints.into_iter().take(3).collect::<Vec<_>>();
    // parallel over blueprints
    blueprints.par_iter().for_each(|b| {
        println!("Start Blueprint {:?}", b);
        let mut cache = HashMap::new();
        println!("{:?}: {}", b, get_geodes(time, &mut cache, 1, 0, 0, 0, 0, 0,b));
    });
}

fn get_geodes(time: i32, cache: &mut HashMap<(i32, i32, i32, i32, i32, i32, i32), i32>,
               oreR: i32, clayR: i32, obsidianR: i32, ore: i32, clay: i32, obsidian: i32, 
               b: &(i32,i32,i32,i32,i32,i32,i32)) -> i32 {
    let (num, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian) = *b;
    if time == 0 {
        return 0;
    }
    if let Some(geode) = cache.get(&(time, oreR, clayR, obsidianR, ore, clay, obsidian)) {
        return *geode;
    }
    let new_ore = ore + oreR;
    let new_clay = clay + clayR;
    let new_obsidian = obsidian + obsidianR;
    let mut geode = get_geodes(time - 1, cache, oreR, clayR, obsidianR, new_ore, new_clay, new_obsidian, b);
    if ore_ore <= ore {
        geode = std::cmp::max(geode, get_geodes(time - 1, cache, oreR + 1, clayR, obsidianR, new_ore - ore_ore, new_clay, new_obsidian, b));
    }
    if clay_ore <= ore {
        geode = std::cmp::max(geode, get_geodes(time - 1, cache, oreR, clayR + 1, obsidianR, new_ore - clay_ore, new_clay, new_obsidian, b));
    }
    if obsidian_ore <= ore && obsidian_clay <= clay {
        geode = std::cmp::max(geode, get_geodes(time - 1, cache, oreR, clayR, obsidianR + 1, new_ore - obsidian_ore, new_clay - obsidian_clay, new_obsidian, b));
    }
    if geode_ore <= ore && geode_obsidian <= obsidian {
        geode = std::cmp::max(geode, get_geodes(time - 1, cache, oreR, clayR, obsidianR, new_ore - geode_ore, new_clay, new_obsidian - geode_obsidian, b) + (time - 1));
    }
    cache.insert((time, oreR, clayR, obsidianR, ore, clay, obsidian), geode);
    geode
}
