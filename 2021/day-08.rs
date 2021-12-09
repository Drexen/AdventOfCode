use std::{
    collections::HashMap,
    fs::File,
    io::{BufRead, BufReader},
};

pub fn main() {
    let file = File::open("src\\day-08-input.txt").unwrap();
    let lines = BufReader::new(file).lines();

    let mut p1_count = 0;
    let mut p2_count = 0;
    for line in lines {
        let line = line.unwrap();
        let mut line = line.split(" | ");

        let input: Vec<String> = line
            .next()
            .unwrap()
            .split(" ")
            .map(|n| {
                let mut a = n.to_owned().chars().collect::<Vec<_>>();
                a.sort();
                a.iter().collect::<String>()
            })
            .collect();

        let output: Vec<String> = line
            .next()
            .unwrap()
            .split(" ")
            .map(|n| {
                let mut a = n.to_owned().chars().collect::<Vec<_>>();
                a.sort();
                a.iter().collect::<String>()
            })
            .collect();

        p1_count += output
            .iter()
            .filter(|n| n.len() == 2 || n.len() == 3 || n.len() == 4 || n.len() == 7)
            .count();

        p2_count += solve_wires(input, output);
    }

    println!("Part one = {}", p1_count);
    println!("Part two = {}", p2_count);
}

pub fn solve_wires(input: Vec<String>, output: Vec<String>) -> u32 {
    let mut mapping: HashMap<String, u32> = HashMap::new();

    let len2_digit = input.iter().filter(|n| n.len() == 2).next().unwrap();
    mapping.insert(len2_digit.clone(), 1);

    let len3_digit = input.iter().filter(|n| n.len() == 3).next().unwrap();
    mapping.insert(len3_digit.clone(), 7);

    let len4_digit = input.iter().filter(|n| n.len() == 4).next().unwrap();
    mapping.insert(len4_digit.clone(), 4);

    let len7_digit = input.iter().filter(|n| n.len() == 7).next().unwrap();
    mapping.insert(len7_digit.clone(), 8);

    // six segment digits
    let sixes: Vec<_> = input.iter().filter(|c| c.len() == 6).collect();
    assert!(sixes.len() == 3);

    let six_digit: Vec<_> = sixes
        .iter()
        .filter(|s| len2_digit.chars().any(|d| s.contains(d) == false))
        .collect();
    assert!(six_digit.len() == 1);
    mapping.insert(six_digit[0].to_string(), 6);

    let nine_digit: Vec<_> = sixes
        .iter()
        .filter(|s| len4_digit.chars().all(|d| s.contains(d)))
        .collect();
    assert!(nine_digit.len() == 1);
    mapping.insert(nine_digit[0].to_string(), 9);

    let zero_digit: Vec<_> = sixes
        .iter()
        .filter(|s| *s != six_digit[0] && *s != nine_digit[0])
        .collect();
    assert!(zero_digit.len() == 1);
    mapping.insert(zero_digit[0].to_string(), 0);

    // five segment digits
    let fives: Vec<_> = input.iter().filter(|c| c.len() == 5).collect();
    assert!(fives.len() == 3);

    let three_digit: Vec<_> = fives
        .iter()
        .filter(|s| len2_digit.chars().all(|d| s.contains(d)))
        .collect();
    assert!(three_digit.len() == 1);
    mapping.insert(three_digit[0].to_string(), 3);

    let five_digit: Vec<_> = fives
        .iter()
        .filter(|s| {
            six_digit[0]
                .chars()
                .filter(|d| s.contains(*d) == false)
                .count()
                == 1
        })
        .collect();
    assert!(five_digit.len() == 1);
    mapping.insert(five_digit[0].to_string(), 5);

    let two_digit: Vec<_> = fives
        .iter()
        .filter(|s| *s != three_digit[0] && *s != five_digit[0])
        .collect();
    assert!(two_digit.len() == 1);
    mapping.insert(two_digit[0].to_string(), 2);

    let mut count = 0;
    output
        .iter()
        .rev()
        .enumerate()
        .for_each(|(i, s)| count += mapping.get(s).unwrap() * 10_u32.pow(i as u32));
    count
}
