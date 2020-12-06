use std::{collections::HashMap, collections::HashSet, fs::File, io::BufRead, io::BufReader};

// Janky, requires two empty lines at the end of input
fn main() {
    part_one();
    part_two();
}

fn part_one() {
    let f = File::open("src\\day-6-input.txt").unwrap();
    let reader = BufReader::new(f);
    let mut current: HashSet<char> = HashSet::new();
    let mut sum = 0;
    for line in reader.lines() {
        let line = line.unwrap();
        if line.len() > 0 {
            line.chars().for_each(|c| {
                current.insert(c);
            });
        } else {
            sum = sum + current.len();
            current.clear();
        }
    }

    println!("Part one = {}", sum);
}

fn part_two() {
    let f = File::open("src\\day-6-input.txt").unwrap();
    let reader = BufReader::new(f);
    let mut current: HashMap<char, u32> = HashMap::new();
    let mut sum = 0;
    let mut num_members = 0;
    for line in reader.lines() {
        let line = line.unwrap();
        if line.len() > 0 {
            num_members = num_members + 1;
            line.chars().for_each(|c| {
                let v = current.entry(c).or_insert(0);
                *v = *v + 1;
            });
        } else {
            sum = sum + current.iter().filter(|(_, c)| **c == num_members).count();
            current.clear();
            num_members = 0;
        }
    }

    println!("Part two = {}", sum);
}
