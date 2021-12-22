#![feature(destructuring_assignment)]

use std::ops::Add;

#[derive(Debug, Clone)]
pub enum SNumber {
    Value(u32),
    Pair(Box<SNumber>, Box<SNumber>),
}

impl Add for SNumber {
    type Output = SNumber;

    fn add(self, rhs: Self) -> Self::Output {
        let snumber = SNumber::Pair(Box::new(self), Box::new(rhs));
        reduce(snumber)
    }
}

fn main() {
    let lines = include_str!("day-18-input.txt").lines();
    let snumbers: Vec<_> = lines.map(|s| parse_input(s).0).collect();

    let first = snumbers.first().unwrap().clone();
    let sum = snumbers.clone().into_iter().fold(first, |sum, n| sum + n);
    let mag = get_magnitude(sum);
    println!("Part one = {}", mag);

    let mut largest_mag = 0;
    for x in 0..snumbers.len() {
        for y in 0..snumbers.len() {
            if x != y {
                let sum = (&snumbers[x]).clone() + (&snumbers[y]).clone();
                let mag = get_magnitude(sum);
                largest_mag = u32::max(mag, largest_mag);
            }
        }
    }

    println!("Part two = {}", largest_mag);
}

pub fn get_magnitude(snumber: SNumber) -> u32 {
    match snumber {
        SNumber::Value(v) => v,
        SNumber::Pair(l, r) => 3 * get_magnitude(*l) + 2 * get_magnitude(*r),
    }
}

pub fn reduce(mut snumber: SNumber) -> SNumber {
    loop {
        let (new_snumber, exploded, _, _) = try_explode(snumber, 0);
        snumber = new_snumber;
        if exploded == true {
            continue;
        }

        let split;
        (snumber, split) = try_split(snumber);
        if split == false {
            return snumber;
        }
    }
}

pub fn try_explode(snumber: SNumber, depth: u32) -> (SNumber, bool, Option<u32>, Option<u32>) {
    match snumber {
        SNumber::Value(_) => (snumber, false, None, None),
        SNumber::Pair(left, right) => {
            if depth == 4 {
                match (*left, *right) {
                    (SNumber::Value(left), SNumber::Value(right)) => {
                        return (SNumber::Value(0), true, Some(left), Some(right))
                    }
                    _ => panic!(),
                };
            }

            let (left, exploded, lv, rv) = try_explode(*left, depth + 1);
            if let Some(rv) = rv {
                let right = add_to_left_most_value(*right, rv);
                return (
                    SNumber::Pair(Box::new(left), Box::new(right)),
                    exploded,
                    lv,
                    None,
                );
            }

            if exploded == true {
                return (
                    SNumber::Pair(Box::new(left), Box::new(*right)),
                    exploded,
                    lv,
                    rv,
                );
            }

            let (right, exploded, lv, rv) = try_explode(*right, depth + 1);
            if let Some(lv) = lv {
                let left = add_to_right_most_value(left, lv);
                return (
                    SNumber::Pair(Box::new(left), Box::new(right)),
                    exploded,
                    None,
                    rv,
                );
            }

            return (
                SNumber::Pair(Box::new(left), Box::new(right)),
                exploded,
                lv,
                rv,
            );
        }
    }
}

pub fn try_split(snumber: SNumber) -> (SNumber, bool) {
    match snumber {
        SNumber::Value(v) => {
            if v >= 10 {
                (
                    SNumber::Pair(
                        Box::new(SNumber::Value(v / 2)),
                        Box::new(SNumber::Value(v - (v / 2))),
                    ),
                    true,
                )
            } else {
                (SNumber::Value(v), false)
            }
        }
        SNumber::Pair(left, right) => {
            let (left, split) = try_split(*left);
            if split == true {
                return (SNumber::Pair(Box::new(left), right), true);
            }
            let (right, split) = try_split(*right);
            (SNumber::Pair(Box::new(left), Box::new(right)), split)
        }
    }
}

pub fn add_to_right_most_value(snumber: SNumber, value: u32) -> SNumber {
    match snumber {
        SNumber::Value(v) => SNumber::Value(v + value),
        SNumber::Pair(left, right) => {
            SNumber::Pair(left, Box::new(add_to_right_most_value(*right, value)))
        }
    }
}

pub fn add_to_left_most_value(snumber: SNumber, value: u32) -> SNumber {
    match snumber {
        SNumber::Value(v) => SNumber::Value(v + value),
        SNumber::Pair(left, right) => {
            SNumber::Pair(Box::new(add_to_left_most_value(*left, value)), right)
        }
    }
}

pub fn parse_input(input: &str) -> (SNumber, &str) {
    let next_char = input.chars().next().unwrap();
    match next_char {
        '[' => {
            let (left, input) = parse_input(input.split_at(1).1);

            let next_char = input.chars().next().unwrap();
            assert!(next_char == ',');

            let (right, input) = parse_input(input.split_at(1).1);

            let next_char = input.chars().next().unwrap();
            assert!(next_char == ']');

            return (
                SNumber::Pair(Box::new(left), Box::new(right)),
                input.split_at(1).1,
            );
        }
        next_char => {
            if let Some(next_char) = next_char.to_digit(10) {
                return (SNumber::Value(next_char), input.split_at(1).1);
            }
        }
    }

    panic!();
}
