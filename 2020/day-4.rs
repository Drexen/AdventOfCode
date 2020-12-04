#![feature(try_blocks)]

use std::{collections::HashMap, fs::File, io::BufRead, io::BufReader};

use regex::Regex;

// Janky, requires two empty lines at the end of input
fn main() {
    part_one();
    part_two();
}

fn part_one() {
    let f = File::open("src\\day-4-input.txt").unwrap();
    let reader = BufReader::new(f);
    let mut current: String = String::new();
    let mut num_valid = 0;
    for line in reader.lines() {
        let line = line.unwrap();
        if line.len() > 0 {
            current += &line;
            current += " ";
        } else {
            if current.contains("byr:")
                && current.contains("iyr:")
                && current.contains("eyr:")
                && current.contains("hgt:")
                && current.contains("hcl:")
                && current.contains("ecl:")
                && current.contains("pid:")
            {
                num_valid = num_valid + 1;
            }

            current = String::new();
        }
    }

    println!("Part one = {}", num_valid);
}

fn part_two() {
    let f = File::open("src\\day-4-input.txt").unwrap();
    let reader = BufReader::new(f);
    let mut current: String = String::new();
    let mut num_valid = 0;
    for line in reader.lines() {
        let line = line.unwrap();
        if line.len() > 0 {
            current += &line;
            current += " ";
        } else {
            if is_valid_passport(&current) {
                num_valid = num_valid + 1;
            }

            current = String::new();
        }
    }

    println!("Part two = {}", num_valid);
}

fn is_valid_passport(input: &str) -> bool {
    let dict: HashMap<&str, &str> = input
        .split(" ")
        .filter_map(|s| {
            if s.len() == 0 {
                return None;
            }
            let mut s = s.split(":");
            Some((s.next().unwrap(), s.next().unwrap()))
        })
        .collect();

    let output: Option<()> = try {
        let birth_year: u32 = dict.get("byr")?.parse().ok()?;
        if birth_year < 1920 || birth_year > 2002 {
            return false;
        }

        let issue_year: u32 = dict.get("iyr")?.parse().ok()?;
        if issue_year < 2010 || issue_year > 2020 {
            return false;
        }

        let expr_year: u32 = dict.get("eyr")?.parse().ok()?;
        if expr_year < 2020 || expr_year > 2030 {
            return false;
        }

        let height_raw = dict.get("hgt")?;
        let height: u32 = height_raw[..height_raw.len() - 2].parse().ok()?;
        if height_raw.chars().nth(height_raw.len() - 2)? == 'c'
            && height_raw.chars().nth(height_raw.len() - 1)? == 'm'
        {
            if height < 150 || height > 193 {
                return false;
            }
        } else if height_raw.chars().nth(height_raw.len() - 2)? == 'i'
            && height_raw.chars().nth(height_raw.len() - 1)? == 'n'
        {
            if height < 59 || height > 76 {
                return false;
            }
        } else {
            return false;
        }

        let hair_color = dict.get("hcl")?;
        let r = Regex::new(r"#[a-f0-9]{6}").unwrap();
        if !r.is_match(&hair_color) {
            return false;
        }

        let eye_color = dict.get("ecl")?;
        if *eye_color != "amb"
            && *eye_color != "blu"
            && *eye_color != "brn"
            && *eye_color != "gry"
            && *eye_color != "grn"
            && *eye_color != "hzl"
            && *eye_color != "oth"
        {
            return false;
        }

        let pid = dict.get("pid")?;
        if pid.len() != 9 || pid.chars().any(|c| !c.is_digit(10)) {
            return false;
        }
    };

    output.is_some()
}
