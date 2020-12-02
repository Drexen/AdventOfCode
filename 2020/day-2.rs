use regex::Regex;
use std::{fs::File, io::*};

fn main() {
    let mut f = File::open("src\\day-2-input.txt").unwrap();

    let r = Regex::new(r"(\d*)-(\d*)\s([a-z]):\s([a-z]*)").unwrap();
    let mut input: String = String::new();
    f.read_to_string(&mut input).unwrap();

    part_one(&input, &r);
    part_two(&input, &r);
}

fn part_one(input: &String, r: &Regex) {
    let mut count = 0;
    for cap in r.captures_iter(&input) {
        let min: u32 = cap[1].parse().unwrap();
        let max: u32 = cap[2].parse().unwrap();
        let target_char: char = cap[3].chars().next().unwrap();
        let password: &str = &cap[4];

        let matches = password.chars().filter(|c| *c == target_char).count() as u32;
        if matches >= min && matches <= max {
            count = count + 1;
        }
    }

    println!("{} valid passwords", count);
}

fn part_two(input: &String, r: &Regex) {
    let mut count = 0;
    for cap in r.captures_iter(&input) {
        let pos_a: u32 = cap[1].parse().unwrap();
        let pos_b: u32 = cap[2].parse().unwrap();
        let target_char: char = cap[3].chars().next().unwrap();
        let password: &str = &cap[4];

        let a = password.chars().nth((pos_a - 1) as usize).unwrap() == target_char;
        let b = password.chars().nth((pos_b - 1) as usize).unwrap() == target_char;

        if a ^ b {
            count = count + 1;
        }
    }

    println!("{} valid passwords", count);
}
