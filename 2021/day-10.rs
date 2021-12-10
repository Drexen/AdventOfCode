use std::{
    collections::HashMap,
    fs::File,
    io::{BufRead, BufReader},
};

pub fn main() {
    let file = File::open("src\\day-10-input.txt").unwrap();
    let lines = BufReader::new(file).lines();

    let mut opening_mapping: HashMap<char, char> = HashMap::new();
    opening_mapping.insert(')', '(');
    opening_mapping.insert(']', '[');
    opening_mapping.insert('}', '{');
    opening_mapping.insert('>', '<');

    let mut syntax_error_cost: HashMap<char, u32> = HashMap::new();
    syntax_error_cost.insert(')', 3);
    syntax_error_cost.insert(']', 57);
    syntax_error_cost.insert('}', 1197);
    syntax_error_cost.insert('>', 25137);

    let mut autocomplete_mapping: HashMap<char, u64> = HashMap::new();
    autocomplete_mapping.insert('(', 1);
    autocomplete_mapping.insert('[', 2);
    autocomplete_mapping.insert('{', 3);
    autocomplete_mapping.insert('<', 4);

    let mut syntax_error_total = 0;
    let mut autocomplete_scores: Vec<u64> = vec![];
    'lines_iter: for line in lines {
        let line = line.unwrap();
        let mut stack: Vec<char> = vec![];
        for c in line.chars() {
            match c {
                '(' | '[' | '{' | '<' => stack.push(c),
                ')' | ']' | '}' | '>' => {
                    if *opening_mapping.get(&c).unwrap() != stack.pop().unwrap() {
                        syntax_error_total += syntax_error_cost.get(&c).unwrap();
                        continue 'lines_iter;
                    }
                }
                _ => panic!(),
            }
        }

        let mut autocomplete_score = 0;
        while stack.len() > 0 {
            autocomplete_score *= 5;
            autocomplete_score += autocomplete_mapping.get(&stack.pop().unwrap()).unwrap();
        }
        autocomplete_scores.push(autocomplete_score);
    }

    println!("Part one = {}", syntax_error_total);

    autocomplete_scores.sort();
    let middle_autocomplete_score = autocomplete_scores[autocomplete_scores.len() / 2];
    println!("Part two = {}", middle_autocomplete_score);
}
