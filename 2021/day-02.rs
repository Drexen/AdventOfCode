use std::{
    fs::File,
    io::{BufRead, BufReader},
};

pub fn main() {
    let file = File::open("src\\day-02-input.txt").unwrap();
    let lines = BufReader::new(file).lines();
    let mut horizontal: i32 = 0;
    let mut depth: i32 = 0;

    let parsed: Vec<_> = lines.map(|l| l.unwrap()).collect();

    for text in &parsed {
        let amount: i32 = text.chars().rev().next().unwrap().to_digit(10).unwrap() as i32;

        if text.contains("forward") {
            horizontal += amount;
        } else if text.contains("down") {
            depth += amount;
        } else if text.contains("up") {
            depth -= amount;
        }
    }

    println!("Part one = {}", horizontal * depth);

    horizontal = 0;
    depth = 0;
    let mut aim = 0;
    for text in &parsed {
        let amount: i32 = text.chars().rev().next().unwrap().to_digit(10).unwrap() as i32;

        if text.contains("forward") {
            horizontal += amount;
            depth += aim * amount;
        } else if text.contains("down") {
            aim += amount;
        } else if text.contains("up") {
            aim -= amount;
        }
    }

    println!("Part two = {}", horizontal * depth);
}
