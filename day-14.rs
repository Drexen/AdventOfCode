use std::collections::HashMap;
use std::fs::File;
use std::io::{self, prelude::*, BufReader};

#[derive(Clone, Debug)]
struct Chemical {
    name: String,
    amount: i64,
}

fn main() {
    let file = File::open("src\\day-14-input.txt").unwrap();
    let reader = BufReader::new(file);

    let mut split_lines = Vec::new();
    for line in reader.lines() {
        let no_whitespace = line.unwrap().replace(" ", "");
        let parts: Vec<_> = no_whitespace.split("=>").collect();
        let inputs: Vec<_> = parts[0].split(",").map(|x| split_chemical(x)).collect();
        split_lines.push((inputs, split_chemical(parts[1])));
    }

    let mut reactions = HashMap::new();
    for split_line in split_lines.iter() {
        reactions.insert(
            (split_line.1).name.clone(),
            (split_line.1.clone(), split_line.0.clone()),
        );
    }

    part_one(&reactions);
    part_two(&reactions);
}

fn part_one(reactions: &HashMap<String, (Chemical, Vec<Chemical>)>) {
    let mut start = HashMap::new();
    start.insert("FUEL".to_owned(), 1);

    let result = break_down(start, &reactions);
    println!("Part one: {:?}", result);
}

fn part_two(reactions: &HashMap<String, (Chemical, Vec<Chemical>)>) {
    let mut prev = 0;
    let mut num_fuel = 0;
    for i in 0.. {
        prev = num_fuel;
        num_fuel = (2 as i64).pow(i);

        let mut start = HashMap::new();
        start.insert("FUEL".to_owned(), num_fuel);
        let result = break_down(start, &reactions);

        if result > 1_000_000_000_000 {
            break;
        }
    }

    let result = find_best(num_fuel, prev, reactions);
    println!("Part two: {:?}", result);
}

fn find_best(
    mut upper_bound: i64,
    mut lower_bound: i64,
    reactions: &HashMap<String, (Chemical, Vec<Chemical>)>,
) -> i64 {
    let mut guess = 0;
    loop {
        if lower_bound == upper_bound {
            return lower_bound;
        }

        guess = lower_bound + (upper_bound - lower_bound) / 2;

        let mut start = HashMap::new();
        start.insert("FUEL".to_owned(), guess);
        let result = break_down(start, &reactions);

        if result > 1_000_000_000_000 {
            upper_bound = guess;
        } else {
            if lower_bound == guess {
                upper_bound -= 1;
            } else {
                lower_bound = guess;
            }
        }
    }
    unreachable!();
}

fn break_down(
    mut chemicals: HashMap<String, i64>,
    reactions: &HashMap<String, (Chemical, Vec<Chemical>)>,
) -> i64 {
    while !finished(&chemicals) {
        let name = chemicals
            .iter()
            .filter(|(k, &v)| *k != "ORE" && v > 0)
            .next()
            .unwrap()
            .0
            .clone();
        let amount = chemicals[&name];
        chemicals.remove(&name);

        let reaction = &reactions[&name];
        let num_reactions = (amount as f32 / (reaction.0).amount as f32).ceil() as i64;
        let spare = (num_reactions * (reaction.0).amount) - amount;

        *chemicals.entry(name).or_insert(0) -= spare;

        for input_chemical in reaction.1.iter() {
            *chemicals.entry(input_chemical.name.clone()).or_insert(0) +=
                input_chemical.amount * num_reactions;
        }
    }

    chemicals[&"ORE".to_owned()]
}

fn finished(chemicals: &HashMap<String, i64>) -> bool {
    if chemicals.values().filter(|&x| *x > 0).count() > 1 {
        false
    } else {
        chemicals.contains_key(&"ORE".to_owned())
    }
}

fn split_chemical(chemical: &str) -> Chemical {
    let count: String = chemical.chars().take_while(|c| c.is_digit(10)).collect();
    let name: String = chemical.chars().skip_while(|c| c.is_digit(10)).collect();
    Chemical {
        name,
        amount: count.parse().unwrap(),
    }
}
