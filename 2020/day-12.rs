use std::{
    fs::File,
    io::{BufRead, BufReader},
};

const EAST: i32 = 0;
const SOUTH: i32 = 1;
const WEST: i32 = 2;
const NORTH: i32 = 3;

fn main() {
    let f = File::open("src\\day-12-input.txt").unwrap();
    let reader = BufReader::new(f);
    let inputs: Vec<(String, i32)> = reader
        .lines()
        .map(|l| {
            let l = l.unwrap();
            let s = l.split_at(1);
            (s.0.to_string(), s.1.parse().unwrap())
        })
        .collect();

    part_one(&inputs);
    part_two(&inputs);
}

fn part_one(inputs: &Vec<(String, i32)>) {
    let mut pos_ship = (0, 0);
    let mut heading: i32 = EAST;
    for i in inputs {
        let i = (i.0.as_str(), i.1);
        match i {
            ("N", val) => pos_ship.1 += val,
            ("S", val) => pos_ship.1 -= val,
            ("E", val) => pos_ship.0 += val,
            ("W", val) => pos_ship.0 -= val,
            ("F", val) => match heading {
                EAST => (pos_ship.0 += val),
                SOUTH => (pos_ship.1 -= val),
                WEST => (pos_ship.0 -= val),
                NORTH => (pos_ship.1 += val),
                _ => (),
            },
            (rot, val) => {
                let val = val / 90;
                if rot == "R" {
                    heading += val;
                } else if rot == "L" {
                    heading -= val;
                }
                heading = (heading + 4) % 4;
            }
        }
    }

    let d = pos_ship.0.abs() + pos_ship.1.abs();
    println!("Part one = {}", d);
}

fn part_two(inputs: &Vec<(String, i32)>) {
    let mut pos_wp = (10, 1);
    let mut pos_ship = (0, 0);
    for i in inputs {
        let i = (i.0.as_str(), i.1);
        match i {
            ("N", val) => pos_wp.1 += val,
            ("S", val) => pos_wp.1 -= val,
            ("E", val) => pos_wp.0 += val,
            ("W", val) => pos_wp.0 -= val,
            ("F", val) => {
                pos_ship = (pos_ship.0 + (pos_wp.0 * val), pos_ship.1 + (pos_wp.1 * val));
            }
            (rot, val) => {
                let num_rotations = match rot {
                    "R" => val / 90,
                    "L" => 4 - (val / 90),
                    _ => panic!(),
                };
                for _ in 0..num_rotations {
                    pos_wp = (pos_wp.1, -pos_wp.0);
                }
            }
        }
    }

    let d = pos_ship.0.abs() + pos_ship.1.abs();
    println!("Part two = {}", d);
}
