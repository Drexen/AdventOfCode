use std::collections::{HashMap, HashSet};

use regex::Regex;

fn main() {
    let mut input_split = include_str!("day-16-input.txt").split("nearby tickets:");
    let rules_str = input_split.next().unwrap();

    let my_ticket: Vec<u32> = rules_str
        .lines()
        .rev()
        .skip(1)
        .next()
        .unwrap()
        .split(",")
        .map(|l| l.parse().unwrap())
        .collect();

    let r = Regex::new(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)").unwrap();
    let mut rules: HashMap<&str, Vec<(u32, u32)>> = HashMap::new();
    for cap in r.captures_iter(rules_str) {
        let range: Vec<(u32, u32)> = vec![
            (
                cap.get(2).unwrap().as_str().parse().unwrap(),
                cap.get(3).unwrap().as_str().parse().unwrap(),
            ),
            (
                cap.get(4).unwrap().as_str().parse().unwrap(),
                cap.get(5).unwrap().as_str().parse().unwrap(),
            ),
        ];
        rules.insert(cap.get(1).unwrap().as_str(), range);
    }

    let nearby_tickets: Vec<Vec<u32>> = input_split
        .next()
        .unwrap()
        .lines()
        .skip(1)
        .map(|l| l.split(",").map(|n| n.parse().unwrap()).collect())
        .collect();

    part_one(&rules, &nearby_tickets);
    part_two(&rules, &nearby_tickets, &my_ticket);
}

fn part_one(rules: &HashMap<&str, Vec<(u32, u32)>>, nearby_tickets: &Vec<Vec<u32>>) {
    let sum: u32 = nearby_tickets
        .iter()
        .map(|ticket| get_ticket_scanning_error_rate(ticket, rules))
        .sum();

    println!("Part one = {}", sum);
}

fn part_two(
    rules: &HashMap<&str, Vec<(u32, u32)>>,
    nearby_tickets: &Vec<Vec<u32>>,
    my_ticket: &Vec<u32>,
) {
    let nearby_tickets: Vec<_> = nearby_tickets
        .iter()
        .filter(|t| get_ticket_scanning_error_rate(t, rules) == 0)
        .collect();

    // trim the possibilities
    let mut possibilities: Vec<HashSet<&str>> = vec![rules.keys().map(|k| *k).collect(); 20];
    for ticket in nearby_tickets {
        for (ti, ticket_element) in ticket.iter().enumerate() {
            for (rule_name, ranges) in rules {
                if possibilities[ti].contains(rule_name) {
                    if !is_value_in_ranges(*ticket_element, ranges) {
                        possibilities[ti].remove(rule_name);
                    }
                }
            }
        }
    }

    for _ in 0..possibilities.len() - 1 {
        let (single_element_index, _) = possibilities
            .iter()
            .enumerate()
            .filter(|(_, p)| p.len() == 1)
            .next()
            .unwrap();

        for i in 0..possibilities.len() {
            if i != single_element_index {
                let single_element_rule_name =
                    *possibilities[single_element_index].iter().next().unwrap();
                possibilities[i].remove(single_element_rule_name);
            }
        }

        // Nasty
        possibilities[single_element_index].insert(".");
    }

    let mut result: u64 = 1;
    for (i, r) in possibilities.iter().enumerate() {
        if r.iter()
            .filter(|r| **r != ".")
            .next()
            .unwrap()
            .starts_with("departure")
        {
            result *= my_ticket[i] as u64;
        }
    }

    println!("Part two = {}", result);
}

fn get_ticket_scanning_error_rate(
    ticket: &Vec<u32>,
    rules: &HashMap<&str, Vec<(u32, u32)>>,
) -> u32 {
    ticket
        .iter()
        .filter(|v| !is_value_in_ranges(**v, &rules.values().flatten().map(|r| *r).collect()))
        .sum()
}

fn is_value_in_ranges(v: u32, ranges: &Vec<(u32, u32)>) -> bool {
    ranges.iter().any(|range| v >= range.0 && v <= range.1)
}
