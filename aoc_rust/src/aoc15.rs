// automatically transpiled from python using semantical preservation

use regex::Regex;
use std::fs::File;
use std::io::{BufRead, BufReader};
use tqdm::tqdm;

pub fn main() {
    let pattern =
        Regex::new(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
            .unwrap();
    let mut signals = Vec::new();

    let file = File::open("../aoc15.txt").expect("Failed to open aoc15.txt");
    let lines = BufReader::new(file)
        .lines()
        .filter_map(Result::ok)
        .filter(|line| !line.is_empty());

    for line in lines {
        if let Some(captures) = pattern.captures(&line) {
            let sx = captures[1].parse::<i32>().unwrap();
            let sy = captures[2].parse::<i32>().unwrap();
            let bx = captures[3].parse::<i32>().unwrap();
            let by = captures[4].parse::<i32>().unwrap();
            let distance = (sx - bx).abs() + (sy - by).abs();
            signals.push((sx, sy, bx, by, distance));
        } else {
            println!("ERROR");
        }
    }

    let row = 2000000;
    let bound = 2 * row;

    let mut possibilites = Vec::new();

    for row in tqdm(0..=bound) {
        let mut intervals = Vec::new();
        let mut beacons = Vec::new();

        for (sx, sy, bx, by, distance) in &signals {
            let dist_on_row = distance - (sy - row).abs();
            let int_start = sx - dist_on_row;
            let int_end = sx + dist_on_row;

            if int_start <= int_end {
                intervals.push((int_start, int_end));
            }

            if *by == row {
                beacons.push((*bx, *by));
            }
        }

        intervals.sort();

        let mut count = 0;
        let mut pos = None;

        for (int_start, int_end) in intervals {
            if pos.is_none() {
                if int_start > 0 {
                    possibilites.push((0, int_start - 1, row));
                }

                pos = Some(int_start);
            } else {
                if pos.unwrap() < int_start {
                    possibilites.push((pos.unwrap(), int_start - 1, row));
                }

                pos = pos.max(Some(int_start));
            }

            if pos.unwrap() > int_end {
                continue;
            }

            count += int_end - pos.unwrap() + 1;
            pos = Some(int_end + 1);
        }
    }

    for (x1, x2, y) in possibilites {
        println!("{} {} {}", x1, x2, y);
    }
}
