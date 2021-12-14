use std::collections::HashMap;

fn main() {
    let lines: Vec<_> = include_str!("day-14-input.txt").lines().collect();
    let polymer = lines[0].to_owned();
    let rules: HashMap<[char; 2], [char; 3]> = lines
        .iter()
        .skip(2)
        .map(|s| s.replace(" -> ", "").chars().collect::<Vec<_>>())
        .map(|s| ([s[0], s[1]], [s[0], s[2], s[1]]))
        .collect();

    println!("Part one = {}", solve(10, &polymer, &rules));
    println!("Part two = {}", solve(40, &polymer, &rules));
}

pub fn solve(num_steps: u64, polymer: &String, rules: &HashMap<[char; 2], [char; 3]>) -> u64 {
    let mut memoization = HashMap::new();

    let occurences = polymer
        .chars()
        .collect::<Vec<_>>()
        .windows(2)
        .map(|pair| {
            (
                memoized_apply_rules([pair[0], pair[1]], num_steps, &rules, &mut memoization),
                pair[0],
            )
        })
        .collect::<Vec<_>>();

    let mut character_occurences = occurences[0].0.clone();
    for occurence in occurences.iter().skip(1) {
        character_occurences =
            merge_occurences(character_occurences, occurence.0.clone(), occurence.1);
    }

    let mut character_occurences: Vec<_> = character_occurences.iter().collect();
    character_occurences.sort_by_key(|e| e.1);
    let result = character_occurences.last().unwrap().1 - character_occurences.first().unwrap().1;
    result
}

fn memoized_apply_rules(
    input: [char; 2],
    remaining_depth: u64,
    rules: &HashMap<[char; 2], [char; 3]>,
    memoization: &mut HashMap<([char; 2], u64), HashMap<char, u64>>,
) -> HashMap<char, u64> {
    if let Some(result) = memoization.get(&(input, remaining_depth)) {
        result.clone()
    } else {
        let result = apply_rules(input, remaining_depth, rules, memoization);
        memoization.insert((input, remaining_depth), result.clone());
        result
    }
}

fn apply_rules(
    input: [char; 2],
    remaining_depth: u64,
    rules: &HashMap<[char; 2], [char; 3]>,
    memoization: &mut HashMap<([char; 2], u64), HashMap<char, u64>>,
) -> HashMap<char, u64> {
    if let Some(replacement) = rules.get(&input) {
        if remaining_depth > 0 {
            let left = memoized_apply_rules(
                [replacement[0], replacement[1]],
                remaining_depth - 1,
                rules,
                memoization,
            );
            let right = memoized_apply_rules(
                [replacement[1], replacement[2]],
                remaining_depth - 1,
                rules,
                memoization,
            );

            return merge_occurences(left, right, replacement[1]);
        }
    }

    let mut result = HashMap::new();
    *result.entry(input[0]).or_default() += 1;
    *result.entry(input[1]).or_default() += 1;
    result
}

fn merge_occurences(
    mut left: HashMap<char, u64>,
    right: HashMap<char, u64>,
    middle_char: char,
) -> HashMap<char, u64> {
    for (k, v) in right {
        *left.entry(k).or_default() += v;
    }

    *left.get_mut(&middle_char).unwrap() -= 1;

    return left;
}
