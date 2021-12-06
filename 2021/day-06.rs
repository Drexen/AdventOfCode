use std::{
    fs::File,
    io::{BufRead, BufReader},
};

pub fn main() {
    let file = File::open("src\\day-06-input.txt").unwrap();
    let mut lines = BufReader::new(file).lines();
    let input = lines.next().unwrap().unwrap();

    let all_fish: Vec<u64> = input.split(",").map(|n| n.parse().unwrap()).collect();
    let mut fish: Vec<u64> = vec![0; 10];
    for f in all_fish {
        fish[f as usize] += 1;
    }

    println!("Part one = {}", simulate(fish.clone(), 80));
    println!("Part two = {}", simulate(fish.clone(), 256));
}

pub fn simulate(mut fish: Vec<u64>, days: u32) -> u64 {
    for _ in 0..days {
        fish[7] += fish[0];
        fish[9] = fish[0];
        for i in 0..9 {
            fish[i] = fish[i + 1];
        }
        fish[9] = 0;
    }
    fish.iter().sum::<u64>()
}
